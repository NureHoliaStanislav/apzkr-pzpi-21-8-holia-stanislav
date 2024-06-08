import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import ProfileService from '../api/ProfileService';
import { useTranslation } from 'react-i18next';
import './Profile.css';


function Profile() {
    const [user, setUser] = useState(null);
    const { t } = useTranslation();
  
    useEffect(() => {
        async function fetchProfile() {
            try {
                const profile = await ProfileService.getProfile();
                setUser(profile);
            } catch (error) {
                console.error('Failed to fetch profile:', error);
            }
        }

        fetchProfile();
    }, []);

    if (!user) {
        return <Typography>Loading...</Typography>;
    }

    return (
        <Card className="profile-card">
            <CardContent>
                <Typography variant="h4" component="h2">
                    {user.first_name} {user.last_name}
                </Typography>
                <Typography color="textSecondary">
                    {t('Email')}: {user.email}
                </Typography>
                {!user.is_staff && (
                    <>
                        <Typography color="textSecondary">
                            {t('Role')}: {user.role}
                        </Typography>
                        <Typography color="textSecondary">
                            {user.role === 'INSTRUCTOR' ? `${t('Experience')}: ${user.experience}` : `${t('Unit')}: ${user.unit}`}
                        </Typography>
                        <Typography color="textSecondary">
                            {t('Specialization')}: {user.specialization}
                        </Typography>
                    </>
                )}
                <Typography color="textSecondary">
                    {t('Is Staff')}: {user.is_staff ? t('Yes') : t('No')}
                </Typography>
                <Typography color="textSecondary">
                    {t('Is Active')}: {user.is_active ? t('Yes') : t('No')}
                </Typography>
            </CardContent>
        </Card>
    );
}

export default Profile;