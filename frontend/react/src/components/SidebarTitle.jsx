import MoreHoriz from '@mui/icons-material/MoreHoriz';
import { Alert, Box, Button, Menu, MenuItem, Snackbar, TextField, Typography } from "@mui/material";
import React, { useRef, useState } from "react";
import styled from "styled-components";

export const SidebarTitle = ({ handleCreateProject }) => {
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);
    const [projectTitle, setProjectTitle] = useState("");
    const [showPopup, setShowPopup] = useState(false);
    const popupref = useRef()
    const [successOpen, setSuccessOpen] = useState(false);
    const [failOpen, setfailOpen] = useState(false);


    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };


    const handleCreateProject_wrap = async () => {
        setShowPopup(false)
        try {
            await handleCreateProject(projectTitle)
            setSuccessOpen(true);
            // handleGetProject()

        } catch (error) {
            console.log(error)
            setfailOpen(true)
        }
    }



    const handleSaveClick = () => {
        setAnchorEl(null);
        setShowPopup(true);
    }

    const handlePopupClose = (e) => {
        console.log("touch")
        if (popupref.current && !popupref.current.contains(e.target)) {
            setShowPopup(false);
            setProjectTitle("");
        }
    }


    const handleChangeProjectTitle = (e) => {
        setProjectTitle(e.target.value)
    }

    const handleCloseSnackbar = () => {
        setSuccessOpen(false);
        setfailOpen(false);
    };






    return (
        <TitleDiv>

            <Snackbar open={successOpen} autoHideDuration={6000} onClose={handleCloseSnackbar}>
                <Alert elevation={6} variant={"filled"} severity="success">
                    {"Todoリストの保存が完了しました。"}

                </Alert>
            </Snackbar>


            <Snackbar open={failOpen} autoHideDuration={6000} onClose={handleCloseSnackbar}>
                <Alert elevation={6} variant={"filled"} severity={"error"}>
                    {"Todoリストの保存が失敗しました。"}

                </Alert>
            </Snackbar>


            <Box>
                <Title>{"Todoリスト"}</Title>
            </Box>
            <MenuDiv>
                <Button size={"small"} onClick={handleClick}>
                    <MoreHoriz />
                </Button>
            </MenuDiv>


            {showPopup && <Overlay onClick={handlePopupClose}>
                <Popup ref={popupref}>
                    <Typography color="black">{"保存するTodoリスト名"}</Typography>
                    <TextField fullWidth onChange={handleChangeProjectTitle} />
                    <Button onClick={handleCreateProject_wrap}>保存する</Button>
                </Popup>
            </Overlay>
            }


            <Menu
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
            >

                <MenuItem onClick={handleSaveClick}>{"Todoリストを保存する"}</MenuItem>
            </Menu>

        </TitleDiv>

    )
}

const TitleDiv = styled(Box)`
display: flex;
justify-content: start;
border-bottom: 0.5px solid black;
margin: 30px ;
padding-bottom: 20px;
`
const Title = styled(Typography)`
font-size: 1.0rem;
color: #827f7f;
font-weight: lighter;

`

const MenuDiv = styled(Box)`
display: flex;
flex-grow: 1;
justify-content: end;
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
/* z-index: 5000; */
  display: flex;
  flex-direction: column;
  justify-content: center;
padding: 20px;
  background-color: white;

border: 1px solid black;
  width: 400px;
  height:200px
`