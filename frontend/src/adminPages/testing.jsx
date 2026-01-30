import { Routes, Route, Link } from "react-router-dom";
function Testing() {
  return (
    <>
    
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/view-reports">View Reports</Link> |{" "}
        <Link to="/deployment-history">Deployment History</Link>
      </nav>
    </>
  );
}

export default Testing