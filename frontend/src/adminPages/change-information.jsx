import { Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import './change-information.css'

function AdminActionForm() {


  const API_URL = import.meta.env.VITE_API_URL; 
  const [categories, setCategories] = useState([]); //store the categories
  useEffect(() => { //to get all the categories at the start so they can be used throughout
      
    axios.get(`${API_URL}/api/v1/categories/`, { //get request using the API URL variable, used to switch allow local use and deployed use
    })
    .then(response => {
       setCategories(response.data); //store them in categories variable declared above
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching categories:", err);
        //alert("No data ");
    });
    },[])


  const buttonData = [ //all of the options that the admin can pick to change
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
    "Delete Issue Report",
    "Create Category",
    "Create Admin",
  ];
  //all of the variables used to store the data gathered by the get requests
  const [reportID, setReportID] = useState("");
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
  const [description, setDescription] = useState("");
  
  const [status, setStatus] = useState("");
  const [bundleID, setBundleID] = useState("");
  const [timestamp, setTimeStamp] = useState("");
  const [raining, setRaining] = useState(false);
  const [observed_reservations, setOberserved_reservations] = useState("");
  const [observed_no_show, setno_show] = useState("");
  const [observed_expired, setexpired] = useState("");
  const token = localStorage.getItem('token');
  //
  
  const [userIdentification, setUserIdentification] = useState("");
  const today = new Date(); //need to get todays date to use to use the iso format
  const dateString = today.toISOString().split("T")[0]; // YYYY-MM-DD, removing the time to replace with the selected time
  const startDateTime = new Date(`${dateString}T${startTime}:00`); //creating new start time
  const endDateTime = new Date(`${dateString}T${endTime}:00`); //creating new end time
  const [startTimestamp, setStartTimeStamp] = useState("");
  const [endTimestamp, setEndTimeStamp] = useState("");
  //the regex is used to make sure the input matches a specific form
  const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/; //this regex makes sure the email has an @ symbol and a domain name (.com)
  const [openingTime, setOpeningTime] = useState("");
  const [closingTime, setClosingTime] = useState("");
  const timeRegex = /^([01]\d|2[0-3]):[0-5]\d$/; //this regex makes sure the time is in a format of HH:MM
  const toMinutes = (time) => { //converts to a number that we can compare to other times, to make sure the closing time is bigger than the opening time
    const [hours, minutes] = time.split(":").map(Number);
    return hours * 60 + minutes;
  }

  const validTimeFormat = //checks the times are in the correct time format (HH:MM)
    timeRegex.test(openingTime) &&
    timeRegex.test(closingTime);


  const slots = Array.from({ length: 24 }, (_, i) => 
    { const start = i;
      const end = i + 1; 
      return `${String(start).padStart(2,"0")}:00 - ${String(end).padStart(2,"0")}:00`;
     }); //creates all the slots for picking the time of the bundle
  
    
    
  function completeAction() {


    const categoryObject = categories.find(
      cat => cat.category_id === Number(bundleCategory) //create a catgeory object to upload both the name and the id at once
    ); //as the backend requires an object for the category with a category name and index, we have to build an object to parse
    //to the backend


    if (!userID && selectedAction !== "Update User") { //makes sure an ID and an action are entered
    alert("Please enter a valid ID"); //if not alert the admin that they havent been entered
    return;
    }
    let data ={};
    let suffix=""; //a suffix variable, this makes sure that we cna build the request by adding the specific path to the end to save space
    switch (selectedAction) { //each case is the same but with different variables that the request needs and the suffix is different
      case "Update Consumer":
        suffix=`consumers/admin/${userID}`;
        if(name) data.display_name = name; //update consumer needs display name and the streak to update
        if(streak) data.streak = streak;
        break;
      case "Update Seller":
        suffix=`sellers/admin/${userID}`; //updating the seller requires a name, location and opening hours
        if(name) data.name = name;
        if(location) data.location = location;
        //the opening and closing time allows for a user to enter both, then builds one variable which the backend requires
        if(openingTime && closingTime && (toMinutes(openingTime) < toMinutes(closingTime))) data.opening_hours = `${openingTime} - ${closingTime}` //only when closing time is after
        break;
      case "Update Bundle": //updating the bundle 
        suffix=`bundles/admin/${userID}`; //the if statements allow certain elements to be changed if they exist, so not all elements
        if(categoryObject) data.category = categoryObject; //have to be present for the object to update, the same for all cases
        if(bundleAllergens) data.allergens = bundleAllergens;
        if(numberAvailable) data.available = Number(numberAvailable);
        if(bundlePrice) data.price = Number(bundlePrice);
        if(bundleWeight) data.weight = Number(bundleWeight);
        if(startTime) data.start_time = startDateTime.toISOString();
        if(endTime) data.end_time = endDateTime.toISOString();
        if(userIdentification) data.user_id = Number(userIdentification);
        if(status) data.status = String(status);
        
        break;
      case "Update Reservation": //updating reservation requires the status of the bundle and a timestamp
        suffix=`reservations/admin/${userID}`;
        if(status) data.status = status;
        if(timestamp) {
          data.timestamp = new Date(timestamp).toISOString();
        } 
        break;
      case "Update Record": //updating record
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
      case "Update User": //updating user
        suffix=`users/admin/${userID}`;
        if(email) data.email = email;
        if(password) data.password = password;
        break;
      
      default:
        console.log("Unknown button clicked!");
    }

    const token = localStorage.getItem('token'); //the token retrieves the locally stored token from when the user logs in
    //this verifies the user and allows them to access the correct data
    const API_URL = import.meta.env.VITE_API_URL; //the API_URL variable stores the URL based on if the website is accessed locally or deployed
    axios.patch(`${API_URL}/api/v1/${suffix}`, data ,{  //a patch request updates data with the data variable that was build in the switch case
      
       //Fetch data for the user
      headers: {
        "Authorization": `Bearer ${token}`, //headers allow the token and content type to be sent to the backend to verify and access the data
        "Content-Type": "application/json"
      }
    })
      .then(response => { //console log to confirm information has been changed
        
        console.log("Information Changed");
          
        
      })
      .catch(err => { //Returns alert if an error occurs
        console.error("Error changing information:", err);
        alert("No data"); //display any errors to the user and the logs
      });
  }

  function deleteBundle(){ //function to delete a bundle
    const token = localStorage.getItem('token');
    const API_URL = import.meta.env.VITE_API_URL;
    console.log(API_URL);
    
    axios.delete(`${API_URL}/api/v1/bundles/${bundleID}`, { //delete request to delete the bundle in the backend
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
    .catch(err => {
      
      console.error("Backend Response:", err.response);
      console.error("Error:", err.response?.data); //display any erorrs

      
    });
    
  }

  function deleteFunction(){ //function for the other delete forms
    const token = localStorage.getItem('token');
    const API_URL = import.meta.env.VITE_API_URL;
    let suffix=""; //similar to the update switches with the suffix
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
      case "Delete Issue Report":
        suffix=`reports/${bundleID}`;
        break;
      default:
        break;

    }
    
    axios.delete(`${API_URL}/api/v1/${suffix}` ,{ //same delete function with the same headers and content type for the backend to verify
      
       //Fetch data for the user
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
      .then(response => {
        
        console.log("Deleted"); //log the object has been deleted
          
        
      })
      .catch(err => {
           console.log("status:", err.response?.status);
           console.log("backend error:", err.response?.data);
      });
  }

  function createCategory() { //create category function
    const token = localStorage.getItem('token');
    const API_URL = import.meta.env.VITE_API_URL;
    const data={
      name:category //creating a cetegory only needs the name of the new category
    }
    axios.post(`${API_URL}/api/v1/categories/`, data ,{
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json" //same headers
      }
    })
    .then(() => {
      console.log("Category Added"); //output
    })
    .catch(err => {
           console.log("status:", err.response?.status);
           console.log("backend error:", err.response?.data);
      }); //display any errors
  }

  function createAdmin() { //creating a new admin
    const token = localStorage.getItem('token');
    const API_URL = import.meta.env.VITE_API_URL;
    const data={
      email:email,
      password:password, //requires an email and passowrd
    };
    console.log(data);
    axios.post(`${API_URL}/api/v1/admins/`, data ,{
      headers: {
        "Authorization": `Bearer ${token}`, //same headers
        "Content-Type": "application/json"
      }
    })
    .then(() => {
      console.log("Admin Added"); //console log to display if admin has been created
    })
    .catch(err => {
           console.log("status:", err.response?.status); //error catching
           console.log("backend error:", err.response?.data);
      });
  }

  return ( //all html for displaying the form selection and enter boxes
    <>
    <div className="change">
      <nav className="navRow">
        <Link to="/view-information" className="button">View Information</Link>
        <Link to="/view-tests" className="button">View Tests</Link> {/* navigation links to the other pages */}
      </nav>
      <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", maxWidth: "500px", margin: "0 auto" }}>
        <h1 className="header">Admin Actions</h1> {/* Heading */}

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
            }} //defining the style of the select element
          >
            <option value="">Select Action</option>
            {buttonData.map((action, idx) => (
              <option key={idx} value={action}> {/* Display all the drop down choices using the array holding all the choices */}
                {action}
              </option>
            ))}
          </select>
        </div>
        <br></br>

        {/* Conditional input for specific actions
        value={numberAvailable}
                      <button className="boxButton" onClick={completeAction}>Add Bundle</button> */}
        <div className="container">
          {/* UPDATING CONSUMER */}
          {selectedAction === "Update Consumer" && ( //every choice has its own selected action check and then a varying number of inputs
            <> {/* dependent on what the backend requires to change the information */}
            <div className="row">
              <label htmlFor="numAvailable3">Enter UserID: </label> {/* each div holds an input */}
              <input
                id="numAvailable3"
                type="number"
                value={userID} // each ID is stored as userID, this means we can use it in the switch statement
                onChange={(e) => setUserID(e.target.value)}
              />
            </div>
              <label htmlFor="numAvailable3">Enter Name: </label>
              <input
                id="numAvailable3"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            <div className="setRow">
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
          <div>
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
          <div className="setRow">
                    <p>Start Time : </p>
                    <input
                      type="datetime-local"
                      value={startTimestamp}
                      onChange={(e) => setStartTimeStamp(e.target.value)}
                      />
            </div>
            <div className="setRow">
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
            <div className="row">
              <label htmlFor="numAvailable3">Enter Name: </label>
              <input
                id="numAvailable3"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="row">
              <label htmlFor="numAvailable3">Location: </label>
              <input
                id="numAvailable3"
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              />
            </div>
            <div className="setRow">
              <p>Opening Time : </p>
              <input
                type="text"
                value={openingTime}
                onChange={(e) => setOpeningTime(e.target.value)}
                />
            </div>
            <div className="setRow">
              <p>Closing Time : </p>
              <input
                type="text"
                value={closingTime}
                onChange={(e) => setClosingTime(e.target.value)}
                />
            </div>
            <br></br>
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
            <div className="row">
              {/* drop down for allergens */}
              <label htmlFor="category">Enter Bundle Category : </label>
              <select
                name="category"
                id="category"
                value={bundleCategory}
                onChange={(e) => setBundleCategory(e.target.value)}
              >
              {/* List of options fo the user to choose from the menu */}
              <option value="">Select Category</option>
              <option value="Baked Goods">Baked Goods</option>
              <option value="Fruit">Fruit</option>
              <option value="Vegetables">Vegetables</option>
              <option value="Meat">Meat</option>
              <option value="Seafood">Seafood</option>
              <option value="Snacks">Snacks</option>
              <option value="Dairy">Dairy</option>
              <option value="Drinks">Drinks</option>
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
        </div>
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
        {/* Delete Issue Report */}
        {selectedAction==="Delete Issue Report" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter IssueID to delete: </label>
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
        {selectedAction==="Create Admin" && (
          <>
            <div className="row">
            <label htmlFor="numAvailable3">Enter admin email: </label>
            <input
              id="numAvailable3"
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="row">
            <label htmlFor="numAvailable3">Enter admin password: </label>
            <input
              id="numAvailable3"
              type="text"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {email && !emailRegex.test(email) && (
            <p style={{color: "red"}}>Email must contain @ and contain a domain name</p>
          )} 
          <button className="boxButton" onClick={createAdmin}>Submit</button>
          </>
        )}
      </div>
    </div>
    </>
  );
}

export default AdminActionForm;