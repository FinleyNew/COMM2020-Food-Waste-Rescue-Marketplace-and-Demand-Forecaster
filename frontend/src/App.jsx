import { useState, useEffect } from "react"; //importing state so we can use it to change the state of the react page when anything changes
import { Routes, Route, Link, Navigate, useNavigate } from "react-router-dom"; //needs to be imported so we can add routes between pages
import ProtectedRoute from "./pages/ProtectedRoute"; //to use protected routes, so that consumers cannot enter seller pages and vice versa
//import './App.css'
import "./index.css"
import SettingsIcon from "./assets/SettingsIcon.png";
// Pages (ensure the file names match exactly)
import Discover from "./consumerPages/Discover"; //every import allows a page to be accessed via the url from another page
import BundleSelect from "./consumerPages/bundle-select";
import Streaks from "./consumerPages/Streaks";
import Codes from "./consumerPages/Codes";
import LoginPage from "./pages/loginPage";
import AddBundles from "./sellerPages/AddBundles";
import Analytics from "./sellerPages/Analytics";
import CurrentBundles from "./sellerPages/CurrentBundles";
import Forecasts from "./sellerPages/Forecasts";
import DeploymentHistory from "./adminPages/DeploymentHistory";
import View_information from "./adminPages/view-information";
import Change_information from "./adminPages/change-information";
import HomePage from "./pages/HomePage";
import Unauthorised from "./pages/unauthorised";
import axios from "axios";

//|{" "}

function App() {


  const [user, setUser] = useState(() => { //user = current state, setuser = function to update user and role later,  useState is a hook to remebember data across re-renders
  const savedUser = localStorage.getItem("user"); //reads from local storage under the key of user
  return savedUser ? JSON.parse(savedUser) : null; //if thertes something in local storage, if yes the parse converts back to a js object
  });
  const storedUser = user;
  const username = user?.username;
  const role = user?.role;
  console.log("user:", user);
  console.log("username:", username);
  console.log("role:", role);

  const [settingsPopup, settingsSetPopup] = useState(false);
  const[darkMode, setDarkMode] = useState(false); //store the variable for the current state
  //const username = localStorage.getItem('username');
  //const role = localStorage.getItem('role');
  const [LSLocation,setLSLocation] = useState(localStorage.getItem('location'));
  const LScompanyName = localStorage.getItem('companyName');
  const LSopeningHours = localStorage.getItem('openingHours');
  const [updateDetails, setUpdateDetails] = useState(false);
  const [displayName, setDisplayName] = useState("");
  const [location, setLocation] = useState("");
  let  correctRole = "";
  const [companyName, setCompanyName] = useState("");

  const [openingTime, setOpeningTime] = useState("");
  const [closingTime, setClosingTime] = useState("");
  const [sellerData, setSellerData] = useState(null);
  const timeRegex = /^([01]\d|2[0-3]):[0-5]\d$/;

  
  const toMinutes = (time) => {
    const [hours, minutes] = time.split(":").map(Number);
    return hours * 60 + minutes;
  }

  const validTimeFormat =
    timeRegex.test(openingTime) &&
    timeRegex.test(closingTime);

  const timeValidForSeller = 
  
    validTimeFormat && toMinutes(closingTime) > toMinutes(openingTime)
    

  
  const validTime =
    timeRegex.test(openingTime) &&
    timeRegex.test(closingTime) &&
    toMinutes(closingTime) > toMinutes(openingTime);
  
    const invalidTime =
    validTimeFormat &&
    toMinutes(closingTime) <= toMinutes(openingTime);



  const API_URL = import.meta.env.VITE_API_URL;
  useEffect(() => { //update the page if the theme is changed
    const savedTheme = localStorage.getItem("theme"); //store the theme in local storage

    if(savedTheme === "dark"){
      setDarkMode(true); //if dark mode is selected change the theme
      document.documentElement.classList.add("dark");
    }
  },[]);

  const logOut = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    localStorage.removeItem("location");
    setUser(null);
    setSellerData(null);
    setLSLocation(null);
    settingsClosePopup();
    navigate("/login");
  }

  const toggleDarkMode = () => { //function for turning dark mode on
    if(darkMode){ //if dark mode is selected (return back to light)
      document.documentElement.classList.remove("dark"); //adds dark to the html tag
      localStorage.setItem("theme","light"); //set theme to light
    } else {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme","dark"); //set theme to dark
    }
    setDarkMode(!darkMode)
  }

  
  function settingsClickPopup() {
    settingsSetPopup(!settingsPopup); //if variable is true then popUp needs to be opened 
  }

  function settingsClosePopup() {
    settingsSetPopup(false); //if variable is false then popUp needs to be closed
  }
  function deleteAccount(){
    let correctRole;
    console.log("role from state:", role);
  console.log("user from localStorage:", localStorage.getItem("user"));
      if(role=="seller"){
        correctRole = "sellers";
      }
      else if(role=="consumer"){
        correctRole="consumers"
      }
      const token = localStorage.getItem('token');
      console.log(token);
      if (!window.confirm("Delete account?")) return;
      console.log(role);
    axios.delete(`${API_URL}/api/v1/${correctRole}/me`, {
      headers : {
        "Authorization": `Bearer ${token}`
      }
    })
    .then(response => {
      console.log("Deleted:", response.data);
      alert("Account");
      localStorage.removeItem("user");
      localStorage.removeItem("token");
      setUser(null);
      const navigate = useNavigate();
      navigate("/login");
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error:", err.response?.data);
        
    });
    
  }

  
    //to show in the settings menu
    useEffect(() => {
      const token = localStorage.getItem('token');
    axios.get(`${API_URL}/api/v1/sellers/me`, {
      headers : {
        "Authorization": `Bearer ${token}`
      }
    })
    .then(response => {
       setSellerData(response.data);
    })
    .catch(err => { //Returns alert if an error occurs
        console.error("Error fetching bundles:", err);
        //alert("No data ");
    });
    },[role])
  


  function handleUpdateDetails() {
    //open a pop up then chance email or username, and password?
    setUpdateDetails(true);
  }

  function completeUpdatedDetails() {
    const token = localStorage.getItem('token');
    const data={};
    if(companyName) data.name = companyName;
    if(location) data.location = location;
    if(openingTime && closingTime) data.opening_hours = `${openingTime} - ${closingTime}`
    console.log(data);
  axios.patch(`${API_URL}/api/v1/sellers/me`,data, 
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )
  .then(res => {
    console.log("Updated:", res.data);
    alert("Details updated successfully");
    localStorage.setItem("location",location);
    setLSLocation(location);
    setUpdateDetails(false); // close form
  })
  .catch(err => {
    console.error("Update failed:", err.response?.data || err.message);
    alert("Failed to update details");
  });
  window.location.reload();
  }
    
  

  return (
    <>
      
        <Routes>
        
        <Route path="/login" element={<LoginPage setUser={setUser} />} />

        <Route path="/discover" element={<ProtectedRoute user={user} requireRole="consumer"><Discover /></ProtectedRoute>} /> {/* protected route only allows a user with the correct type to access that page */}
        <Route path="/bundle-select" element={<ProtectedRoute user={user} requireRole="consumer"><BundleSelect /></ProtectedRoute>} />
        <Route path="/streaks" element={<ProtectedRoute user={user} requireRole="consumer"><Streaks /></ProtectedRoute>} />
        <Route path="/codes" element={<ProtectedRoute user={user} requireRole="consumer"><Codes /></ProtectedRoute>} />

        <Route path="/add-bundles" element={<ProtectedRoute user={user} requireRole="seller"><AddBundles /></ProtectedRoute>} />
        <Route path="/analytics" element={<ProtectedRoute user={user} requireRole="seller"><Analytics /></ProtectedRoute>} />
        <Route path="/current-bundles" element={<ProtectedRoute user={user} requireRole="seller"><CurrentBundles /></ProtectedRoute>} />
        <Route path="/forecasts" element={<ProtectedRoute user={user} requireRole="seller"><Forecasts /></ProtectedRoute>} />



        <Route path="/deployment-history" element={<ProtectedRoute user={user} requireRole="admin"><DeploymentHistory /></ProtectedRoute>} />
        <Route path="/view-information" element={<ProtectedRoute user={user} requireRole="admin"><View_information /></ProtectedRoute>} />
        <Route path="/change-information" element={<ProtectedRoute user={user} requireRole="admin"><Change_information /></ProtectedRoute>} />


        <Route path="/" element={<HomePage />} /> {/* these pages are accessible by everybody */}
        <Route path="/unauthorised" element={<Unauthorised />} />
        <Route path="/bundle/:id" element={<BundleSelect />} />
        
        
      </Routes>
      <button className="dark-mode-btn" onClick={settingsClickPopup}>
        <img src={SettingsIcon} className="settingsIcon" alt="Settings"></img>
      </button>
      {settingsPopup && (
        <div className="settingsPopup settingsOpenPopup">
          {!user || location.pathname === "/login" ? (
          <div>
            <h1>Please login to an account to access settings</h1>
            <input
              type="checkbox"
              id="darkModeToggle"
              checked={darkMode}
              onChange={toggleDarkMode}
            />
            <label htmlFor="darkModeToggle">
              {darkMode ? "Dark Mode" : "Light Mode"}
            </label> 
            </div>) : (
            <>
              <h1>Settings</h1>
              <p>Account Details:</p>
              <div className="settingsTextBox">
                <p>Email: {username}</p>
                <p>Account Type: {role}</p>
                {role === "seller" && (
                  <>
                  <p>Company Name: {sellerData?.name}</p>
                  <p>Location: {sellerData?.location}</p>
                  <p>Opening Hours: {sellerData?.opening_hours}</p>
                  </>
                )}
              </div>
              <Link to="/login" className="signOutButton" onClick={() => logOut()}><b>Sign Out</b></Link>
              <br></br>
              <h3>Accessibility:</h3>
              <div className="settingsRow">
                <input
                  type="checkbox"
                  id="darkModeToggle"
                  checked={darkMode}
                  onChange={toggleDarkMode}
                />
                <label htmlFor="darkModeToggle">
                  {darkMode ? "Dark Mode" : "Light Mode"}
                </label>
              </div>
              <br></br>
              <h3>Change Details</h3>
              <button onClick={deleteAccount}>Delete Account</button>
              <br></br>
              {role==="seller" && (
                <button onClick={handleUpdateDetails}>Update Details</button>
              )}
              {updateDetails===true && (
                <>
                    <div className="rowRegister">
                    <p>Company Name: </p>
                    <input
                      type="text"
                      value={companyName}
                      onChange={(e) => setCompanyName(e.target.value)}
                      />
                  </div>
                    <div className="rowRegister">
                    <p>Location: </p>
                    <input
                      type="text"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                      />
                      <h3>Times must be in the format HH:MM</h3>
                  </div>
                  <div className="rowRegister">
                    <p>Opening Time : </p>
                    <input
                      type="text"
                      value={openingTime}
                      onChange={(e) => setOpeningTime(e.target.value)}
                      />
                  </div>
                  <div className="rowRegister">
                    <p>Closing Time : </p>
                    <input
                      type="text"
                      value={closingTime}
                      onChange={(e) => setClosingTime(e.target.value)}
                      />
                  </div>
                  <br></br>
                  <button onClick={completeUpdatedDetails} //was close popup
                              
                              >Update Details</button>
                    </>
              )}
              
              <br></br>
              <br></br>
              <button className="settingsButton" onClick={settingsClosePopup}>Back</button>
            </>
            )}
        </div>
      )}
    </>
  );
}

export default App; //exports the component so it can be imported in other files
