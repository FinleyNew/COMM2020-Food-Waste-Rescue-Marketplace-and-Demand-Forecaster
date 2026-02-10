import { useState } from "react";
import { useNavigate } from "react-router-dom";


function LoginPage({setUser}) {// username is the variable, setUsername changes it and useState means it can be changed throughout the program
  const [username, setUsername] = useState(""); //setUsername is the function to change it, defining variables of username and password
  const [password, setPassword] = useState(""); //more secure than accessing it with getElementId
  const navigate = useNavigate();

  function loginFunction() {
    if (username=== "harryConsumer" && password === "lewis") {
      setUser({
        username:"harry",
        role:"consumer"
      })
      localStorage.setItem("user",JSON.stringify({username:"harry",role: "consumer"}));
      localStorage.setItem('token',"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDE0NzQ5NTgsInN1YiI6IjEifQ.TBw2UD-s4nuWlWTcBzj95SNjuHKC0KaBmf49cW2DJrU");
      navigate("/discover");
    } 
    else if(username === "harrySeller" && password === "lewis"){
      setUser({
        username:"harry",
        role:"seller"
      })
      localStorage.setItem("user",JSON.stringify({username:"harry",role: "seller"}));
      localStorage.setItem('token',"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDE0NzQ5MDksInN1YiI6IjIifQ.Ayy7RYQGz3dhAFC9txefYLdAe_hbvjtzHMtOTm2utU4")
      navigate("/current-bundles");
    }
    else if(username === "harryAdmin" && password === "lewis"){
      setUser({
        username:"harry",
        role:"admin"
      })
      localStorage.setItem("user",JSON.stringify({username:"harry",role: "admin"}));
      navigate("/view-reports");
    }
    else {
      alert("Wrong username or password");
    }
  }

  return (
    <>
      <h3>Please Enter Username and Password</h3>

      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <br /><br />

      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <br /><br />

      <button onClick={loginFunction}>Login</button>
    </>
  );
}

export default LoginPage;
