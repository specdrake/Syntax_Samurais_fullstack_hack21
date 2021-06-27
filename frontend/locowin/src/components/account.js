import { Redirect } from 'react-router-dom'
import { useState } from 'react'
import PopupComp from '../helpers/Popup-comp'

const BASE = 'https://locowin.herokuapp.com'

export default function Account() {
    const [prop, setProp] = useState({sev: "", msg: ""})
    let user = JSON.parse(localStorage.getItem('logged-user'))

    if (!user) {
		return <Redirect to="/login" />
	}

    let userLocation;

    function setLocation(loc) {
        userLocation = loc
        return loc
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setLocation);
    }

    function save(e) {
        e.preventDefault();
        let name = document.getElementById('acc-name').value
        let age = document.getElementById('acc-age').value
        let aadhar = document.getElementById('acc-aadh').value
        let phone = document.getElementById('acc-num').value
        let latitude = "" + userLocation.coords.latitude
        let longitude = "" + userLocation.coords.longitude
        let received = document.getElementById('acc-doses').value
        let special = document.getElementById('acc-com').checked
        fetch(`${BASE}/auth/profile/${user.username}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${user.tokens.access}`
            },
            body: JSON.stringify({name, age, aadhar, phone, latitude, longitude, received, special}),
        })
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('user-profile', JSON.stringify(data))
            user.first_time_login = false
            localStorage.setItem('logged-user', JSON.stringify(user))
            setProp({sev: "info", msg: "Your profile has been updated"})
        })
        .catch(err => {
            setProp({sev: "error", msg: err})
        })
    }
    
    return (
        <div className="account">
            <div className="acc-area">
                <div className="acc-title">Enter your account details</div>
                <form>
                    <input type="text" placeholder="Name" id="acc-name" />
                    <input type="number" placeholder="Age" id="acc-age" />
                    <input type="text" placeholder="Aadhaar No." id="acc-aadh" />
                    <input type="text" placeholder="Phone Number" id="acc-num" />
                    <select id="acc-doses">
                        <option value="0">0</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                    </select>
                    <input type="checkbox" id="acc-com" name="acc-com" value={true} />
                    <label htmlFor="acc-com">I have co-morbidities</label>
                    <button onClick={save} className="acc-btn">Save Changes</button>
                </form>
            </div>
            <PopupComp data={prop} />
        </div>
    );
}
  