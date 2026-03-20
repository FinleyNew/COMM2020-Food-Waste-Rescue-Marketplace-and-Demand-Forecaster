import { Routes, Route, Link } from "react-router-dom";
function ViewReports() {
  return (
    <>
    {/* Initialises the navifation bar where sellers can move between pages */}
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/view-information">View Information</Link> | {" "}
        <Link to="/deployment-history">Deployment History</Link>
      </nav>
    </>
  );
}
//exports the component so it can be imported in other files
export default ViewReports