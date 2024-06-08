import React, { useState } from 'react';
import AuthService from '../../shared/AuthService';
import { useTranslation } from 'react-i18next';
import './Login.css'; 

function Login({ onLogin }) {
  const { t } = useTranslation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    AuthService.login({ user: { email, password } })
      .then(() =>{
        onLogin();
        setError(null);
      })
      .catch(error => {
        setError(error.message);
        console.error(error);
      });
  };

  return (
    <div className="login-container">
      <h2>{t('Login')}</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <input 
          type="email" 
          value={email} 
          onChange={e => setEmail(e.target.value)} 
          required 
          placeholder={t('Email')}
        />
        <input 
          type="password" 
          value={password} 
          onChange={e => setPassword(e.target.value)} 
          required 
          placeholder={t('Password')}
        />
        {error && <p className="error-message">{t('Incorrect password or login')}</p>}
        <button type="submit" className="login-button">{t('Login')}</button>
      </form>
    </div>    
    );
}

export default Login;
