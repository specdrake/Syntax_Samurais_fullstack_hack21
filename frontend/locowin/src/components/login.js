import { Redirect } from 'react-router-dom'
import { useState } from 'react'

const BASE = 'https://locowin.herokuapp.com'

export default function Login() {

	const [isLoggedIn, setLogin] = useState(false)
	const [isFirstTime, setFirstTime] = useState(false)
	const [user, setUser] = useState(null)

	function login() {
		
	}

	function register() {
		
	}

	if (isFirstTime) {
		return <Redirect to="/account" />
	}

	if (isLoggedIn) {
		return <Redirect to="/dashboard" />
	}

	return (
		<div className="login">
			<div className="login-f">
				<div className="log-title">Login</div>
				<form>
					<input type="text" placeholder="username" id="login-user" />
					<input type="password" placeholder="password" id="login-pass" />
					<button onClick={login}>Login</button>
				</form>
			</div>
			<div className="sep"></div>
			<div className="register-f">
				<div className="log-title">Register</div>
				<form>
					<input type="text" placeholder="email" id="reg-mail" />
					<input type="text" placeholder="username" id="reg-user" />
					<input type="password" placeholder="password" id="reg-pass" />
					<button onClick={register}>Register</button>
				</form>
			</div>
		</div>
	);
}