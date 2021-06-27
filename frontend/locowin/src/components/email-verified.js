import { Link } from "react-router-dom";

export default function EmailVerified() {
    let email = JSON.parse(localStorage.getItem('user-email'))

    return (
        <div className="email">
            <div className="message">Your e-mail has been verified. You may now login.</div>
            <div className="mail">{email}</div>
            <Link to="/login" className="link" onClick={() => localStorage.clear()}>
                <div className="return">Login</div>
            </Link>
        </div>
    );
}
  