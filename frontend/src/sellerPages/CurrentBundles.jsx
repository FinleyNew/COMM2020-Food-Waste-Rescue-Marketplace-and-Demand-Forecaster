import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import './CurrentBundles.css'
import Company from "../assets/Company.png";
import Bundle from "../assets/BundleImage.png";
function CurrentBundles() {
  
  const [bundles, setBundles] = useState([]); //create state
  const [code, setCode] = useState("");

  const navigate = useNavigate();
  useEffect(() => {
    const token = localStorage.getItem('token');
    fetch("http://127.0.0.1:8000/api/v1/bundles/me",{ //Fetch data for the user
      headers:{
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    }) //fetch here , useeffect means it only fetches once
      .then(res => res.json())
      .then(data => {
        console.log("API DATA:", data); 
        setBundles(data);
      })
      .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        alert("No data ");
      });
  }, []);
  const deleteBundle = (posting_id) => { //Function to delete bundles from backend
    if (!window.confirm("Delete this bundle?")) return;

    fetch(`http://127.0.0.1:8000/api/v1/bundles/${posting_id}`, {
    method: "GET"
    })
    .then(res => res.json())
    .then(data => {
      console.log("Deleted:", data);
      alert("Bundle deleted");
    })
    
    .catch(err => console.error(err));
};

const enterCode = (claim_code) => { //Function to return an entered code from the backend
  if (!window.confirm("Collect this bundle?")) return;

  const token = localStorage.getItem('token'); 

  fetch(`http://127.0.0.1:8000/api/v1/reservations/collect/${claim_code}`, { //Fetches inputted tocken
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  })
    .then(res => res.json())
    .then(data => {
      console.log("Collected:", data);
      alert("Bundle collected");
    })
    .catch(err => console.error(err));
};


  return (
    <>
      <div className="currentBundles">
        {/* Initialises the navifation bar where sellers can move between pages */}
          <nav className="row">
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
                <div className="textBox">
                  <img
                    src={Company}
                    alt="Company"
                    className="companyIcon"
                  />
                  <div className="row">
                    <p>Price: £{bundle.price_display}</p>
                    <p>Category: {bundle.category}</p>
                    <p>Available: {bundle.available}</p>
                  </div>
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
                <div className="textBox">
                  <div className="row">
                    <img
                      src={Bundle}
                      alt="Bundle"
                      className="companyIcon"
                    />
                  </div>
                </div>
            </div>
            ))}
          </div>
        </div>
    </>
  );
}
//exports the component so it can be imported in other files
export default CurrentBundles;