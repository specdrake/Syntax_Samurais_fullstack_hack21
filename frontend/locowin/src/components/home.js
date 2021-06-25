import { useState } from 'react'
import { BsChevronDown } from 'react-icons/bs'
// import '../css/style.css'
// import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
// import moment from 'moment'

export default function Home() {
	const [vaxxes, getVaxxes] = useState(null)

	function renderMap() {
		
	}

    return (
		<div className="home">
			<div className="front">
				<h1 className="stat">15,29,47,291</h1>
				<h3 className="stat-tag">vaccinated so far</h3>
				<BsChevronDown className="arrow" />
			</div>
			<div className="map">
				<h1 className="map-title">Choose a waypoint</h1>
				<div className="map-section">
					{renderMap()}
				</div>
			</div>
			<div className="waypoints">
				<h1 className="wayp-title">Your next available waypoints</h1>
				<h3 className="wayp-tag">Choose your venue to get vaccinated</h3>
				<div className="vax-img"></div>
				<div className="wayp-list">
					<div className="wayp">
						<div className="wp-title">Bawana Industrial Area</div>
						<div className="wp-venue">at 4:30pm on 22nd June 2021</div>
						<div className="wp-buttons">
							<div className="wp-view">View</div>
							<div className="wp-book">Book</div>
						</div>
					</div>
					<div className="wayp">
						<div className="wp-title">Bawana Industrial Area</div>
						<div className="wp-venue">at 4:30pm on 22nd June 2021</div>
						<div className="wp-buttons">
							<div className="wp-view">View</div>
							<div className="wp-book">Book</div>
						</div>
					</div>
					<div className="wayp">
						<div className="wp-title">Bawana Industrial Area</div>
						<div className="wp-venue">at 4:30pm on 22nd June 2021</div>
						<div className="wp-buttons">
							<div className="wp-view">View</div>
							<div className="wp-book">Book</div>
						</div>
					</div>
					<div className="wayp">
						<div className="wp-title">Bawana Industrial Area</div>
						<div className="wp-venue">at 4:30pm on 22nd June 2021</div>
						<div className="wp-buttons">
							<div className="wp-view">View</div>
							<div className="wp-book">Book</div>
						</div>
					</div>
					<div className="wayp">
						<div className="wp-title">Bawana Industrial Area</div>
						<div className="wp-venue">at 4:30pm on 22nd June 2021</div>
						<div className="wp-buttons">
							<div className="wp-view">View</div>
							<div className="wp-book">Book</div>
						</div>
					</div>
				</div>
			</div>
		</div>
    );
}
  