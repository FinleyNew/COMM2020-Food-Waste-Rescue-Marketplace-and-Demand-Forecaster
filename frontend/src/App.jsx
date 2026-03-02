import { useState, useEffect } from "react"; //importing state so we can use it to change the state of the react page when anything changes
import { Routes, Route, Link } from "react-router-dom"; //needs to be imported so we can add routes between pages
import ProtectedRoute from "./pages/ProtectedRoute"; //to use protected routes, so that consumers cannot enter seller pages and vice versa
//import './App.css'
import "./index.css"
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
import Testing from "./adminPages/testing";
import ViewReports from "./adminPages/ViewReports";
import HomePage from "./pages/HomePage";
import Unauthorised from "./pages/unauthorised";
//|{" "}

function App() {

  const[darkMode, setDarkMode] = useState(false); //store the variable for the current state
  useEffect(() => { //update the page if the theme is changed
    const savedTheme = localStorage.getItem("theme"); //store the theme in local storage

    if(savedTheme === "dark"){
      setDarkMode(true); //if dark mode is selected change the theme
      document.documentElement.classList.add("dark");
    }
  },[]);

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

  const [user, setUser] = useState(() => { //user = current state, setuser = function to update user and role later,  useState is a hook to remebember data across re-renders
  const savedUser = localStorage.getItem("user"); //reads from local storage under the key of user
  return savedUser ? JSON.parse(savedUser) : null; //if thertes something in local storage, if yes the parse converts back to a js object
  });
    

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
        <Route path="/testing" element={<ProtectedRoute user={user} requireRole="admin"><Testing /></ProtectedRoute>} />
        <Route path="/view-reports" element={<ProtectedRoute user={user} requireRole="admin"><ViewReports /></ProtectedRoute>} />


        <Route path="/" element={<HomePage />} /> {/* these pages are accessible by everybody */}
        <Route path="/unauthorised" element={<Unauthorised />} />
        <Route path="/bundle/:id" element={<BundleSelect />} />
        
        
      </Routes>
      
      <div>
        <button className="dark-mode-btn" onClick={toggleDarkMode} >
          {darkMode ? "Light Mode" : "Dark Mode"} 
        </button>
      </div>
      
      
      
    </>
  );
}

export default App; //exports the component so it can be imported in other files
