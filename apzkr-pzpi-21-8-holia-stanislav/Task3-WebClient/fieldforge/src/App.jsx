import React, { useState, useEffect } from 'react';
import AuthService from './shared/AuthService'; // Adjusted path
import { BrowserRouter as Router, Routes, Route, useNavigate, Navigate } from 'react-router-dom'; // Added Navigate
import Login from './pages/login/Login';
import SignUp from './pages/sign-up/SignUp';
import Trainings from './pages/trainings/ui/Trainings';
import Profile from './pages/profile/ui/Profile';
import Mines from './pages/mines/ui/Mines';
import Users from './pages/users/ui/Users';
import Header from './shared/header/Header';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    AuthService.getCurrentUser().then(res => setUser(res))
  }, []);

 const handleLogin = () => {
    AuthService.getCurrentUser().then(res => setUser(res))
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div className="App-header">
      <Router>
      <Header user={user} onLogout={handleLogout} />{
          <Routes>
            <Route path="/login" element={<LoginWrapper user={user} onLogin={handleLogin} />} />
            <Route path="/sign-up" element={<SignUpWrapper user={user} onLogin={handleLogin} />} />
            <Route path="/mines" element={<MinesWrapper user={user}/>} />
            <Route path="/users" element={<UsersWrapper user={user}/>} />
            <Route path="/profile" element={<ProfileWrapper user={user}/>} />
            <Route path="/trainings" element={<TrainingsWrapper user={user}/>} />
            <Route path="/" element={<Navigate to="/login" />} /> {/* Redirects to /login */}
          </Routes>
        }
      </Router>
    </div>
  );
}

function LoginWrapper({ user, onLogin }) {
  const navigate = useNavigate();
  useEffect(() => {
    if (user) {
      navigate('/profile');
    }
  }, [user, navigate]);

  return <Login onLogin={onLogin} />;
}

function SignUpWrapper({ user, onLogin }) {
  const navigate = useNavigate();
  useEffect(() => {
    if (user) {
      navigate('/profile');
    }
  }, [user, navigate]);

  return <SignUp onLogin={onLogin} />;
}

function MinesWrapper({ user }) {
  const navigate = useNavigate();
  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  return <Mines/>;
}

function UsersWrapper({ user }) {
  const navigate = useNavigate();
  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  return <Users/>;
}

function ProfileWrapper({ user }) {
  const navigate = useNavigate();
  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  return <Profile/>;
}
function TrainingsWrapper({ user }) {
  const navigate = useNavigate();
  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  return <Trainings/>;
}
export default App;

