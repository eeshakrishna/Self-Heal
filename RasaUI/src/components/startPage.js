import React from "react";
//import { Link } from 'react-router-dom';
import '../App.css';

function Start() {
  return (
    <div className="LPhomebody">
      <div className="LPcontainer">
        <div className="LPcard">
          <h1 className="LPtitle">Welcome to Self Heal</h1>
          <a href="/login" className="LPbutton">Login</a> <spacer/><spacer/>
          <a href="/register" className="LPbutton">Register</a>
        </div>
      </div>
      <div className="LPcontainer">
        <div className="LPcard">
          <h1 className="LPtitle">About Self Heal</h1>
          <p className="LPdescription"> Meet your new chat companion dedicated to making you feel heard. Our bot engages in
            meaningful conversations, offering you a space to express yourself freely and explore your emotions.
            With every chat, discover a path toward healing and empowerment.<br/><br/> </p>
        </div>
      </div>
    </div>
  );
}
export default Start;