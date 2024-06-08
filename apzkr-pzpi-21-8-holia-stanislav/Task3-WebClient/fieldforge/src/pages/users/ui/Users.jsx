import React, { useState, useEffect } from 'react';
import UsersService from '../api/UsersService';
import { useTranslation } from 'react-i18next';
import './Users.css';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Typography,
    Button
} from '@mui/material';


function Users() {
    const [users, setUsers] = useState(null);
    const { t } = useTranslation();
    const fetchUsers = async () => {
        try {
            const users = await UsersService.getUsers();
            setUsers(users);
        } catch (error) {
            console.error('Failed to fetch users:', error);
        }
    };
    const handleBanUser = async (uuid) => {
        console.log(`Ban user with UUID: ${uuid}`);
        try {
            const result = await UsersService.banUser(uuid);
            console.log(result);
            // After successfully banning the user, you might want to remove them from the users state or refetch the users
            fetchUsers();
        } catch (error) {
            console.error('Failed to ban user:', error);
        }
    };
    useEffect(() => {
        fetchUsers();
    }, []);

    if (!users) {
        return <Typography>{t("There is no users in system")}</Typography>;
    }

    return (
        <div>
            <Typography variant="h4" className="users-title">
                {t('Users')}
            </Typography>
            <TableContainer component={Paper}>
                <Table className="users-table" aria-label="users table">
                    <TableHead>
                        <TableRow>
                            <TableCell>{t('UUID')}</TableCell>
                            <TableCell>{t('First Name')}</TableCell>
                            <TableCell>{t('Last Name')}</TableCell>
                            <TableCell>{t('Email')}</TableCell>
                            <TableCell>{t('Role')}</TableCell>
                            <TableCell>{t('Is Staff')}</TableCell>
                            <TableCell>{t('Is Active')}</TableCell>
                            <TableCell>{t('Unit')}</TableCell>
                            <TableCell>{t('Specialization')}</TableCell>
                            <TableCell>{t('Experience')}</TableCell>
                            <TableCell>{t("Actions")}</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {users.map((user) => (
                            <TableRow key={user.uuid}>
                                <TableCell>{user.uuid}</TableCell>
                                <TableCell>{user.first_name}</TableCell>
                                <TableCell>{user.last_name}</TableCell>
                                <TableCell>{user.email}</TableCell>
                                <TableCell>{user.role || '-'}</TableCell>
                                <TableCell>{user.is_staff ? t('Yes') : t('No')}</TableCell>
                                <TableCell>{user.is_active ? t('Yes') : t('No')}</TableCell>
                                <TableCell>{user.unit || '-'}</TableCell>
                                <TableCell>{user.specialization || '-'}</TableCell>
                                <TableCell>{user.experience || '-'}</TableCell>
                                <TableCell>
                                    <Button
                                        variant="contained"
                                        color="error"
                                        size="small"
                                        onClick={() => handleBanUser(user.uuid)}
                                        disabled={!user.is_active}
                                    >
                                        {t("Ban")}
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );

}

export default Users;