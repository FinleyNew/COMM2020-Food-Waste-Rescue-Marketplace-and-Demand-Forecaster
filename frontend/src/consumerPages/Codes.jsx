import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './Discover.css'
import Company from "../assets/Company.png";
import axios from "axios";
function Codes() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [bundles, setBundles] = useState([]); //needs an empty array as it will display a list of data instead of of one object
    
    


    useEffect(() => { //use effect allows the command run on entering the page and if anything changes
      const token = localStorage.getItem('token'); //defines the token which we need to authorize the user and get their data
      axios.get(`${API_URL}/api/v1/reservations/me`,{ //the server url to get the information for 
        headers: {
          "Authorization": `Bearer ${token}`, //sending the token to verify the user
          "Content-Type": "application/json" //defines that we are getting a JSON object/piece of data
        }
      })
      .then(response => {
        setBundles(response.data); //updates the react state so the page can rerender with the new info
      })
      .catch(err =>{
        console.error("request failed",err);
      })
    },[]) //if anything changes reload the page




    if (!bundles) return <p>Loading bundle...</p>;
  
  return (
      <>
        <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link> {/* defines the links to the other other pages */}
        <Link to="/discover" className="button"><b>Discover</b></Link>
        <Link to="/streaks" className="button"><b>Streaks</b></Link>
      </nav>
      <h1 className="headline">Codes</h1>
      <section className="column">
        {bundles.map(bundle => ( //have to use a map as there are multiple objects all with multiple data attributes, so using a map to traverse them
          <div key={bundle.posting_id}> {/* needs a key to uniquely identify a specific object when traversing through them all */}
          <section>
            <div className="bundleEntry">
              <div className="textBlock">
                <img src={Company} alt="Company" className="leftImg"/>
                <div className="desc">
                  <p className="desc">Reservation ID : {bundle.reservation_id}</p>
                  <p className="desc">Claim Code - {bundle.claim_code}</p> {/* displaying all the information by accessing the specific object */}
                </div>
              </div>
              <div className="textBlock">
                <div className="desc">
                  <p className="codeText">Status - {bundle.status}</p>
                  <p>Bundle ID - {bundle.posting_id}</p>
                  
                </div>
              </div>
              </div>
            </section>
            <div className="whitespace" aria-hidden="true"></div>
            </div>
        ))}
      </section>
      
      </>
    );
}

export default Codes; //exports the component so it can be imported in other files
