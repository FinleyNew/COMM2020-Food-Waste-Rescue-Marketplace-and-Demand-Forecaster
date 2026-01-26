import { Routes, Route, Link } from "react-router-dom";
function Codes() {
  return (
      <>
      
        <nav>
          <Link to="/login">Login Page</Link> |{" "}
          <Link to="/discover">Discover</Link> |{" "}
          <Link to="/streaks">Streaks</Link>
        </nav>
      </>
    );
}

export default Codes
