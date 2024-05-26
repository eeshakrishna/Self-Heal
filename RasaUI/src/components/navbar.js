import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
//import {Navbar } from 'react-bootstrap';
import {Link} from 'react-router-dom'
import axios from 'axios';
import { useNavigate  } from 'react-router-dom';




function Navbar() {


  const navigate = useNavigate();


    const handleLogout = async () => {
        try {
            const response = await axios.post('http://localhost:5000/logout', {}, { withCredentials: true });


            if (response.status === 200) {
                alert(response.data.message);
                // Redirect to login page or homepage after logout
                navigate('/login');
            } else {
                alert('Failed to log out');
            }
        } catch (error) {
            console.error('Error logging out:', error);
            alert('An error occurred while logging out.');
        }
    };


  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light fixed-top" style={{ backgroundColor: '#efdecd', borderRadius:50, marginTop:10,marginLeft:10,marginRight:10}}>
        <div className="container-fluid">
          <span className="navbar-brand mb-0 h1" style={{ fontSize: '1.6rem', fontFamily:'serif'}}>
            <strong>SELF HEAL -  </strong> Therapy Anywhere
          </span>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNavAltMarkup"
            aria-controls="navbarNavAltMarkup"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>


          <div
            className="collapse navbar-collapse justify-content-end"
            id="navbarNavAltMarkup"
          >
            <div className="navbar-nav">
              <Link to="/home"><button className="nav-item nav-link btn btn-light mx-4" style={{ fontSize: '1.2rem' , fontFamily:'serif'}}>HOME</button></Link>
              <Link to="/hotline"><button className="nav-item nav-link btn btn-light mx-4" style={{ fontSize: '1.2rem' , fontFamily:'serif'}}>HELP</button></Link>
              <Link to="/chatbot"><button className="nav-item nav-link btn btn-light mx-4" style={{ fontSize: '1.2rem' , fontFamily:'serif'}}>BOT</button></Link>
              <Link to="/features"><button className="nav-item nav-link btn btn-light mx-4" style={{ fontSize: '1.2rem' , fontFamily:'serif'}}>FEATURES</button></Link>
              <button className="nav-item nav-link btn btn-light mx-4" style={{ fontSize: '1.2rem' , fontFamily:'serif'}} onClick={handleLogout} >LOGOUT</button>
              {/* <button onClick={handleLogout}>Logout</button> */}
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
}


export default Navbar;



