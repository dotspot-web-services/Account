
import { useState } from "react";

function Loguser() {
   const [loginData, setLogin] = useState({
        username : "",
        paswd : ""
   })
   function handleInputChange(event:any){
        event.preventDefault()
        event.target.id != 'paswd'? setLogin({...loginData, username: event.target.value}):
        setLogin({...loginData, paswd: event.target.value})
   }
   function handleSubmit(event:any){
        event.preventDefault()
        const formdata:any = new FormData(event.target)
    }
    return(
        <div className="login">
            <form action="">
                <input type="text" name="username" id="username" placeholder="Email or Phone" ref={loginData.username} onChange={handleInputChange} required />
                <input type="passwod" name="paswd" id="paswd" placeholder="Password" ref={loginData.paswd} onChange={handleInputChange} required />
                <input type="submit" value="Login" />
            </form>
            <button>
                <a href="http://">
                    <img src="" alt="Search" />
                </a>
            </button>
        </div>
    )  
};


export default Loguser;