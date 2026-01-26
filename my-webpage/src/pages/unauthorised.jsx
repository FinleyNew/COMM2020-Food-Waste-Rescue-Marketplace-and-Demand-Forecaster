import { Routes, Route, Link } from "react-router-dom";
function Unauthorised() {
  return(
    <>
      
      <nav>
          <Link to="/login">Login Page</Link>
      </nav>
      <h1>You are unauthorised to view this page, please log in with another account </h1>

    </>
    
  );

}

export default Unauthorised;