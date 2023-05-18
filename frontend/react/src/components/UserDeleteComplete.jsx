import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import styled from 'styled-components';

export const UserDeleteComplete = () => {
    return (
        <Box
            sx={{
                minHeight: '100vh',
                backgroundColor: '#EEEEEE',
                p: 5,
                mt: 5,
            }}
        >
            <Typography>ユーザー削除が完了しました。</Typography>

            <LogoutLink to="/">{'メイン画面へ戻る'}</LogoutLink>
        </Box>
    );
};

const LogoutLink = styled(RouterLink)`
    text-decoration: none;
    color: #1976d2;
`;
