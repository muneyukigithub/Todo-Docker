import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { Alert, Snackbar, styled } from '@mui/material';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import React from 'react';
import { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import axios from './defaultaxios';
import { useUser } from './UserContext';

export default function SignIn() {
    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(false);

    const UserContext = useUser();
    const navigate = useNavigate();

    const handleChangeUser = (event) => {
        setUser(event.target.value);
    };

    const handleChangePassword = (event) => {
        setPassword(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        // エラー処理のためcatchは必要
        try {
            const response = await axios.post(
                'jwt_createtoken/',
                {
                    email: user,
                    password: password,
                },
                { headers: { 'Content-Type': 'application/json' } }
            );

            if (response.status === 200) {
                const response = await axios.get('/jwt_userinfo/');
                const userinfo = response.data;
                userinfo && localStorage.setItem('userinfo', JSON.stringify(userinfo));
                UserContext.setUser(userinfo);
                navigate('/main');
            }
        } catch (error) {
            setError(true);
        }
    };

    const handleClose = () => {
        setError(false);
    };

    return (
        <Container component="main" maxWidth="xs">
            <Box
                sx={{
                    marginTop: 15,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    {'ログイン'}
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                    {/* {error && <Alert severity="error" onClose={() => { setError(false) }}>
                        ユーザ名かパスワードが間違っています
                    </Alert>
                    } */}

                    <TextField
                        onChange={handleChangeUser}
                        inputProps={{
                            maxLength: 20,
                            pattern: '^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*.)+[a-zA-Z]{2,}$',
                        }}
                        margin="normal"
                        required
                        fullWidth
                        type="text"
                        id="email"
                        label="メールアドレス"
                        name="email"
                        autoComplete="email"
                        autoFocus
                    />
                    <TextField
                        onChange={handleChangePassword}
                        required
                        fullWidth
                        name="password"
                        label="パスワード"
                        type="password"
                        id="password"
                        autoComplete="off"
                    />

                    <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }} onSubmit={handleSubmit}>
                        {'ログインする'}
                    </Button>

                    <Box display={'flex'} justifyContent={'end'}>
                        <RegisterLink to="/regist/">{'新規登録する'}</RegisterLink>
                    </Box>
                </Box>
            </Box>
            <Snackbar open={error} autoHideDuration={6000} onClose={handleClose}>
                <Alert elevation={6} variant={'filled'} severity={'error'}>
                    {'ログインが失敗しました'}
                </Alert>
            </Snackbar>
        </Container>
    );
}

const RegisterLink = styled(RouterLink)`
    text-decoration: none;
    color: #1976d2;
`;
