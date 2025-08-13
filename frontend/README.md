# How to run React client

Within the /frontend directory:
`npm install`
`set HTTPS=false&&npm start`

Then navigate to http://localhost:3000

# How to use QR code scanner
## Desktop
As long as you are navigating to QR code scanner from `localhost` then it should use your webcam as expected to validate tickets as a management user.

## Mobile
To use it on mobile, React and Flask must be running securely on HTTPS.

To run React on HTTPS run `set HTTPS=true&&npm start` from the frontend directory and navigate to https://localip:3000 
in mobile browser. You may also have to navigate to https://localip:5000/docs in order to validate the certificate for 
Flask's 5000 port.

To set the local IP, look in `package.json` and change the `REACT_APP_ROUTE_URL` to equal your IP with HTTPS and the 5000 port.
