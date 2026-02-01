import { Routes, Route, Link } from "react-router-dom";
function AddBundles() {
  return (
    <>

      <nav class="row">
        <Link to="/login" className="button"><b>Login Page</b></Link>
        <Link to="/current-bundles" className="button"><b>Current Bundles</b></Link>
        <Link to="/analytics" className="button"><b>Analytics</b></Link>
      </nav>
      <h1 className="headline">Add Bundles</h1>
      <section>
        <div className="textBlock">
            <div className="desc">
              <p>Bundle Name</p>
              <p>Location</p>
              <p>Collection Time</p>
            </div>
            <p className="button">Add</p>
        </div>
      </section>
    </>
  );
}

export default AddBundles