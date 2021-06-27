import { useEffect, useState } from 'react'
import { BsChevronDown } from 'react-icons/bs'
import '../css/style.css'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import moment from 'moment'
import { Redirect } from 'react-router-dom'
import PopupComp from '../helpers/Popup-comp'

const BASE = 'https://locowin.herokuapp.com'

export default function Home() {
	const [waypoints, setWaypoints] = useState([])
	const [prop, setProp] = useState({sev: "", msg: ""})

	let user = JSON.parse(localStorage.getItem('logged-user'))
	let profile = JSON.parse(localStorage.getItem('user-profile'))

	const [best_wp, setWp] = useState([])

	useEffect(() => {
		fetch(`${BASE}/vaccine/all`, { 
            method: 'GET',
            headers: {'Content-Type': 'application/json',},
        })
        .then(response => {
			if (!response.ok) {
				throw "Something went wrong"
			}
			return response.json()
		})
        .then(data => {
            setWaypoints(data)
        })
		.catch(err => {
			setProp({sev: 'error', msg: err})
			// getPopup('error', err)
		})

		if (user) {
			fetch(`${BASE}/auth/profile/${user.username}`, {
				method: 'PUT',
				mode: 'cors',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${user.tokens.access}`
				},
				body: JSON.stringify(profile),
			})
			.then(response => response.json())
		}

		if (user && user.tokens && user.tokens.access) {
			fetch(`${BASE}/vaccine/best`, { 
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
				setWp(data.result)
			})
			.catch(err => {
				setProp({sev: 'error', msg: err})
				// getPopup('error', err)
			})
		}

	}, [])
	
	if (!profile) {
		return <Redirect to="/dashboard" />
	}

	let profObj = profile[0]
	if (!profObj) {
		profObj = profile
	}

	if (user) {
		if (user.first_time_login) {
			return <Redirect to="/account" />
		}
	}

    function getDate(eta) {
        return moment(eta).format("Do MMMM YYYY")
    }

    function getTime(eta) {
        return moment(eta).format("hh:mm a")
    }

	function book(c) {
		fetch(`${BASE}/vaccine/book/`, {
			method: 'POST',
            mode: 'cors',
            headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${user.tokens.access}`
			},
            body: JSON.stringify({
				date: c.eta,
				id: Math.floor(~~c.id)
			}),
		})
		.then(response => {
			if (!response.ok) {
				throw "Something went wrong"
			}
			return response.json()
		})
		.then(data => {
			setProp({sev: "success", msg: "Your vaccine has been booked successfully"})
		})
		.catch(err => {
			setProp({sev: "error", msg: err})
		})
	}

    function renderMarker(waypoint) {
        return (
			<Marker position={[waypoint.latitude, waypoint.longitude]} key={waypoint.id}>
				<Popup>
					<div className="tip-title">{waypoint.name}</div>
					<div className="tip-date">{getDate(waypoint.eta)}</div>
					<div className="tip-time">{getTime(waypoint.eta)}</div>
					<div className="capacity">Available doses: <span>{waypoint.capacity}</span></div>
				</Popup>
			</Marker>
		)
    }

    function renderMap() {
        return (
			<MapContainer className="map-container" center={[~~profObj.latitude + 0.73, ~~profObj.longitude + 0.11]} zoom={13} scrollWheelZoom={false}>
				<TileLayer
					attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
					url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
				/>
				{waypoints.map(c => renderMarker(c))}
			</MapContainer>
		)
    }

	function formatDate(date) {
		return ("at " + moment(date).format("hh:mm a") + " on " + moment(date).format("Do MMMM YYYY"))
	}

	function bestWaypoint(c) {
		return (
			<div className="wayp" key={c.id}>
				<div className="wp-title">{c.name}</div>
				<div className="wp-venue">{formatDate(new Date(c.eta))}</div>
				<div className="wp-buttons">
					<div className="wp-book" onClick={() => book(c)}>Book</div>
				</div>
			</div>
		)
	}

	function down() {
		if (user) {
			return (<BsChevronDown className="arrow" />)
		}
	}

	function renderMapSection() {
		if (user) {
			return (
				<div className="map">
					<h1 className="map-title">View all waypoints</h1>
					<div className="map-section">
						{renderMap()}
					</div>
				</div>
			)
		}
	}

	function renderWaypoints() {
		if (user) {
			return (
				<div className="waypoints">
					<h1 className="wayp-title">Your next available waypoints</h1>
					<h3 className="wayp-tag">Choose your venue to get vaccinated</h3>
					<div className="vax-img">
						<img src="http://cdn.onlinewebfonts.com/svg/img_488760.png" alt="vaccine" />
					</div>
					<div className="wayp-list">
						{best_wp.map((c) => bestWaypoint(c))}
					</div>
				</div>
			)
		}
	}

    return (
		<div className="home">
			<div className="front">
				<h1 className="stat">31,48,41,384</h1>
				<h3 className="stat-tag">vaccinated so far</h3>
				{down()}
			</div>
			{renderMapSection()}
			{renderWaypoints()}
			<PopupComp data={prop} />
		</div>
    );
}
  