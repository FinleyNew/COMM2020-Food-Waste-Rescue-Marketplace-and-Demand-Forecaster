import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./loginPage.css"

function LoginPage({setUser}) {// username is the variable, setUsername changes it and useState means it can be changed throughout the program
  const [username, setUsername] = useState(""); //setUsername is the function to change it, defining variables of username and password
  const [password, setPassword] = useState(""); //more secure than accessing it with getElementId
  const navigate = useNavigate();
  const [ErrorLogin, setErrorLogin] = useState(false);
  const [Popup, setPopup] = useState(false);
  const [token,setToken] = useState("");
  const [role,setRole] = useState("");
  function openPopup() {
    setPopup(true); //if variable is true then popUp needs to be opened 
  }
  function closePopup() {
    setPopup(false); //if variable is false then popUp needs to be closed
  }
  function loginFunction() {

    const data={
      grant_type:"password",
      username:username,
      password:password.toString()
    };
    const formData = new URLSearchParams();
    formData.append("grant_type","password");
    formData.append("username",username);
    formData.append("password",password);
   



    fetch("http://127.0.0.1:8000/api/v1/login/access-token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: formData
    })
    .then(res => {
      if(!res.ok){
        throw new Error(`Server Error: ${res.status}`);
      }
      return res.json();
    })
    .then(data => {
      const token = data.access_token;
      setToken(token);
      if(token){
      //token is set
      //new fetch

      fetch(`http://127.0.0.1:8000/api/v1/users/me`, { //Fetches inputted tocken
      method: "GET",
      headers:{
        "Authorization": `Bearer ${token}`
      }
      })
      .then(res => res.json())
      .then(data => {

        const role = data.role;
        setRole(role);

        if(role=="consumer"){
          setUser({
            username:username,
            role:"consumer"
          })
          localStorage.setItem('token',token);
          navigate("/discover")
        }
        else if(role=="seller"){
          setUser({
            username:username,
            role:"seller"
          })
          localStorage.setItem('token',token);
          navigate("/current-bundles")
        }
        else{
          console.error("unknown role")
        }





      })
      .catch(err => console.error(err));
    }
    })
    //Alerts upon an error
    .catch(err => {
      console.error("Error fetching data ",err);
      alert("No data")
    })

    
    
    










    
  }

  return (
    <div className="loginBox">
      <div className="loginItems">
        <h3>Please Enter Your Email and Password</h3> {/* Writes a prompt to screen for username and password */}
        {/* Creates an input box for the user to send their username and saves it */}
        <div className="rowRegister">
          <p>Email:</p>
          <input 
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        {/* Creates an input box for the user to send their password and saves it */}
        <div className="rowRegister">
          <p>Password:</p>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {ErrorLogin && (
          <div className="popupRegister open-popupRegister">
            <h3>No Account Found</h3>
            <br></br>
            <br></br>
            <p>We could not find an account associated with this email and password, please try again.</p>
            <br></br>
            <button onClick={() => setErrorLogin(false)}>Confirm</button>
          </div>
        )}
        <br></br>
        {/* Makes a button that submits entires to above input boxes when selected*/}
        <div className="rowRegister">
          <button className="loginButton" onClick={loginFunction}>Login</button>
          <button className="loginButton" onClick={() => (openPopup())}> {/* if the pay button is clicked it sends the information to the create reservation page */}
                Register
          </button>
        </div>
            {Popup && (
              <div className="popupRegister open-popupRegister">
                <h3>Account Registration</h3>  {/*if the button is clicked, open the pop up to pay*/}
                <br></br>
                <div className="rowRegister">
                  <p>Email: </p>
                  <input 
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </div>
                {/* Creates an input box for the user to send their password and saves it */}
                <div className="rowRegister">
                  <p>Password:</p>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
                <div className="rowRegister">
                  <button onClick={closePopup}>Confirm</button>
                  <button onClick={closePopup}>Cancel</button>
                </div>
              </div>
            )}
      </div>
    </div>
  );
}

//exports the component so it can be imported in other files
export default LoginPage;
