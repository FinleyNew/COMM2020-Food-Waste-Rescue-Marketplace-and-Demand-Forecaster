import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './Discover.css'
import axios from "axios";
function Streaks() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [bundle,setBundle] = useState(null); //defines the state and variable that allows the react page to be rerendered when called, no array as its one object that's returned
  

  useEffect(() => { //useEffect allows the command run on entering the page and if anything changes
    const token = localStorage.getItem('token'); //defines the token which we need to authorize the user and get their data
    axios.get(`${API_URL}/api/v1/consumers/me`,{ //the backend server url to get the information for 
      headers: {
        "Authorization": `Bearer ${token}`, //sending the token to verify the user
        "Content-Type": "application/json" //defines that we are getting a JSON object/piece of data
      }
    })
    .then(response => {
      setBundle(response.data); //updates the react state so the page can rerender with the new info
    })
    .catch(err => {
          console.error("Error fetching bundles:", err); //catches any errors and displays an erorr messages 
          alert("No data ");
    });
  },[]) //allows the page to rerender if anything changes




  return (
      <>
        <div className="discover">
          <nav className="row">
            <Link to="/login" className="button"><b>Login Page</b></Link>
            <Link to="/discover" className="button"><b>Discover</b></Link> {/* displays the links to the other pages */}
            <Link to="/codes" className="button"><b>Codes</b></Link>
          </nav>
          <h1 className="headline">Streaks</h1>
          <div className="mainBox">
            <div className="bundleEntry">
              {bundle && (
                <div>
                  <p className="textCentre">{bundle.display_name} has rescued for {bundle.streak} week(s) in a row!</p><hr></hr> {/* message to display the streak */}
                </div>
              )}
              <div className="rowIcons">
                <p className="headline">Badges:</p>
                <img className="icon" src="https://thumbs.dreamstime.com/b/modern-bronze-circle-metal-badges-labels-design-elements-vector-illustration-84952346.jpg" alt="Bronze Badge"/>   
                <img className="icon" src="https://img.favpng.com/11/16/23/gold-medal-silver-medal-illustration-png-favpng-vJK1hRCuK1bUdtG0Hb4dJ7VkU.jpg" alt="Silver Badge"/>   
                <img className="icon" src="https://www.onlygfx.com/wp-content/uploads/2022/04/blank-gold-badge-label-2.png" alt="Gold Badge"/>   {/* badge images */}
              </div>
              <div className="textBox">
                <p>Summary PIS</p> {/* summary statement */}
              </div>
            </div>
          </div>
        </div>
      </>
    );
}

export default Streaks; //exports the component so it can be imported in other files
