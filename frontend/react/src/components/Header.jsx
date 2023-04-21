import { Alert, AppBar, Box, Button, Menu, MenuItem, Snackbar, TextField, Toolbar, Typography } from "@mui/material";
import React, { useRef, useState } from "react";
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import styled from "styled-components";
import axios from './defaultaxios';
import { useUser } from "./UserContext";

export const Header = ({ headerHeight }) => {

  const [userDeleteError, setUserDeleteError] = useState(false);
  const [logoutError, setLogoutError] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const popupref = useRef();
  const UserContext = useUser();
  const navigate = useNavigate();

  const email = UserContext?.user?.email
  const userid = UserContext?.user?.id
  const logout = UserContext.logout
  const open = Boolean(anchorEl);


  const handleLogout = async () => {
    setAnchorEl(null)

    try {
      await axios.get("/jwt_deletetoken/")
      logout()
      navigate("/logoutcomplete/")
    } catch (error) {
      setLogoutError(true)
      console.log(error)
    }
  }


  const handleDeleteUser = async () => {
    setShowPopup(false);
    try {
      await axios.delete(`userdelete/?userid=${userid}`)
      logout()
      navigate("userdeletecomplete/")
    } catch (error) {
      setUserDeleteError(true)
      console.log(error)
    }
  }


  const handleDeleteUserComfirm = () => {
    setAnchorEl(null);
    setShowPopup(true);
  }

  const handleSetAnchor = (event) => {
    setAnchorEl(event.currentTarget);
    // setMenuValue(value);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
  };

  const handleCloseLogoutSnack = () => {
    setLogoutError(false);
  };


  const handleCloseUserDeleteSnack = () => {
    setUserDeleteError(false);
  };

  const handleClosePopup = (e) => {
    if (popupref.current && !popupref.current.contains(e.target)) {
      setShowPopup(false);

    }
  }




  return (
    <HeaderDiv headerHeight={headerHeight}>
      <Toolbar>
        <FrontLink to="/">{"Todo管理"}</FrontLink>


        <MenuDiv>
          {email ?
            <Button onClick={handleSetAnchor}>{email}</Button>
            : <LoginLink to="/login">
              <LoginButton variant="outlined" >
                {"ログイン"}
              </LoginButton>
            </LoginLink>

          }


        </MenuDiv>
      </Toolbar>


      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleCloseMenu}
      >
        <MenuItem onClick={handleLogout}>{"ログアウト"}</MenuItem>
        <MenuItem onClick={handleDeleteUserComfirm}>{"アカウント削除"}</MenuItem>

      </Menu>

      <Snackbar open={userDeleteError} autoHideDuration={6000} onClose={handleCloseUserDeleteSnack}>
        <Alert elevation={6} variant={"filled"} severity={"error"}>
          {"アカウント削除に失敗しました"}

        </Alert>
      </Snackbar>

      <Snackbar open={logoutError} autoHideDuration={6000} onClose={handleCloseLogoutSnack}>
        <Alert elevation={6} variant={"filled"} severity={"error"}>
          {"ログアウトに失敗しました"}

        </Alert>
      </Snackbar>

      {showPopup && <Overlay onClick={handleClosePopup}>
        <Popup ref={popupref}>
          <Typography color="black">{email}</Typography>
          <Button onClick={handleDeleteUser}>{"このアカウントを削除しますか？"}</Button>
        </Popup>
      </Overlay>
      }
    </HeaderDiv>
  )
};



// const HeaderDiv = styled(AppBar)<{headerHeight}>`
const HeaderDiv = styled(AppBar)`
background-color: #fff;
position: fixed;
top:0;
height: ${(props) => props.headerHeight}px;
box-shadow: none;
border-bottom: 0.5px solid gray;
`;

const LoginButton = styled(Button)`
border-radius: 32px;
/* background-color: gray; */
color:gray;
border:1px solid gray;
font-weight: bold;
`

const LoginLink = styled(RouterLink)`
  text-decoration: none;
  color:#1976d2
`


const MenuDiv = styled(Box)`
display: flex;
flex-grow: 1;
justify-content: end;
`

const FrontLink = styled(RouterLink)`
text-decoration: none;
color:gray;
font-size: 1rem;
font-weight: bold;
`




const Overlay = styled(Box)`
/* z-index: 1200; */
position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(241, 241, 241, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
`

const Popup = styled(Box)`
/* z-index: 8200; */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
padding: 20px;
  background-color: white;

border: 1px solid black;
  width: 400px;
  height:200px
`