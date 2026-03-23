import { Routes, Route, Link } from "react-router-dom";
import './DeploymentHistory.css'
function DeploymentHistory() {
  return (
    <>
    {/* Initialises the navifation bar where sellers can move between pages */}
    <div className="deployment">  
      <nav className="navRow">
        <Link to="/change-information" className="button">Change Information</Link>
        <Link to="/view-information" className="button">View Information</Link>
      </nav>
    </div>
    </>
  );
}
//exports the component so it can be imported in other files
export default DeploymentHistory