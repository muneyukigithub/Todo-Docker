// import { useAuth } from 'AuthContext';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import styled from 'styled-components';


const RegistComplete = () => {
    return (
        <Box
            sx={{
                minHeight: '100vh',
                backgroundColor: '#EEEEEE',
                p: 5,
                mt: 5,
            }}>

            <Typography>ユーザー登録が完了しました。</Typography>
            <LoginLink to="/login">
                {"ログインする"}
            </LoginLink>

        </Box >
    )


}

export default RegistComplete

const LoginLink = styled(RouterLink)`
  text-decoration: none;
  color:#1976d2
`