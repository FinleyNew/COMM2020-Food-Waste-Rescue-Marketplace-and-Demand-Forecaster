import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./loginPage.css"

function LoginPage({setUser}) {// username is the variable, setUsername changes it and useState means it can be changed throughout the program
  const [username, setUsername] = useState(""); //setUsername is the function to change it, defining variables of username and password
  const [password, setPassword] = useState(""); //more secure than accessing it with getElementId
  const navigate = useNavigate();

  function loginFunction() {
    if (username=== "consumer" && password === "1") { //Pathway for if the consumer details are correctly inputted
      setUser({ //Defines username and role constant attributes for this consumer login
        username:"harry",
        role:"consumer"
      })
      localStorage.setItem("user",JSON.stringify({username:"harry",role: "consumer"})); //Stores details so that they remain if the page is refreshed or the state changes
      localStorage.setItem('token',"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDE0NzQ5NTgsInN1YiI6IjEifQ.TBw2UD-s4nuWlWTcBzj95SNjuHKC0KaBmf49cW2DJrU"); //Stores the user token for further authentication
      navigate("/discover"); //Takes the user to the discover page in consumerPages
    } 
    else if(username === "seller" && password === "1"){ //Pathway for if the seller details are correctly inputted
      setUser({ //Defines username and role constant attributes for this seller login
        username:"harry",
        role:"seller"
      })
      localStorage.setItem("user",JSON.stringify({username:"harry",role: "seller"})); //Stores details so that they remain if the page is refreshed or the state changes
      localStorage.setItem('token',"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDE0NzQ5MDksInN1YiI6IjIifQ.Ayy7RYQGz3dhAFC9txefYLdAe_hbvjtzHMtOTm2utU4") //Stores the user token for further authentication
      navigate("/current-bundles"); //Directs the user to the current-bundles page in sellerPages
    }
    else if(username === "harryAdmin" && password === "lewis"){ //Pathway for if the admin details are correctly inputted
      setUser({ //Defines username and role constant attributes for this admin login
        username:"harry",
        role:"admin"
      })
      localStorage.setItem("user",JSON.stringify({username:"harry",role: "admin"})); //Stores details so that they remain if the page is refreshed or the state changes
      navigate("/view-reports"); //Takes the user to the view-reports page in adminPages
    }
    else {
      alert("Wrong username or password"); //Error message if inputs don't correlate with any provided
    }
  }

  return (
    <div className="loginBox">
      <div className="loginItems">
        <h3>Please Enter Username and Password</h3> {/* Writes a prompt to screen for username and password */}
        {/* Creates an input box for the user to send their username and saves it */}
        <input 
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        {/* Creates a space in the page */}
        <br /><br />
        {/* Creates an input box for the user to send their password and saves it */}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {/* Creates a space in the page */}
        <br /><br />
        {/* Makes a button that submits entires to above input boxes when selected*/}
        <button onClick={loginFunction}>Login</button>
      </div>
    </div>
  );
}

//exports the component so it can be imported in other files
export default LoginPage;
