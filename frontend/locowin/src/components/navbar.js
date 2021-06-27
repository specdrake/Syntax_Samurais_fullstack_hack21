import { Link } from 'react-router-dom'

export default function NavBar() {
    const user = JSON.parse(localStorage.getItem('logged-user'))
    
    function getNavData() {
        if (!user) {
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
        } else if (user.first_time_login) {
            return
        } else {
            return (
                <div className="buttons">
                    <Link to="/dashboard" className="link">
                        <div className="nav-dash">Dashboard</div>
                    </Link>
                    <Link to="/login" className="link" onClick={() => localStorage.clear()}>
                        <div className="nav-dash">Log Out</div>
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
  