import { Routes, Route, Link } from "react-router-dom";
import {useState, useEffect} from "react";
import './Discover.css'

import Company from "../assets/Company.png";
import Bundle from "../assets/BundleImage.png";
function Discover() {
  
  const [bundles, setBundles] = useState([]); //defines the state and variable that allows the react page to be rerendered when called

  useEffect(() => { //useEffect allows the command run on entering the page and if anything changes
      const token = localStorage.getItem('token'); //defines the token which we need to authorize the user and get their data
      fetch("http://127.0.0.1:8000/api/v1/bundles/",{ //the backend server url to get the information for 
        headers:{
          "Content-Type": "application/json" //defines that we are getting a JSON object/piece of data
        }
      }) //fetch here , useeffect means it only fetches once
        .then(res => res.json()) //converts the data into an object JSON
        .then(data => {
          console.log("API DATA:", data); 
          setBundles(data); //updates the react state so the page can rerender with the new info
        })
        .catch(err => {
          console.error("Error fetching bundles:", err); //catches any errors and displays an erorr messages 
          alert("No data ");
        });
    }, []);
  return (
    <>
      <div className="discover">
        <nav class="row">
            <Link to="/login" className="button"><b>Login Page</b></Link> {/* displays the links to the other pages */}
            <Link to="/streaks" className="button"><b>Streaks</b></Link>
            <Link to="/codes" className="button"><b>Codes</b></Link>
            <details>
            <summary>
                <img className="setting" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBdndCKhAJ4SlVEaNCkA4U6BN4tDXZsRtxSw&s"></img> {/* holds the images for the settings page */}
            </summary>
            <label>
                <input type="checkbox" name="darkmode"/> {/* checkbox for darkmode */}
                Enable Dark Mode DOESNT WORK YET
            </label>
            </details>
        </nav>
        <h1 className="headline">Bundles</h1>

            {bundles.map(bundle => (
              <Link to={`/bundle/${bundle.posting_id}`} className="mainBox" key={bundle.posting_id}> {/* needs a key to uniquely identify a specific object when traversing through them all */}
                  <div className="bundleEntry">
                      <img src={Bundle} alt="Bundle" className="rowImg"/>
                      <div className="textBox">
                          <div className="bundleRow">
                              <h1>Bundle Name</h1>
                              <h1>{bundle.available} Available</h1>
                          </div>
                          <div className="bundleRow">
                              <div className="column">
                                  <p>Collection Time: {bundle.formatted_time_range}</p>
                                  <p>Price: £{bundle.price_display}</p>
                              </div>
                              <img src={Company} alt="Company" className="companyIcon"/>
                          </div>
                      </div>
                  </div>
                </Link>
            ))}
        </div>
    </>
);
}

export default Discover; //exports the component so it can be imported in other files
