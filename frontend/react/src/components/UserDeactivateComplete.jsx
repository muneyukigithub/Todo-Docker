import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';

const UserDeactivateComplete = () => {
    const username = location.state.username;

    return (
        <Box
            sx={{
                minHeight: '100vh',
                backgroundColor: '#EEEEEE',
                p: 5,
            }}
        >
            <Typography>ユーザー退会が完了しました。</Typography>
            <Typography gutterBottom>{username}</Typography>
            <Link
                component={RouterLink}
                to={'/'}
                color="primary"
                variant="h6"
                sx={{ textDecoration: 'None', pt: 2 }}
            >
                メイン画面へ戻る
            </Link>
            <CssBaseline />
        </Box>
    );
};

export default UserDeactivateComplete;
