import { useState } from 'react'
import IconButton from '@material-ui/core/IconButton';
import Collapse from '@material-ui/core/Collapse'
import { Alert, AlertTitle } from '@material-ui/lab'
import CloseIcon from '@material-ui/icons/Close';

export default function PopupComp(props) {
    const [popup, setPopup] = useState("")
	const [open, setOpen] = useState(true);
    
    function renderPopup(sev, msg) {
        if (!sev) return (<span></span>)
        let sevCpy = sev.substr(1)
        let title = sev[0].toUpperCase() + sevCpy
        return (
            <Collapse in={open} style={{
                position: "fixed",
                width: "80vw",
                bottom: "20px",
                left: "10vw",
                zIndex: "500"
            }}>
                <Alert
                action={
                    <IconButton aria-label="close" color="inherit" size="small" style={{height: "auto"}}
                        onClick={() => {
                            setOpen(false);
                            setPopup("")
                        }}>
                        <CloseIcon fontSize="inherit" />
                    </IconButton>
                }
                severity={sev}>
                    <AlertTitle>{title}</AlertTitle>{msg}
                </Alert>
            </Collapse>
        )
    }

    return (
        <div>
            {renderPopup(props.data.sev, props.data.msg)}
        </div>
    )
}