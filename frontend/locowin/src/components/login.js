import { Redirect } from 'react-router-dom'
import { useState } from 'react';
import PopupComp from '../helpers/Popup-comp';

const BASE = 'https://locowin.herokuapp.com'

export default function Login() {
    const [prop, setProp] = useState({sev: "", msg: ""})
    function login(e) {
        e.preventDefault();
        let username = document.getElementById('login-user').value
        let password = document.getElementById('login-pass').value
        
        fetch(`${BASE}/auth/login/`, { 
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password}),
        })
        .then(response => {
			if (!response.ok) {
				throw "Something went wrong"
			}
			return response.json()
		})
        .then(data => {
			localStorage.setItem('logged-user', JSON.stringify(data))
			window.location.reload()
        })
		.catch(err => {
			setProp({sev: 'error', msg: err})
		})
    }

    function register(e) {
        e.preventDefault();
        let email = document.getElementById('reg-mail').value
        let username = document.getElementById('reg-user').value
        let password = document.getElementById('reg-pass').value
        
        fetch(`${BASE}/auth/register/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, username, password}),
        })
        .then(response => {
			if (!response.ok) {
				throw "Something went wrong"
			}
			return response.json()
		})
        .then(data => {
            localStorage.setItem('user-email', JSON.stringify(email))
            window.location.reload()
        })
		.catch(err => {
			setProp({sev: 'error', msg: err})
		})
    }

    const user = JSON.parse(localStorage.getItem('logged-user'))
    const email = localStorage.getItem('user-email')

    if (email) {
        return <Redirect to="/email-sent" />
    }

    if (user) {
        if (user.first_time_login) {
            return <Redirect to="/account" />
        } else {
            return <Redirect to="/dashboard" />
        }
    }

	return (
		<div className="login">
			<div className="login-f">
				<div className="log-title">Login</div>
				<form>
					<input type="text" placeholder="username" id="login-user" />
					<input type="password" placeholder="password" id="login-pass" />
					<button onClick={login} className="log-btn">Login</button>
				</form>
			</div>
			<div className="sep"></div>
			<div className="register-f">
				<div className="log-title">Register</div>
				<form>
					<input type="text" placeholder="email" id="reg-mail" />
					<input type="text" placeholder="username" id="reg-user" />
					<input type="password" placeholder="password" id="reg-pass" />
					<button onClick={register} className="log-btn">Register</button>
				</form>
			</div>
            <PopupComp data={prop} />
		</div>
	);
}