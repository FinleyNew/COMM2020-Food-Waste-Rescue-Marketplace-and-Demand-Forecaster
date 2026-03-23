import { Link, useNavigate, useParams } from "react-router-dom"; //to use the buttons to change to other pages
import { useState, useEffect } from "react"; //to use the fetch, to make sure it only fetches once
import './Discover.css' //links to the css page to move and size different components around
import Company from "../assets/Company.png";
import Bundle from "../assets/BundleImage.png"; //here for the base images
import axios from "axios";
function BundleSelect() {
  const navigate = useNavigate();
  const { id } = useParams(); //creates the ID variable to store the bundleID to navigate pages with it

  const [bundle, setBundle] = useState(null); //bundle is used to hold the data, setBundle is used to store it
  const [Popup, setPopup] = useState(false);
  const [reportButton, setReportButton] = useState(false);
  const [viewReport, setViewReportButton] = useState(false);
  const [showReports, setShowReports] = useState([]);
  const [report, setReport] = useState("");
  const API_URL = import.meta.env.VITE_API_URL;
  function openPopup() {
    setPopup(true); //if variable is true then popUp needs to be opened 
  }

  function closePopup() {
    setPopup(false); //if variable is false then popUp needs to be closed
  }





  useEffect(() => { //useEffect allows the command run on entering the page and if anything happens inside ID
    axios.get(`${API_URL}/api/v1/bundles/${id}`,{ //links to the backend page on the API with the specific bundle of ID
    })
    .then(response => {
      setBundle(response.data); //axios stores the JSON in response.data
    })
    .catch(err => console.error(err)); //catches and displays any errors
  }, [id]) //this part means if ID changes the page reloades with the new information


  if (!bundle) return <p>Loading bundle...</p>;


  function createReservation(postingID){ //this function takes place if the user "pays" for a bundle
    const token = localStorage.getItem(`token`); //gets the users token, for security and to make sure the site gets THEIR information
    const payload = JSON.parse(atob(token.split('.')[1])); //gets the exact payload from the token, rather than the bundle information, more accurate, the split gets the ...
    const userID = parseInt(payload.sub); // ... part that contains the userID then using sub gets the userID
    const API_URL = import.meta.env.VITE_API_URL;
    const data={
      posting_id:postingID,
      user_id:userID
    };
    
    axios.post(`${API_URL}/api/v1/reservations/`, data, {
      headers: { //extra data we are sending to the backend
        "Authorization": `Bearer ${token}`, //verifies the users as who they are and their token
        "Content-Type": "application/json" //telling the backend we are explicity sending JSON data
      },
    })
      .then(response => {
      setBundles(response.data); // Update state with search results
    })
    .catch(err => {
      console.error("Error searching bundles:", err);
      setBundles([]); // Clear bundles if search fails
    });
    
  }




  function createReport() {
    const data={
      posting_id:id,
      description:report,
    }
    console.log(data);
    const token = localStorage.getItem(`token`);
    axios.post(`${API_URL}/api/v1/reports/`, data ,{
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    
  }
  function closeReportPopup() {
    setReportButton(false);
  }

  function handleViewReports() {
  const token = localStorage.getItem('token');
  const API_URL = import.meta.env.VITE_API_URL;

  axios.get(`${API_URL}/api/v1/reports/consumer/${id}`, {  
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  })                                                      
  .then(response => {
    console.log("response created");
    setShowReports(response.data);
  });
}

  return (
    <>
      <div className="discover">
        <div className="pageHeading">
          <nav className="navBundleRow">
            <Link to="/discover" className="button"><b>Discover</b></Link> {/*This section holds all the links to the other pages*/}
            <Link to="/streaks" className="button"><b>Streaks</b></Link>
            <Link to="/codes" className="button"><b>Codes</b></Link>
          </nav>
          <div className="textHeading">
            <h1>Bundles</h1> {/* header for the bundles page */}
          </div>
      </div>

        <section>
          <div className="mainBox">
            <div className="bundleEntry"> {/* the start for each bundle and inside this div holds all the info for the bundle */}
              <img
                src={Bundle}
                alt="Bundle"
                className="rowImg"
              />{/* holds the base company image */}
              <div className="textBox">
                <div className="bundleRow">
                  <h1>{bundle.seller.name}</h1>
                  <img
                      src={bundle.seller.logo_url}
                      alt="Company"
                      className="companyIcon" //holds the specific bundle image
                    />
                </div>
                <div className="bundleRow">
                  <div className="column">
                    <p>Category: {bundle.category.name}</p> {/* displays the category, allergens and prices */}
                    <p>Contents: {bundle.contents}</p>
                    <p>Pickup Location: {bundle.seller.location}</p>
                    <p>Pickup Date: {bundle.formatted_date}</p>
                    <p>Price: £{bundle.price}</p>
                  </div>
                  <div className="column">
                    <p>Date to Collect: {bundle.formatted_date}</p> {/* displays the formatted date and the time range */}
                    <p>Time to Collect: {bundle.formatted_time_range}</p>
                    <p>{bundle.discount_percent}% off original price</p>
                    <p>Allergens: {bundle.allergens}</p>
                  </div>
                </div>
                <br></br>
              </div>
              <div className="centerAlign">
                <button className="payButton" onClick={() => (openPopup(),createReservation(bundle.posting_id))}> {/* if the pay button is clicked it sends the information to the create reservation page */}
                  Pay
                </button>
                <Link to="/discover" className="payButton">Back</Link>
                <button className="payButton" onClick={() => (setReportButton(true))}>Create Report</button>
                <button className="payButton" onClick={() => (handleViewReports(),setViewReportButton(true))}>View Reports</button>


              </div>
              {Popup && (
                <div className="popup open-popup" id="payment">
                  <h1>Payment Successful!</h1>  {/*if the button is clicked, open the pop up to pay*/}
                  <button className="button" onClick={() => (closePopup,navigate("/discover"))}>Confirm</button>
                </div>
              )}
              {reportButton && (
                <div className="popup open-popup">
                  <div className="textBox">
                    <h1>Please enter the issue to send to the seller.</h1>
                    <div className="row">
                    {/* Outputs an input box with a label asking for bundle allergen inputs */}
                    <label htmlFor="report">Enter Issue : </label>
                    <input
                      id="report"
                      type="text"
                      value={report}
                      onChange={(e) => setReport(e.target.value)}
                    />
                    <br></br>
                    <br></br>
                    <button className="button" onClick={() => (createReport(), closeReportPopup())}>Confirm</button>
                  </div>
                </div>
                   {/* {setReportButton(false)} close after report is made */}
                </div>
              )}
              {viewReport && (
                <div className="popup open-popup">
                  <h1>View Reports</h1>
                    <div className="textBox">
                      {showReports.length === 0 ? (
                        <p>No reports found</p>
                      ) : (
                      <div className="reportsFormat">
                        {showReports.map((report) => (
                          <>
                            <h1>Description: {report.description}</h1>
                            <h1>Seller Response: {report.seller_response}</h1>
                            <h1>Status: {report.status}</h1>
                          </>
                        ))}
                      </div>
                      )}
                      <button className="button" onClick={() => setViewReportButton(false)}>Close</button>
                    </div>
                </div>
              )}
            </div>
          </div>
        </section>
      </div>
    </>
  );
}

export default BundleSelect; //exports the component so it can be imported in other files
