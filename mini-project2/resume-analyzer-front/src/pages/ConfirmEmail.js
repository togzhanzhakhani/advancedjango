import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useParams } from 'react-router-dom';
import '../css/ConfirmEmail.css';

function ConfirmEmail() {
  const { uid, token } = useParams();
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const confirmEmail = async () => {
      try {
        const response = await axios.post(
          `http://localhost:8000/api/confirm-email/${uid}/${token}/`
        );
        setMessage("Email confirmed successfully!");
        setTimeout(() => {
            navigate('/login'); 
          }, 3000);  
      } catch (error) {
        console.error("Error during email confirmation", error);
        setMessage("Invalid or expired link.");
      }
    };
    confirmEmail();
    }, [uid, token, navigate]);

    return (
    <div className="confirm-email-container">
        <h2 className="confirm-email-title">Email Confirmation</h2>
        <p className="confirm-email-message">{message}</p>
    </div>
    );
}
export default ConfirmEmail;