import { Routes, Route, Link } from "react-router-dom";
function Analytics() {
  return (
    <>

      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/add-bundles" className="button"><b>Add Bundles</b></Link>
      </nav>
    </>
  );
}

export default Analytics