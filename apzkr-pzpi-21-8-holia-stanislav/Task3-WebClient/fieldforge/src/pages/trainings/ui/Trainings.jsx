import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import TrainingsService from '../api/TrainingsService';
import { useTranslation } from 'react-i18next';
import './Trainings.css';


function Profile() {
    const [trainings, setTrainings] = useState(null);
    const { t } = useTranslation();
  
    useEffect(() => {
        async function fetchTrainings() {
            try {
                const trainings = await TrainingsService.getTrainings();
                setTrainings(trainings);
            } catch (error) {
                console.error('Failed to fetch trainings:', error);
            }
        }

        fetchTrainings();
    }, []);

    if (!trainings) {
        return <Typography>{t("You doesnt have any trainings yet")}</Typography>;
    }

    return (
        <div className="trainings-container">
        {trainings.map((training) => (
            <Card key={training.uuid} className="training-card">
                <CardContent>
                    <Typography variant="h5" component="div">
                        {t('Training type')}: {training.type}
                    </Typography>
                    <Typography color="textSecondary">
                        {t('Start Time')}: {new Date(training.start_time).toLocaleString()}
                    </Typography>
                    <Typography color="textSecondary">
                        {t('End Time')}: {new Date(training.end_time).toLocaleString()}
                    </Typography>
                    <Typography variant="body2">
                        {t('Description')}: {training.description}
                    </Typography>
                </CardContent>
            </Card>
        ))}
    </div>
    );
}

export default Profile;