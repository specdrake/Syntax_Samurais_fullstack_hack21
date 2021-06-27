import { BrowserRouter, Route, Switch } from 'react-router-dom'
import Home from './components/home.js'
import Login from './components/login.js'
import Account from './components/account.js'
import Dashboard from './components/dashboard.js'
import NavBar from './components/navbar.js'
import EmailSent from './components/email-sent.js'
import EmailVerified from './components/email-verified.js'

function App() {
	return (
		<BrowserRouter>
		<NavBar />
		<Switch>
			<Route component={Home} path='/' exact />
			<Route component={Login} path='/login' />
			<Route component={Account} path='/account' />
			<Route component={Dashboard} path='/dashboard' />
			<Route component={EmailSent} path='/email-sent' />
			<Route component={EmailVerified} path='/email-verified' />
		</Switch>
		</BrowserRouter>
	);
}

export default App;
