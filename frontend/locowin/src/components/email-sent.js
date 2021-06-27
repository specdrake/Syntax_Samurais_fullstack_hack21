export default function EmailSent() {

    let email = JSON.parse(localStorage.getItem('user-email'))

    return (
        <div className="email">
            <div className="message">An e-mail has been sent to verify your mail ID</div>
            <div className="mail">{email}</div>
            <div className="tip">
                Please click on the link sent to your mail ID and you will be redirected
                to the website. You may close this page.
            </div>
        </div>
    );
}
  