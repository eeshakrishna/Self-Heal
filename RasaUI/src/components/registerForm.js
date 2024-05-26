import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import './loginRegister.css'

function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [dob, setDob] = useState("");
  const [phone, setPhone] = useState("");
  const [emergencyContact, setEmergencyContact] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const { response } = await axios.post("http://localhost:5000/register",
       {
        name,
        email,
        password,
        dob,
        phone,
        emergency_contact: emergencyContact
      },{
        withCredentials:true,
      }
      );

    if (response && response.data && response.data.message) {
      setMessage(response.data.message);

      // Redirect to login page after successful registration
      if (response.data.message === "Registered successfully") {
        navigate('/login');  // Redirect to login page
      }
    } else {
      setMessage("Registered Successful");
    }
  } catch (error) {
    if (
      error.response &&
      error.response.data &&
      error.response.data.message
    ) {
      setMessage(error.response.data.message);
    } else {
      setMessage("Network error occurred");
    }
  }
};

return (
  <div className=" bby">
    <div className=" container ">
      <h2>REGISTER </h2>
      <form className="form" onSubmit={handleSubmit}>
        <div>
          {/* <label>Name</label> */}
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="input-field"
            placeholder="Name"
          />
        </div>
        <div>
          {/* <label>Email</label> */}
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="input-field"
            placeholder="Email"
          />
        </div>
        <div>
          {/* <label>Password</label> */}
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
            placeholder="Password"
          />
        </div>
        <div>
          {/* <label>Date of Birth</label> */}
          <input
            type="text"
            value={dob}
            onChange={(e) => setDob(e.target.value)}
            className="input-field"
            placeholder="DOB(DD-MM-YY)"
          />
        </div>
        <div>
          {/* <label>Phone Number</label> */}
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            className="input-field"
            placeholder="Phone Number"
          />
        </div>
        <div>
          {/* <label>Emergency Contact Number</label> */}
          <input
            type="tel"
            value={emergencyContact}
            onChange={(e) => setEmergencyContact(e.target.value)}
            className="input-field"
            placeholder="Emergency Contact Number"
          />
        </div>
        <button type="submit" className="button">REGISTER</button> <br/>
        <a href="/login"> <p>After registering go to login</p> </a>
        {message && <p>{message}</p>}
      </form>
    </div>
  </div>
);
}

export default Register;
