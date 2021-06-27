import { Link, Redirect } from 'react-router-dom'
import PopupComp from '../helpers/Popup-comp'
import { useState, useEffect } from 'react'
import moment from 'moment'

const BASE = 'https://locowin.herokuapp.com'

export default function Dashboard() {
	const [prop, setProp] = useState({sev: "", msg: ""})
	let user = JSON.parse(localStorage.getItem('logged-user'))
	const [dash_data, setDash] = useState({
		due_days: null,
		doses: '-',
		message: "You are yet to book a slot"
	})


	function updateDash() {
		fetch(`${BASE}/vaccine/dashboard`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${user.tokens.access}`
			},
		})
		.then(response => {
			if (!response.ok) {
				throw "Something went wrong"
			}
			return response.json()
		})
		.then(data => {
			setDash(data)
		})
		.catch(err => {
			setProp({sev: 'error', msg: err})
		})
	}

	useEffect(() => {
		if (user)
			updateDash()
	}, [])


	if (!user) {
		return <Redirect to="/login" />
	}

	function parseStatus(received) {
		if (received === 1) return 1 + " dose"
		return received + " doses"
	}

	function parseDate(date) {
		return moment(date).format("on Do MMMM YYYY, hh:mm a")
	}

	function cancel() {
		fetch(`${BASE}/vaccine/cancelself/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${user.tokens.access}`
			},
		})
		.then(response => {
			if (!response.ok) {
				throw "Something went wrong"
			}
			return response.json()
		})
		.then(data => {
			setProp({sev: 'success', msg: "Your booking was cancelled successfully"})
			updateDash()
		})
		.catch(err => {
			setProp({sev: 'error', msg: err})
		})
	}

	function parseWp() {
		if (dash_data.message == null) {
			return (
				<div className="dash-tip">
					Your booked waypoint is
					<div className="dash-add">
						<p>{dash_data.waypoint}</p>
						<p>{parseDate(new Date(dash_data.datetime))}</p>
					</div>
				</div>
			)
		}
		return (
			<div className="dash-tip">
				{dash_data.message}
			</div>
		)
	}

	function parseDue(x) {
		if (x == null) return "-"
		return x + 1
	}

	return (
		<div className="dashboard">
			<div className="dash-area">
				<div className="dash-tip">
					Your next vaccination is due in <span>{parseDue(dash_data.due_days)}</span> days
				</div>
				<div className="dash-tip">
					You have received <span>{parseStatus(dash_data.doses)}</span> so far
				</div>
				{parseWp()}
				<div className="ret-button cancel-btn" onClick={() => cancel()}>Cancel booking</div>
				<Link to="/account" className="link edit-link">
					<div className="ret-button">Edit account details</div>
				</Link>
				<Link to="/" className="link ret-link">
					<div className="ret-button">Return to Home</div>
				</Link>
			</div>
			<PopupComp data={prop} />
		</div>
	);
}
