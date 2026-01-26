import { Routes, Route, Link } from "react-router-dom";
function ViewReports() {
  return (
    <>
    
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/testing">Testing</Link> |{" "}
        <Link to="/deployment-history">Deployment History</Link>
      </nav>
    </>
  );
}

export default ViewReports