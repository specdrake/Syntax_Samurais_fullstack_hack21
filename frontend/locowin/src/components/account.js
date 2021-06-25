import { Redirect } from 'react-router-dom'
import { useState } from 'react'
// import '../css/style.css'

export default function Account() {

    const [isLoggedIn, setLogin] = useState(false)
    const [isFirstLogin, setFirst] = useState(false)

    if (!isLoggedIn) {
		// return <Redirect to="/login" />
	}

    function save() {
        // validate info

		return <Redirect to="/dashboard" />
    }

    return (
        <div className="account">
            <div className="acc-area">
                <div className="acc-title">Enter your account details</div>
                <form>
                    <input type="text" placeholder="Name" />
                    <input type="number" placeholder="Age" />
                    <input type="text" placeholder="Phone Number" />
                    
                    <button onClick={save}>Save Changes</button>
                </form>
            </div>
        </div>
    );
}
  