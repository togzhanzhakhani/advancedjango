import React, { useState, useEffect } from "react";

const Notification = ({ message, onClose }) => {
  return (
    <div className="notification-container">
      <div className="notification-message">
        <span>{message}</span>
        <button onClick={onClose} className="close-button">X</button>
      </div>
    </div>
  );
};

export default Notification;
