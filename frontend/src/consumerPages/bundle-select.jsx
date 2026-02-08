import { Routes, Route, Link } from "react-router-dom";
function BundleSelect() {
  return (
      <>
      
        <nav>
          <Link to="/login">Login Page</Link> |{" "}
          <Link to="/discover">Discover</Link> |{" "}
          <Link to="/codes">Codes</Link>
        </nav>
      </>
    );
}

export default BundleSelect;