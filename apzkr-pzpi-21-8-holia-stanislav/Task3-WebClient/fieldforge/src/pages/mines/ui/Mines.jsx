import React, { useState, useEffect } from 'react';
import MinesService from '../api/MinesService';
import { useTranslation } from 'react-i18next';
import './Mines.css';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Typography,
    Button,
    TextField,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Select,
    MenuItem,
    FormControl,
    InputLabel
} from '@mui/material';


function Mines() {
    const [mines, setMines] = useState(null);
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);
    const [newMine, setNewMine] = useState({ uuid: '', type: '', range: '', is_activated: false, is_defused: false });

    const fetchMines = async () => {
        try {
            const mines = await MinesService.getMines();
            setMines(mines);
        } catch (error) {
            console.error('Failed to fetch mines:', error);
        }
    };
    const handleAddMine = async () => {
        try {
            await MinesService.addMine(newMine);
            fetchMines();
            setOpen(false);
            setNewMine({ uuid: '', type: '', range: '', is_activated: false, is_defused: false });
        } catch (error) {
            console.error('Failed to add mine:', error);
        }
    };


    const handleDeleteMine = async (uuid) => {
        try {
            await MinesService.deleteMine(uuid);
            setMines(mines.filter(mine => mine.uuid !== uuid));
        } catch (error) {
            console.error('Failed to delete mine:', error);
        }
    };


    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewMine(prevState => ({ ...prevState, [name]: value }));
    };

    useEffect(() => {
        fetchMines();
    }, []);

    if (!mines) {
        return <Typography>{t("There is no mines in system")}</Typography>;
    }

    return (
        <div>
            <Typography variant="h4" className="title">
                {t('Mines')}
            </Typography>
            <Button variant="contained" color="primary" className="addButton" onClick={() => setOpen(true)}>
                {t('Add New Mine')}
            </Button>
            <Dialog open={open} onClose={() => setOpen(false)}>
                <DialogTitle>{t('Add New Mine')}</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        {t('To add a new mine, please enter the mine type, range, activation status, and defused status here.')}
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        name="uuid"
                        label={t("UUID")}
                        type="text"
                        fullWidth
                        value={newMine.uuid}
                        onChange={handleChange}
                    />
                    <FormControl margin="dense" fullWidth>
                        <InputLabel>{t("Type")}</InputLabel>
                        <Select
                            name="type"
                            value={newMine.type}
                            onChange={handleChange}
                        >
                            <MenuItem value="AP">{t("Anti Personnel")}</MenuItem>
                            <MenuItem value="TW">{t("Tripwire")}</MenuItem>
                        </Select>
                    </FormControl>
                    <TextField
                        margin="dense"
                        name="range"
                        label={t("Range")}
                        type="number"
                        fullWidth
                        value={newMine.range}
                        onChange={handleChange}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpen(false)} color="primary">
                        {t('Cancel')}
                    </Button>
                    <Button onClick={handleAddMine} color="primary">
                        {t('Add')}
                    </Button>
                </DialogActions>
            </Dialog>
            <TableContainer component={Paper}>
                <Table className="table" aria-label="mines table">
                    <TableHead>
                        <TableRow>
                            <TableCell>{t('UUID')}</TableCell>
                            <TableCell>{t('Type')}</TableCell>
                            <TableCell>{t('Range')}</TableCell>
                            <TableCell>{t('Is Activated')}</TableCell>
                            <TableCell>{t('Is Defused')}</TableCell>
                            <TableCell>{t('Actions')}</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {mines.map((mine) => (
                            <TableRow key={mine.uuid}>
                                <TableCell>{mine.uuid}</TableCell>
                                <TableCell>{mine.type}</TableCell>
                                <TableCell>{mine.range}</TableCell>
                                <TableCell>{mine.is_activated ? t('Yes') : t('No')}</TableCell>
                                <TableCell>{mine.is_defused ? t('Yes') : t('No')}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="contained"
                                        color="secondary"
                                        className="button"
                                        onClick={() => handleDeleteMine(mine.uuid)}
                                    >
                                        {t('Delete')}
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
};


export default Mines;