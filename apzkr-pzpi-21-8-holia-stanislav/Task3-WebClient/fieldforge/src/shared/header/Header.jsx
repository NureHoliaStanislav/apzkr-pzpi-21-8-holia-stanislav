import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import AuthService from '../AuthService';
import { useNavigate } from 'react-router-dom'; 
import { useTranslation } from 'react-i18next';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';

function Header({ user, onLogout }) {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleProfile = () => {
    navigate('/profile');
  };

  const handleLogout = () => {
    AuthService.logout();
    onLogout();
  };

  const handleLogin = () => {
    navigate('/login'); 
  };

  const handleSignup = () => {
    navigate('/sign-up'); 
  };

  const handleMines = () => {
    navigate('/mines'); 
  };

  const handleUsers = () => {
    navigate('/users'); 
  };

  const handleTrainings = () => {
    navigate('/trainings');
  };

  const handleLanguageMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleLanguageChange = (lang) => {
    i18n.changeLanguage(lang);
    setAnchorEl(null);
  };

  return (
    <AppBar position="fixed" sx={{ backgroundColor: '#000' }}>
      <Toolbar>
        <Box sx={{ flexGrow: 1 }} />
        <Typography variant="h6" component="div" sx={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)' }}>
          FieldForge
        </Typography>
        <Box sx={{ flexGrow: 1, display: 'flex', justifyContent: 'flex-end' }}>
          <Button color="inherit" onClick={handleLanguageMenu}>{t('Language')}</Button>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={() => setAnchorEl(null)}
          >
            <MenuItem onClick={() => handleLanguageChange('en')}>English</MenuItem>
            <MenuItem onClick={() => handleLanguageChange('ua')}>Ukrainian</MenuItem>
          </Menu>
          {user ? (
            <>
              {user.is_staff && <Button color="inherit" onClick={handleUsers}>{t('Users')}</Button>}
              {user.is_staff && <Button color="inherit" onClick={handleMines}>{t('Mines')}</Button>}
              {!user.is_staff && <Button color="inherit" onClick={handleTrainings}>{t('Trainings')}</Button>}
              <Button color="inherit" onClick={handleProfile}>{t('Profile')}</Button>
              <Button color="inherit" onClick={handleLogout}>{t('Logout')}</Button>
            </>
          ) : (
            <>
              <Button color="inherit" onClick={handleLogin}>{t('Login')}</Button>
              <Button color="inherit" onClick={handleSignup}>{t('Sign up')}</Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Header;