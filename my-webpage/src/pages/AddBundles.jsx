import { Routes, Route, Link } from "react-router-dom";
function AddBundles() {
  return (
    <>
    
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/current-bundles">Current Bundles</Link> |{" "}
        <Link to="/analytics">Analytics</Link>
      </nav>
    </>
  );
}

export default AddBundles