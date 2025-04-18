import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/Register"; 
import Login from "./pages/Login";
import ConfirmEmail from "./pages/ConfirmEmail";
import ResetPassword from "./pages/ResetPassword";
import NewPassword from "./pages/NewPassword";
import Home from "./pages/Home";

function App() {
  return (
    <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/confirm-email/:uid/:token" element={<ConfirmEmail />} />
            <Route path="/login" element={<Login />} />
            <Route path="/reset-password" element={<ResetPassword />}  />
            <Route path="/new-password/:uid/:token" element={<NewPassword />} />
          </Routes>
    </Router>
  );
}

export default App;
