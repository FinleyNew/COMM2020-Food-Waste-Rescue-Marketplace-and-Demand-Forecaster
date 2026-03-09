import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './Codes.css'
import Company from "../assets/Company.png";
function Codes() {
  const [bundles, setBundles] = useState([]); //needs an empty array as it will display a list of data instead of of one object
    
    useEffect(() => { //useEffect allows the command run on entering the page and if anything changes
      const token = localStorage.getItem('token'); //defines the token which we need to authorize the user and get their data
      fetch("http://127.0.0.1:8000/api/v1/reservations/me",{ //the backend server url to get the information for 
        headers:{ //extra information to send to the backend
          "Authorization": `Bearer ${token}`, //sending the token to verify the user
          "Content-Type": "application/json" //defines that we are getting a JSON object/piece of data
        }
      }) //fetch here , useeffect means it only fetches once
        .then(res => res.json()) //converts the data into an object JSON
        .then(data => {
          console.log("API DATA:", data); 
          setBundles(data); //updates the react state so the page can rerender with the new info
        })
        .catch(err => {
          console.error("Error fetching bundles:", err);
          alert("No data ");
        });
    }, []); //if anything changes reload the page
    if (!bundles) return <p>Loading bundle...</p>;
  
  return (
      <>
      <div className="codes">
        <nav className="row">
          <Link to="/login" className="button"><b>Login Page</b></Link> {/* defines the links to the other other pages */}
          <Link to="/discover" className="button"><b>Discover</b></Link>
          <Link to="/streaks" className="button"><b>Streaks</b></Link>
        </nav>
        <h1>Codes</h1>
          {bundles.map(bundle => ( //have to use a map as there are multiple objects all with multiple data attributes, so using a map to traverse them
            <div key={bundle.posting_id}> {/* needs a key to uniquely identify a specific object when traversing through them all */}
              <div className="mainBox">
                <div className="bundleEntry">
                  <div className="textBox">
                    <div className="bundleRow">
                      <h1>Bundle Name</h1>
                      <h2>Claim Code: {bundle.claim_code}</h2> {/* displaying all the information by accessing the specific object */}
                    </div>
                    <div className="bundleRow">
                      <div className="column">
                          <p>Status: {bundle.status}</p>
                          <p>Reservation ID : {bundle.reservation_id}</p>
                          <p>Bundle ID: {bundle.posting_id}</p>
                      </div>
                      <div className="column">
                        <img src={Company} alt="Company" className="companyIcon"/>
                      </div>
                    </div>
                  </div>
                  </div>
                </div>
              </div>
          ))}
      </div>
      </>
    );
}

export default Codes; //exports the component so it can be imported in other files
