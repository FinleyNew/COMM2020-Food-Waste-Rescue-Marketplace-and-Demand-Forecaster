import { Routes, Route, Link } from "react-router-dom";
function DeploymentHistory() {
  return (
    <>
    
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/view-reports">View Reports</Link> |{" "}
        <Link to="/testing">Testing</Link>
      </nav>
    </>
  );
}

export default DeploymentHistory