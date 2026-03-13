import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './CurrentBundles.css'
import Company from "../assets/Company.png";
import Bundle from "../assets/BundleImage.png";
import axios from "axios";
function CurrentBundles() {
  const API_URL = import.meta.env.VITE_API_URL;
  const [bundles, setBundles] = useState([]); //create state
  const [noBundles, setNoBundles] = useState(false);
  const [code, setCode] = useState("");

  const navigate = useNavigate();
  


  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/bundles/me`, {
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      setBundles(response.data);
      if (response.data.length === 0) {
          setNoBundles(true);
        } else {
          setBundles(response.data);
          setNoBundles(false);
        }
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });
  },[])



  const deleteBundle = (posting_id) => { //Function to delete bundles from backend
    const API_URL = import.meta.env.VITE_API_URL;
    if (!window.confirm("Delete this bundle?")) return;

    axios.get(`${API_URL}/api/v1/bundles/${posting_id}`, {
    
    })
    .then(response => {
      console.log("Deleted:", response.data);
      alert("Bundle deleted");
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
    });
    
    
};

const enterCode = (claim_code) => { //Function to return an entered code from the backend
  if (!window.confirm("Collect this bundle?")) return;
  const API_URL = import.meta.env.VITE_API_URL;
  const token = localStorage.getItem('token'); 

  axios.get(`${API_URL}/api/v1/reservations/collect/${claim_code}`, { //Fetches inputted tocken
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  })
    .then(response => {
      console.log("Collected:", response.data);
      alert("Bundle collected");
    })
    .catch(err => console.error(err));
};


  return (
    <>
      <div className="currentBundles">
        {/* Initialises the navifation bar where sellers can move between pages */}
          <nav className="navRow">
            <Link to="/login" className="button"><b>Login Page</b></Link>
            <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
            <Link to="/analytics" className="button"><b>Analytics</b></Link>
            <Link to="/forecasts" className="button"><b>Forecasts</b></Link>
          </nav>
          {/* Header to display the page name to the user */}
          <h1>Bundles</h1>
          {/* Section for the code input and submission button */}
          <form onSubmit={(e) => {
                  e.preventDefault();
                  enterCode(code);
                }}>
                  <input
                    id="enterCode"
                    type="text"
                    placeholder="enter code"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                  />
                  <button type="submit">Confirm Collection</button>

                </form>
                <br></br>
          {/* Columns structure for displaying bundle infomation */}
          <div className="mainBox">
            {bundles.map(bundle => ( //.map allows us to display
              <div key={bundle.posting_id} className="bundleEntry">
                {/* Contains company image and first column data */}
                <div className="displayImage">
                  <img
                    src={Company}
                    alt="Company"
                    className="companyIcon"
                  />
                </div>
                <div className="textBox">
                  <p>Price: £{bundle.price_display}</p>
                  <p>Category: {bundle.category}</p>
                  <p>Available: {bundle.available}</p>
                </div>
                {/* Holds the middle column data for the bundle entry */}
                <div className="textBox">
                  <div className="row">
                    <p>Allergens - {bundle.allergens} </p>
                    <p>Date to Collect: {bundle.formatted_date}</p>
                    <p>Time to Collect: {bundle.formatted_time_range}</p>
                    <p>Weight: {bundle.weight}</p>
                    <p>Reserved: {bundle.reserved}</p>
                    {/* Button to delete bundles on click */}
                    <button onClick={() => deleteBundle(bundle.posting_id)}>
                        Delete Bundle
                      </button>
                  </div>
                </div>
                {/* Final row bundle image */}
                <div className="displayImage">
                  <img
                    src={Bundle}
                    alt="Bundle"
                    className="companyIcon"
                  />
                </div>
            </div>
            ))}
          </div>
          {noBundles && (
          <p style={{color:"red"}}>
                      No bundles
                  </p>)}
        </div>
    </>
  );
}
//exports the component so it can be imported in other files
export default CurrentBundles;