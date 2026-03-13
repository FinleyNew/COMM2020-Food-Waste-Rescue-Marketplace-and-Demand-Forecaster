import { Routes, Route, Link } from "react-router-dom";
import {useState, useEffect} from "react";
import './Discover.css'
import axios from "axios";
import Company from "../assets/Company.png";
import Bundle from "../assets/BundleImage.png";
function Discover() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [bundles, setBundles] = useState([]); //defines the state and variable that allows the react page to be rerendered when called

 



    useEffect(() => { //useEffect allows the command run on entering the page and if anything changes
      
      axios.get(`${API_URL}/api/v1/bundles/`,{
        headers:{
          "Content-Type": "application/json" //defines that we are getting a JSON object/piece of data
        }
      })
      .then(response => {
        setBundles(response.data); //updates the react state so the page can rerender with the new info
      })
      .catch(err => {
          console.error("Error fetching bundles:", err); //catches any errors and displays an erorr messages 
          alert("No data ");
        });
    }, [])



  return (
    <>
      <div className="discover">
        <nav class="row">
            <Link to="/login" className="button"><b>Login Page</b></Link> {/* displays the links to the other pages */}
            <Link to="/streaks" className="button"><b>Streaks</b></Link>
            <Link to="/codes" className="button"><b>Codes</b></Link>
        </nav>
        <h1 className="headline">Bundles</h1>

            {bundles.map(bundle => (
              <Link to={`/bundle/${bundle.posting_id}`} className="mainBox" key={bundle.posting_id}> {/* needs a key to uniquely identify a specific object when traversing through them all */}
                  <div className="bundleEntry">
                      <img src={Bundle} alt="Bundle" className="bundleImage"/>
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
