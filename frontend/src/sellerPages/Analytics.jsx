import { Routes, Route, Link } from "react-router-dom";
function Analytics() {
  return (
    <>
    
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/current-bundles">Current Bundles</Link> |{" "}
        <Link to="/add-bundles">Add Bundles</Link>
      </nav>
    </>
  );
}

export default Analytics