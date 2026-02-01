import { useState } from "react";
import { Routes, Route, Link } from "react-router-dom";
import ProtectedRoute from "./pages/ProtectedRoute";

// Pages (ensure the file names match exactly)
import Discover from "./customerPages/Discover";
import BundleSelect from "./customerPages/bundle-select";
import Streaks from "./customerPages/Streaks";
import Codes from "./customerPages/Codes";
import LoginPage from "./pages/loginPage";
import AddBundles from "./sellerPages/AddBundles";
import Analytics from "./sellerPages/Analytics";
import CurrentBundles from "./sellerPages/CurrentBundles";
import DeploymentHistory from "./adminPages/DeploymentHistory";
import Testing from "./adminPages/testing";
import ViewReports from "./adminPages/ViewReports";
import HomePage from "./pages/HomePage";
import Unauthorised from "./pages/unauthorised";
//|{" "}

function App() {
  const [user, setUser] = useState(() => { //user = current state, setuser = function to update user and role later,  useState is a hook to remebember data across re-renders
  const savedUser = localStorage.getItem("user"); //reads from local storage under the key of user
  return savedUser ? JSON.parse(savedUser) : null; //if thertes something in local storage, if yes the parse converts back to a js object
  });
    

  return (
    <>
      {/* <nav>
        <Link to="/login">LoginPage</Link>
        
      </nav>*/}

      <Routes>
        
        <Route path="/login" element={<LoginPage setUser={setUser} />} />

        <Route path="/discover" element={<ProtectedRoute user={user} requireRole="customer"><Discover /></ProtectedRoute>} />
        <Route path="/bundle-select" element={<ProtectedRoute user={user} requireRole="customer"><BundleSelect /></ProtectedRoute>} />
        <Route path="/streaks" element={<ProtectedRoute user={user} requireRole="customer"><Streaks /></ProtectedRoute>} />
        <Route path="/codes" element={<ProtectedRoute user={user} requireRole="customer"><Codes /></ProtectedRoute>} />

        <Route path="/add-bundles" element={<ProtectedRoute user={user} requireRole="seller"><AddBundles /></ProtectedRoute>} />
        <Route path="/analytics" element={<ProtectedRoute user={user} requireRole="seller"><Analytics /></ProtectedRoute>} />
        <Route path="/current-bundles" element={<ProtectedRoute user={user} requireRole="seller"><CurrentBundles /></ProtectedRoute>} />


        <Route path="/deployment-history" element={<ProtectedRoute user={user} requireRole="admin"><DeploymentHistory /></ProtectedRoute>} />
        <Route path="/testing" element={<ProtectedRoute user={user} requireRole="admin"><Testing /></ProtectedRoute>} />
        <Route path="/view-reports" element={<ProtectedRoute user={user} requireRole="admin"><ViewReports /></ProtectedRoute>} />


        <Route path="/" element={<HomePage />} />
        <Route path="/unauthorised" element={<Unauthorised />} />
      </Routes>
      <details>
        <summary>Settings</summary>
        <label>
          <input type="checkbox" name="darkmode"/>
            Enable Dark Mode DOESNT WORK YET
        </label>
      </details>
    </>
  );
}

export default App;
