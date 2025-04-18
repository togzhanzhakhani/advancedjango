import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import '../css/resetpass.css'

const NewPassword = () => {
    const { uid, token } = useParams();
    const [newPassword, setNewPassword] = useState("");
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState(""); 
    const navigate = useNavigate();
  
    useEffect(() => {
      if (!uid || !token) {
        setMessage("Invalid or expired link.");
        setMessageType("error");
      }
    }, [uid, token]);
  
    const handleSubmit = async (e) => {
      e.preventDefault();
  
      try {
        const response = await axios.post(
          `http://localhost:8000/api/password_reset/confirm/${uid}/${token}/`,
          { new_password: newPassword }
        );
        setMessage(response.data.message);
        setMessageType("success");
        // setTimeout(() => {
        //   navigate("/login"); 
        // }, 3000);
      } catch (error) {
        setMessage("Error resetting password. Please try again.");
        setMessageType("error");
      }
    };
  
    return (
      <div className="password-reset-wrapper">
        <h2>Reset Password</h2>
        <form onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="password"
            className="input"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            placeholder="Enter new password"
          />
        </div>
          <button type="submit" className="submit-button">Reset Password</button>
        </form>
  
        {message && (
          <div className={`message ${messageType}`}>
            <p>{message}</p>
          </div>
        )}
  
        <div className="login-link">
          <p>Remembered your password?</p>
          <a href="/login">Login here</a>
        </div>
      </div>
    );
  };
export default NewPassword;
