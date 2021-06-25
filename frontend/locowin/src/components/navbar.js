import { useState } from 'react';
import { Link } from 'react-router-dom'

export default function NavBar() {
    const [loggedIn, setLogin] = useState(false)

    function getNavData() {
        if (!loggedIn) {
            return (
                <div className="buttons">
                    <Link to="/login" className="link">
                        <div className="nav-log">Log In</div>
                    </Link>
                    <Link to="/login" className="link">
                        <div className="nav-reg">Register</div>
                    </Link>
                </div>    
            )
        } else {
            return (
                <div className="buttons">
                    <Link to="/dashboard" className="link">
                        <div className="nav-dash">Dashboard</div>
                    </Link>
                </div>  
            ) 
        }
    }

    return (
        <div className="nav">
            <Link to="/" className="link">
                <div className="title">LoCoWin</div>
            </Link>
            {getNavData()}
        </div>
    );
}
  