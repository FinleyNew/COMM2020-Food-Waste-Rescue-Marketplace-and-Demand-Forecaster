import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

function AdminActionForm() {


  const API_URL = import.meta.env.VITE_API_URL;
  const [categories, setCategories] = useState([]); //store the categories
  useEffect(() => { //to get all the categories at the start so they can be used throughout
      
    axios.get(`${API_URL}/api/v1/categories/`, {
    })
    .then(response => {
       setCategories(response.data); //store them in categories
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching categories:", err);
        //alert("No data ");
    });
    },[])


  const buttonData = [
    "Update Consumer",
    "Update Seller",
    "Update Bundle",
    "Update Reservation",
    "Update Record",
    "Update User",
    "Delete Bundle",
    "Delete Forecast",
    "Delete Record",
    "Delete Reservation",
    "Delete Seller",
    "Delete Consumer",
    "Create Category",
  ];

  const [selectedAction, setSelectedAction] = useState("");
  const [category, setCategory] = useState("");
  const [userID, setUserID] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [streak, setStreak] = useState(null);
  const [bundleWeight, setBundleWeight] = useState("");
  const [bundlePrice,setBundlePrice] = useState("");
  const [bundleAllergens,setBundleAllergens] = useState("");
  const [bundleCategory, setBundleCategory] = useState("");
  const [numberAvailable, setNumberAvailable] = useState("");
  const [location, setLocation] = useState("");
  const [endTime, setEndTime] = useState("");
  const [startTime, setStartTime] = useState("");
  const [status, setStatus] = useState("");
  const [bundleID, setBundleID] = useState("");
  const [timestamp, setTimeStamp] = useState("");
  const [raining, setRaining] = useState(false);
  const [observed_reservations, setOberserved_reservations] = useState("");
  const [observed_no_show, setno_show] = useState("");
  const [observed_expired, setexpired] = useState("");
  const token = localStorage.getItem('token');
  const payload = JSON.parse(atob(token.split('.')[1]));
  const [userIdentification, setUserIdentification] = useState("");
  const today = new Date(); //need to get todays date to use to use the iso format
  const dateString = today.toISOString().split("T")[0]; // YYYY-MM-DD, removing the time to replace with the selected time
  const startDateTime = new Date(`${dateString}T${startTime}:00`); //creating new start time
  const endDateTime = new Date(`${dateString}T${endTime}:00`); //creating new end time
  const [startTimestamp, setStartTimeStamp] = useState("");
  const [endTimestamp, setEndTimeStamp] = useState("");
  
  const [openingTime, setOpeningTime] = useState("");
  const [closingTime, setClosingTime] = useState("");
  const timeRegex = /^([01]\d|2[0-3]):[0-5]\d$/;
  const toMinutes = (time) => {
    const [hours, minutes] = time.split(":").map(Number);
    return hours * 60 + minutes;
  }

  const validTimeFormat =
    timeRegex.test(openingTime) &&
    timeRegex.test(closingTime);


  const slots = Array.from({ length: 24 }, (_, i) => 
    { const start = i;
      const end = i + 1; 
      return `${String(start).padStart(2,"0")}:00 - ${String(end).padStart(2,"0")}:00`;
     });
  
    
    
  function completeAction() {


    const categoryObject = categories.find(
      cat => cat.category_id === Number(bundleCategory) //create a catgeory object to upload both the name and the id at once
    );


    if (!userID && selectedAction !== "Update User") {
    alert("Please enter a User ID");
    return;
    }
    let data ={};
    let suffix="";
    switch (selectedAction) {
      case "Update Consumer":
        suffix=`consumers/admin/${userID}`;
        if(name) data.display_name = name;
        if(streak) data.streak = streak;
        break;
      case "Update Seller":
        suffix=`sellers/admin/${userID}`;
        if(name) data.name = name;
        if(location) data.location = location;
        if(openingTime && closingTime && (toMinutes(openingTime) < toMinutes(closingTime))) data.opening_hours = `${openingTime} - ${closingTime}` //only when closing time is after
        break;
      case "Update Bundle":
        suffix=`bundles/admin/${userID}`;
        if(categoryObject) data.category = categoryObject;
        if(bundleAllergens) data.allergens = bundleAllergens;
        if(numberAvailable) data.available = Number(numberAvailable);
        if(bundlePrice) data.price = Number(bundlePrice);
        if(bundleWeight) data.weight = Number(bundleWeight);
        if(startTime) data.start_time = startDateTime.toISOString();
        if(endTime) data.end_time = endDateTime.toISOString();
        if(userIdentification) data.user_id = Number(userIdentification);
        if(status) data.status = String(status);
        console.log(data);
        break;
      case "Update Reservation":
        suffix=`reservations/admin/${userID}`;
        if(status) data.status = status;
        if(timestamp) {
          data.timestamp = new Date(timestamp).toISOString();
        } 
        break;
      case "Update Record":
        suffix=`records/admin/${userID}`;
        if(categoryObject) data.category = categoryObject;
        if(bundlePrice) data.price = Number(bundlePrice);
        if(raining) data.raining = raining;
        if(observed_reservations) data.observed_reservations = observed_reservations;
        if(observed_no_show) data.observed_no_shows = observed_no_show;
        if(observed_expired) data.observed_expired = observed_expired;
        if(bundleWeight) data.weight = Number(bundleWeight);
        if(startTimestamp) {data.start_time = new Date(startTimestamp).toISOString();}
        if(endTimestamp) {data.end_time = new Date(endTimestamp).toISOString();}

        break;
      case "Update User":
        suffix=`users/admin/${userID}`;
        if(email) data.email = email;
        if(password) data.password = password;
        break;
      
      default:
        console.log("Unknown button clicked!");
    }

    const token = localStorage.getItem('token');
    const API_URL = import.meta.env.VITE_API_URL;
    axios.patch(`${API_URL}/api/v1/${suffix}`, data ,{
      
       //Fetch data for the user
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
      .then(response => {
        //setForecasts(response.data); // data is likely an array
        //setAnalytics(response.data);
        console.log("hello");
          
        
      })
      .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching forecasts:", err);
        alert("No data");
      });
  }

  function deleteBundle(){
    const token = localStorage.getItem('token');
    const API_URL = import.meta.env.VITE_API_URL;
    console.log(API_URL);
    console.log(bundleID);
    axios.delete(`${API_URL}/api/v1/bundles/${bundleID}`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
    .catch(err => {
      console.error("FULL ERROR:", err); 
      console.error("BACKEND RESPONSE:", err.response);
      console.error("ERROR DATA:", err.response?.data);

      alert(JSON.stringify(err.response?.data, null, 2));
    });
    
  }

  function deleteFunction(){
    const token = localStorage.getItem('token');
    const API_URL = import.meta.env.VITE_API_URL;
    let suffix="";
    switch(selectedAction){
      case "Delete Forecast":
        suffix=`forecasts/${bundleID}`;
        break;
      case "Delete Record":
        suffix=`records/${bundleID}`;
        break;
      case "Delete Reservation":
        suffix=`reservations/${bundleID}`;
        break;
      case "Delete Seller":
        suffix=`sellers/${bundleID}`;
        break;
      case "Delete Consumer":
        suffix=`consumers/${bundleID}`;
        break;
      default:

    }
    
    axios.delete(`${API_URL}/api/v1/${suffix}` ,{
      
       //Fetch data for the user
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
      .then(response => {
        //setForecasts(response.data); // data is likely an array
        //setAnalytics(response.data);
        console.log("hello");
          
        
      })
      .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching forecasts:", err);
        alert("No data");
      });
  }

  function createCategory() {
    const token = localStorage.getItem('token');
    const API_URL = import.meta.env.VITE_API_URL;
    const data={
      name:category
    }
    axios.post(`${API_URL}/api/v1/categories/`, data ,{
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
    .then(() => {
      console.log("Category Added");
    })
  }

  return (
    <>
    <nav>
            <Link to="/login">Login Page</Link> |{" "}
            <Link to="/view-information">View Information</Link> | {" "}
            <Link to="/deployment-history">Deployment History</Link>
          </nav>
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", maxWidth: "500px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center" }}>Admin Actions</h1>

      <div style={{ marginTop: "20px" }}>
        {/* Dropdown */}
        <select
          value={selectedAction}
          onChange={(e) => setSelectedAction(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            fontSize: "16px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            cursor: "pointer",
          }}
        >
          <option value="">Select Action</option>
          {buttonData.map((action, idx) => (
            <option key={idx} value={action}>
              {action}
            </option>
          ))}
        </select>
      </div>

      {/* Conditional input for specific actions
      value={numberAvailable}
                    <button className="boxButton" onClick={completeAction}>Add Bundle</button> */}
      <div style={{ marginTop: "20px" }}>
        {/* UPDATING CONSUMER */}
        {selectedAction === "Update Consumer" && (
          <>
          <div className="row">
            <label htmlFor="numAvailable3">Enter UserID: </label>
            <input
              id="numAvailable3"
              type="number"
              value={userID}
              onChange={(e) => setUserID(e.target.value)}
            />
          </div>
          <br></br>
          <div className="row">
            <label htmlFor="numAvailable3">Enter Name: </label>
            <input
              id="numAvailable3"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <br></br>
          <div className="row">
            <label htmlFor="numAvailable3">Enter Streak: </label>
            <input
              id="numAvailable3"
              type="text"
              value={streak}
              onChange={(e) => setStreak(e.target.value)}
            />
          </div>
          <button className="boxButton" onClick={completeAction}>Submit</button>
          </>
        )}
        {/* UPDATE SELLER */}
        {selectedAction === "Update Seller" && (
          <>
          <div className="row">
            <label htmlFor="numAvailable3">Enter UserID: </label>
            <input
              id="numAvailable3"
              type="number"
              value={userID}
              onChange={(e) => setUserID(e.target.value)}
            />
          </div>
          <br></br>
          <div className="row">
            <label htmlFor="numAvailable3">Enter Name: </label>
            <input
              id="numAvailable3"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <br></br>
          <div className="row">
            <label htmlFor="numAvailable3">Location: </label>
            <input
              id="numAvailable3"
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>
          <div className="row">
                    <p>Opening Time : </p>
                    <input
                      type="text"
                      value={openingTime}
                      onChange={(e) => setOpeningTime(e.target.value)}
                      />
            </div>
            <div className="row">
                    <p>Closing Time : </p>
                    <input
                      type="text"
                      value={closingTime}
                      onChange={(e) => setClosingTime(e.target.value)}
                      />
            </div>
          <button className="boxButton" onClick={completeAction}>Submit</button>
          </>
        )}
        {/* UPDATE BUNDLE */}
        {selectedAction === "Update Bundle" && (
          <>
          <div className="row">
            <label htmlFor="numAvailable3">Enter Bundle ID: </label>
            <input
              id="numAvailable3"
              type="number"
              value={userID}
              onChange={(e) => setUserID(e.target.value)}
            />
          </div>
          <br></br>
          <div className="row">
                    {/* drop down for allergens */}
                     <label htmlFor="category">Enter Bundle Category : </label>
                  <select
                    name="category"
                    id="category"
                    value={bundleCategory}
                    onChange={(e) => setBundleCategory(e.target.value)}
                  >
                  {categories.map((cat) => (
                    <option key={cat.category_id} value={cat.category_id}>
                      {cat.name}
                    </option>
                  ))}
                  </select>
                  </div>


                  <div>
                <div className="row">
                  {/* Outputs an input box with a label asking for bundle allergen inputs */}
                  <label htmlFor="allergens">Enter Bundle Allergens : </label>
                  <input
                    id="allergens"
                    type="text"
                    value={bundleAllergens}
                    onChange={(e) => setBundleAllergens(e.target.value)}
                  />
                  </div>
                </div>


                  <div className="row">
                  {/* Makes an input box with a label to input the number of bundles to sell */}
                  <label htmlFor="numAvailable">Enter Number Available : </label>
                  <input
                    id="numAvailable"
                    type="number"
                    value={numberAvailable}
                    onChange={(e) => setNumberAvailable(e.target.value)}
                  />
              </div>

                  <div className="row">
                  {/* An input box with a label to input the bundle price */}
                  <label htmlFor="price">Enter Bundle Price : </label>
                  <input
                    id="price"
                    type="number"
                    value={bundlePrice}
                    onChange={(e) => setBundlePrice(e.target.value)}
                  />
                </div>

                  <div className="row">
                  {/* Outputs an input box with a label asking for bundle weight */}
                  <label htmlFor="weight">Enter Bundle Weight : </label>
                  <input
                    id="weight"
                    type="number"
                    value={bundleWeight}
                    onChange={(e) => setBundleWeight(e.target.value)}
                  />
                </div>

                  <div className="row">
                  {/* Outputs a drop down menu for the user to click a bundle collection time */}
                  <label htmlFor="collectionTime">Collection Time: </label>
                  {/* Divides the start and end time before saving them seperately */}
                  <select
                    id="collectionTime"
                    onChange={(e) => {
                      const[start,end] = e.target.value.split(" - ");
                      setStartTime(start);
                      setEndTime(end);
                    }}
                  >
                    {slots.map((slot,idx) =>(
                      <option key={idx} value={slot}>
                        {slot}
                      </option>
                    ))}
                  </select>
                    {/* Button to add bundles when clicked and forecast the data */}
                </div>

                <div className="row">
                  {/* Outputs an input box with a label asking for bundle weight */}
                  <label htmlFor="weight">Enter UserID : </label>
                  <input
                    id="weight"
                    type="number"
                    value={userIdentification}
                    onChange={(e) => setUserIdentification(e.target.value)}
                  />
                </div>

                <div className="row">
                    {/* drop down for allergens */}
                    <label htmlFor="category">Enter Bundle Status : </label>
                    <select
                      name="category"
                      id="category"
                      value={status}
                      onChange={(e) => setStatus(e.target.value)}
                    >
                    {/* List of options fo the user to choose from the menu */}
                    <option value="">Select Category</option>
                    <option value="expired">Expired</option>
                    <option value="available">Available</option>
                    <option value="sold_out">Sold Out</option>
                    <option value="reserved">Reserved</option>
                    
                    </select>
                  </div>
          <button className="boxButton" onClick={completeAction}>Submit</button>
          </>
        )}
        {/* Delete Bundle */}
        {selectedAction==="Delete Bundle" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter BundleID to delete: </label>
            <input
              id="numAvailable3"
              type="text"
              value={bundleID}
              onChange={(e) => setBundleID(e.target.value)}
            />
          </div>
          <button className="boxButton" onClick={deleteBundle}>Submit</button>
          </>
        )}
        {/* Update Reservations */}
        {selectedAction==="Update Reservation" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter Reservation ID to delete: </label>
            <input
              id="numAvailable3"
              type="number"
              value={userID}
              onChange={(e) => setUserID(e.target.value)}
            />
          </div>
          <div className="row">
                    {/* drop down for allergens */}
                    <label htmlFor="category">Enter Bundle Status : </label>
                    <select
                      name="category"
                      id="category"
                      value={status}
                      onChange={(e) => setStatus(e.target.value)}
                    >
                    {/* List of options fo the user to choose from the menu */}
                    <option value="">Select Category</option>
                    <option value="no_show">No Show</option>
                    <option value="reserved">Reserved</option>
                    <option value="collected">Collected</option>
                    
                    </select>
          </div>
          <div className="row">
            <label htmlFor="numAvailable3">Enter timestamp: </label>
            <input
              id="numAvailable3"
              type="datetime-local"
              value={timestamp}
              onChange={(e) => setTimeStamp(e.target.value)}
            />
          </div>

          <button className="boxButton" onClick={completeAction}>Submit</button>
          </>
        )}
        {/* UPDATE RECORD */}
        {selectedAction==="Update Record" && (
          <>
          <div className="row">
            <label htmlFor="numAvailable3">Enter Record ID to delete: </label>
            <input
              id="numAvailable3"
              type="number"
              value={userID}
              onChange={(e) => setUserID(e.target.value)}
            />
          </div>

           <div className="row">
            <label htmlFor="numAvailable3">Enter price: </label>
            <input
              id="numAvailable3"
              type="number"
              value={bundlePrice}
              onChange={(e) => setBundlePrice(e.target.value)}
            />
          </div>

           <div className="row">
            <label htmlFor="numAvailable3">Enter raining ( true, false): </label>
            <input
              id="numAvailable3"
              type="text"
              value={raining}
              onChange={(e) => setRaining(e.target.value)}
            />
          </div>
           <div className="row">
            <label htmlFor="numAvailable3">Enter observed reservations: </label>
            <input
              id="numAvailable3"
              type="text"
              value={observed_reservations}
              onChange={(e) => setOberserved_reservations(e.target.value)}
            />
          </div>
           <div className="row">
            <label htmlFor="numAvailable3">Enter observed no shows: </label>
            <input
              id="numAvailable3"
              type="text"
              value={observed_no_show}
              onChange={(e) => setno_show(e.target.value)}
            />
          </div>
           <div className="row">
            <label htmlFor="numAvailable3">Enter observed expieres: </label>
            <input
              id="numAvailable3"
              type="text"
              value={observed_expired}
              onChange={(e) => setexpired(e.target.value)}
            />
          </div>
          <div className="row">
            <label htmlFor="numAvailable3">Enter weight: </label>
            <input
              id="numAvailable3"
              type="number"
              value={bundleWeight}
              onChange={(e) => setBundleWeight(e.target.value)}
            />
          </div>
          <div className="row">
                    <p>Start Time : </p>
                    <input
                      type="datetime-local"
                      value={startTimestamp}
                      onChange={(e) => setStartTimeStamp(e.target.value)}
                      />
            </div>
            <div className="row">
                    <p>End Time : </p>
                    <input
                      type="datetime-local"
                      value={endTimestamp}
                      onChange={(e) => setEndTimeStamp(e.target.value)}
                      />
            </div>
            <button className="boxButton" onClick={completeAction}>Submit</button>
          
          </>
        )}
        {/* Update User */}
        {selectedAction==="Update User" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter UserID to update: </label>
            <input
              id="numAvailable3"
              type="number"
              value={userID}
              onChange={(e) => setUserID(e.target.value)}
            />
          </div>
          
          <div className="row">
            <label htmlFor="numAvailable3">Enter email: </label>
            <input
              id="numAvailable3"
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="row">
            <label htmlFor="numAvailable3">Enter password: </label>
            <input
              id="numAvailable3"
              type="text"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="boxButton" onClick={completeAction}>Submit</button>
          </>
        )}
        {/* Delete Forecast */}
        {selectedAction==="Delete Forecast" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter ForecastID to delete: </label>
            <input
              id="numAvailable3"
              type="text"
              value={bundleID}
              onChange={(e) => setBundleID(e.target.value)}
            />
          </div>
          <button className="boxButton" onClick={deleteFunction}>Submit</button>
          </>
        )}
        {/* Delete Record */}
        {selectedAction==="Delete Record" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter RecordID to delete: </label>
            <input
              id="numAvailable3"
              type="text"
              value={bundleID}
              onChange={(e) => setBundleID(e.target.value)}
            />
          </div>
          <button className="boxButton" onClick={deleteFunction}>Submit</button>
          </>
        )}
        {/* Delete Reservation */}
        {selectedAction==="Delete Reservation" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter ReservationID to delete: </label>
            <input
              id="numAvailable3"
              type="text"
              value={bundleID}
              onChange={(e) => setBundleID(e.target.value)}
            />
          </div>
          <button className="boxButton" onClick={deleteFunction}>Submit</button>
          </>
        )}
        {/* Delete Seller */}
        {selectedAction==="Delete Seller" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter UserID to delete: </label>
            <input
              id="numAvailable3"
              type="text"
              value={bundleID}
              onChange={(e) => setBundleID(e.target.value)}
            />
          </div>
          <button className="boxButton" onClick={deleteFunction}>Submit</button>
          </>
        )}
        {/* Delete Consumer */}
        {selectedAction==="Delete Consumer" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter UserID to delete: </label>
            <input
              id="numAvailable3"
              type="text"
              value={bundleID}
              onChange={(e) => setBundleID(e.target.value)}
            />
          </div>
          <button className="boxButton" onClick={deleteFunction}>Submit</button>
          </>
        )}
        {/* Create Category */}
        {selectedAction==="Create Category" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter category name to add: </label>
            <input
              id="numAvailable3"
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            />
          </div>
          <button className="boxButton" onClick={createCategory}>Submit</button>
          </>
        )}
      </div>
    </div>
    </>
  );
}

export default AdminActionForm;