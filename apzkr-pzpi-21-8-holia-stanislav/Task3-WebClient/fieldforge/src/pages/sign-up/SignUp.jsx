import React, { useState } from 'react';
import AuthService from '../../shared/AuthService';
import './SignUp.css';
import { useTranslation } from 'react-i18next';

function SignUp({ onLogin }) {
  const { t } = useTranslation();
  const [unit, setUnit] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [role, setRole] = useState('SOLDIER');
  const [experience, setExperience] = useState('');
  const [specialization, setSpecialization] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    let user = {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
      role,
    };
  
    if (role === 'SOLDIER') {
      user = { ...user, unit, specialization };
    } else if (role === 'INSTRUCTOR') {
      user = { ...user, experience, specialization };
    }
    AuthService.signup({ 
      user
    })
      .then(user => {
        onLogin(user);
        setError(null);
      })
      .catch(error => {
        setError(error.message);
        console.error(error);
      });
  };

  return (
    <div className="sign-up-container">
      <h2>{t('Sign Up')}</h2>
      <form onSubmit={handleSubmit} className="sign-up-form">
        <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder={t('Email')} required />
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder={t('Password')} required />
        <input type="text" value={firstName} onChange={e => setFirstName(e.target.value)} placeholder={t('First Name')} required />
        <input type="text" value={lastName} onChange={e => setLastName(e.target.value)} placeholder={t('Last Name')} required />
        <select value={role} onChange={e => setRole(e.target.value)} required>
          <option value="SOLDIER">{t('Soldier')}</option>
          <option value="INSTRUCTOR">{t('Instructor')}</option>
        </select>        
        {role === 'SOLDIER' ? (
          <input type="text" value={unit} onChange={e => setUnit(e.target.value)} placeholder={t('Unit')} required />
        ) : (
          <input type="text" value={experience} onChange={e => setExperience(e.target.value)} placeholder={t('Experience')} required />
        )}        
        <input type="text" value={specialization} onChange={e => setSpecialization(e.target.value)} placeholder={t('Specialization')} required />
        <button type="submit" className='sign-up-button'>{t('Sign Up')}</button>
      </form>
      {error && <p>{t(error)}</p>}
    </div>
  );
}

export default SignUp;
