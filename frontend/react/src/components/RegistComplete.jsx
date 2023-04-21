// import { useAuth } from 'AuthContext';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';

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
            <Link
                component={RouterLink}
                to={"/login"}
                color="primary"
                variant='h6'

                sx={{ textDecoration: "None", pt: 2 }}
            >ログインする
            </Link>
        </Box >
    )


}

export default RegistComplete
