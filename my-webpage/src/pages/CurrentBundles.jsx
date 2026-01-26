import { Routes, Route, Link } from "react-router-dom";
function CurrentBundles() {
  return (
    <>
    
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/add-bundles">Add Bundles</Link> |{" "}
        <Link to="/analytics">Analytics</Link>
      </nav>
    </>
  );
}

export default CurrentBundles