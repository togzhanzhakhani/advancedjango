import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import '../css/auth.css'
import Notification from "./Notification";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [role, setRole] = useState("job_seeker");
  const [showNotification, setShowNotification] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/api/register/", {
        username: username,
        password: password,
        email: email,
        role: role,
      });
      setMessage("Please check your email for the confirmation link.");
      setShowNotification(true);
    } catch (error) {
      setMessage("Error during registration, please try again.");
      setShowNotification(true);
      console.error("Error during registration:", error);
    }
  };
  const handleCloseNotification = () => {
    setShowNotification(false);
  };

  return (
    <div className="register-container">
      <h2 className="register-title">Register</h2>
      <form onSubmit={handleRegister} className="register-form">
        <div className="form-group">
          <label className="label">Username:</label>
          <input
            type="text"
            className="input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
          />
        </div>
        <div className="form-group">
          <label className="label">Email:</label>
          <input
            type="email"
            value={email}
            className="input"
            placeholder="Enter your email"
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label className="label">Role:</label>
          <select
            value={role}
            className="input"
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="job_seeker">Job Seeker</option>
            <option value="recruiter">Recruiter</option>
          </select>
        </div>
        <div className="form-group">
          <label className="label">Password:</label>
          <input
            type="password"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
          />
        </div>
        <button type="submit" className="submit-button">Register</button>
      </form>
      <div className="login-link">
        <p>Already have an account?</p>
        <button onClick={() => navigate("/login")} className="link-button">Login Here</button>
      </div>
      {showNotification && <Notification message={message} onClose={handleCloseNotification} />}
    </div>
  );
}

export default Register;
