import { Routes, Route, Link } from "react-router-dom";
function DeploymentHistory() {
  return (
    <>
    {/* Initialises the navifation bar where sellers can move between pages */}
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/change-information">Change Information</Link> |{" "}
        <Link to="/view-information">View Information</Link>
      </nav>
    </>
  );
}
//exports the component so it can be imported in other files
export default DeploymentHistory