import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Link from '@mui/material/Link';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import React, { useEffect, useRef, useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import axios from './defaultaxios';
import { Snackbar, styled } from '@mui/material';
import Alert from '@mui/material/Alert';

const Register = () => {
  const navigate = useNavigate();
  const [userValid, setUserValid] = useState(true);
  const [passwordValid, setPasswordValid] = useState(true);
  const [password2Valid, setPassword2Valid] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [successOpen, setSuccessOpen] = useState(false);
  const [failOpen, setfailOpen] = useState(false);

  const handleSubmit = async (e) => {

    // ユーザー登録 (情報キーと代入変数名が同じとき、キーを省略できる)
    const sendData = {
      email,
      password,
      password2
    }

    try {
      await axios.post("usercreate/", sendData, { headers: { "Content-Type": "application/json" } })
      navigate("/registcomplete")

      // setSuccessOpen(true)

    } catch (error) {
      setfailOpen(true)
      console.log(error)
    }


  }

  const handleChangeEmail = (e) => {
    setEmail(e.target.value);
    setUserValid(e.target.validity.valid)
  }

  const handleChangePassword = (e) => {
    setPassword(e.target.value)
    setPasswordValid(e.target.validity.valid)
  }

  const handleChangePassword2 = (e) => {
    setPassword2(e.target.value)
    setPassword2Valid(e.target.validity.valid)

  }

  const handleClose = () => {
    setSuccessOpen(false);
    setfailOpen(false);
  };

  return (
    <Container component="main" maxWidth="xs">

      <Snackbar open={successOpen} autoHideDuration={6000} onClose={handleClose}>
        <Alert elevation={6} variant={"filled"} severity="success">
          {"ユーザー登録が完了しました。"}

        </Alert>
      </Snackbar>


      <Snackbar open={failOpen} autoHideDuration={6000} onClose={handleClose}>
        <Alert elevation={6} variant={"filled"} severity={"error"}>
          {"ユーザー登録が失敗しました。"}

        </Alert>
      </Snackbar>

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
          {"新規登録"}
        </Typography>

        {/* <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}> */}
        <Box sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                error={!userValid}
                helperText={!userValid && "メールアドレスの形式で入力してください"}
                // helperText={inputRef?.current?.validationMessage}
                inputProps={{ maxLength: 50, pattern: "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*.)+[a-zA-Z]{2,}$" }}
                onChange={handleChangeEmail}
                // inputRef={inputRef}
                required
                fullWidth
                id="email"
                label="メールアドレス"
                name="email"
                autoComplete="email"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                error={!passwordValid}
                helperText={!passwordValid && "8文字以上入力してください"}
                inputProps={{ minLength: 8 }}
                required
                fullWidth
                name="password"
                label="パスワード"
                type="password"
                id="password"
                autoComplete="new-password"
                onChange={handleChangePassword}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                error={!password2Valid}
                helperText={!password2Valid && "8文字以上入力してください"}
                inputProps={{ minLength: 8 }}
                required
                fullWidth
                name="password2"
                label="確認用パスワード"
                type="password"
                id="password2"
                autoComplete="new-password"
                onChange={handleChangePassword2}

              />
            </Grid>
          </Grid>
          <Button
            // type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            onClick={handleSubmit}
          >
            {"ユーザー作成する"}
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <LoginLink to="/login">
                {"ログインする"}
              </LoginLink>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  )
}

export default Register



const LoginLink = styled(RouterLink)`
  text-decoration: none;
  color:#1976d2
`
