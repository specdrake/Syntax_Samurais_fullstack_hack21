import { BrowserRouter, Route, Switch } from 'react-router-dom'
import Home from './components/home.js'
import Login from './components/login.js'
import Account from './components/account.js'
import Dashboard from './components/dashboard.js'
import NavBar from './components/navbar.js'

function App() {
	return (
		<BrowserRouter>
		<NavBar />
		<Switch>
			<Route component={Home} path='/' exact />
			<Route component={Login} path='/login' />
			<Route component={Account} path='/account' />
			<Route component={Dashboard} path='/dashboard' />
		</Switch>
		</BrowserRouter>
	);
}

export default App;
