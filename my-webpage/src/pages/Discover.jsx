import { Routes, Route, Link } from "react-router-dom";
function Discover() {
  return (
    <>
    
      <nav>
        <Link to="/login">Login Page</Link> |{" "}
        <Link to="/streaks">Streaks</Link> |{" "}
        <Link to="/codes">Codes</Link>
      </nav>
    </>
  );
}

export default Discover
