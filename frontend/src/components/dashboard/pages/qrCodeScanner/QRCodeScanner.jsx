import './qrCodeScanner.css';
import './qrCodeScannerMobile.css';

import {useEffect, useState, useRef} from "react";
import {useNavigate} from "react-router-dom";
import {QrScanner} from '@yudiel/react-qr-scanner';
import httpClient from "../../../../httpClient";
import {getCookie} from "../../../../helpers";

import {Tick, Cross} from "../../../../img";
import Button from "react-bootstrap/Button";

const QRCodeScanner = (props) => {
    const user = props.user;
    const setUser = props.setUser;
    let event = props.event;
    let [validImg, setValidImg] = useState();
    let [ticketMsg, setTicketMsg] = useState();
    let [ticketType, setTicketType] = useState();
    const [hasScanned, setHasScanned] = useState(false);
    const scannerRef = useRef(null);

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null || (user.role !== "management")) {
            navigate("/")
        }
    }, [user])

    const handleDecode = (result) => {
        if (hasScanned) {
            return;
        }

        setHasScanned(true);

        const data = {
            event_id: event.event_id,
            qr_data: result
        }

        httpClient.post(`/ticket/validate`, data, {
            headers: {
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": getCookie("csrf_access_token"),
            }
        })
        .then(response => {
            // valid ticket
            setValidImg(Tick);
            setTicketMsg(response.msg);
            setTicketType(response.ticket_type);
        })
        .catch(error => {
            console.log(error)
            if (error.response) {
                // invalid ticket
                setValidImg(Cross);
                setTicketMsg(error.response.data.msg)
            }
        });

        scannerRef.current.stop();
    }

    let content;
    if (!hasScanned) {
        content = <QrScanner scanDelay={15000}
                             onDecode={handleDecode}
                             onError={(error) => console.log(error?.message)} />;
    } else {
        content =
            <div>
                <img className={'ticketImgResponse'} src={validImg} />
                <div className={'ticketResponseContainer'}>
                    <p className={'ticketResponseMsg'}>
                        {validImg === Cross ?
                            <span style={{ color: "red"}}>Error: </span>
                        :
                            <span style={{ color: "green"}}>Success: </span>}
                        {ticketMsg}
                    </p>
                    {validImg === Tick && <br/>}
                    {validImg === Tick &&
                        <p className={'ticketResponseText'}>Ticket Type: {ticketType}</p>
                    }
                </div>
            </div>;
    }

    return (
        <div className={'contentContainer qrScannerDiv'}>
            <h1 className={'scannerHeader'}>Scan Ticket: {event.event_name}</h1>
            {content}
            {hasScanned &&
                <Button className={'scannerButton'} onClick={() => {
                    setHasScanned(false);
                    scannerRef.current.start();
                }} variant="primary">Scan Next Ticket</Button>
            }
        </div>
    )
}

export default QRCodeScanner;