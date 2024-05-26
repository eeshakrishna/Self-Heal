import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './loginRegister.css'

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/login', {
                email,
                password
            },{
                withCredentials:true,
              }
        );
            setMessage(response.data.message);
            sessionStorage.setItem('email', email)

            // Redirect to home page if login is successful
            if (response.data.message === "Logged in successfully") {
                navigate('/home'); // Redirect to home page
            }
        } catch (error) {
            setMessage(error.response.data.message);
        }
    };

    return (
        <div className="bby">
        <div className="container">
            <h2>Login</h2>
            <form className="form" onSubmit={handleSubmit}>
                <div>
                    {/* <label>Email</label> */}
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email" 
                        className="input-field"
                    />
                </div>
                <div>
                    {/* <label>Password</label> */}
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password" 
                        className="input-field"
                    />
                </div>
                <button className="button" type="submit">Login</button>
                {message && <p>{message}</p>}
            </form>
            <p>New to Self-Heal? <Link to="/register">Register Now</Link></p>  
        </div>
        </div>
    );
}

export default Login;
