import { useState } from 'react'
import moment from 'moment'
import { Link } from 'react-router-dom'

export default function Dashboard() {

	const [isLoggedIn, setLogin] = useState(true)

	if (!isLoggedIn) {
		// return <Redirect to="/login" />
	}

	const user = {
		due: new Date('June 28, 2021'),
		received: 1,
		waypoint: {
			address: "Bawana Industrial Area",
			date: new Date('June 29, 2021 10:30:00')
		}
	}

	function getDays(next) {
		let cur = new Date();
		let td = next.getTime() - cur.getTime()
		return Math.floor(td / (1000 * 60 * 60 * 24));
	}

	function parseStatus(received) {
		if (received == 1) return 1 + " dose"
		return received + " doses"
	}

	function parseDate(date) {
		return moment(date).format("Do MMMM YYYY, hh:mm a")
	}

	return (
		<div className="dashboard">
			<div className="dash-area">
				<div className="dash-tip">
					Your next vaccination is due in <span>{getDays(user.due)}</span> days
				</div>
				<div className="dash-tip">
					You have received <span>{parseStatus(user.received)}</span> so far
				</div>
				<div className="dash-tip">
					Your booked waypoint: 
					<div className="dash-add">
						<p>{user.waypoint.address}</p>
						<p>{parseDate(user.waypoint.date)}</p>
					</div>
				</div>
				<Link to="/" className="link ret-link">
					<div className="ret-button">Return to Home</div>
				</Link>
			</div>
		</div>
	);
}
