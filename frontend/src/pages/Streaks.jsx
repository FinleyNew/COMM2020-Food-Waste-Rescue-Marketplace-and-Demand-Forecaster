import { Routes, Route, Link } from "react-router-dom";
function Streaks() {
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

export default Streaks;
