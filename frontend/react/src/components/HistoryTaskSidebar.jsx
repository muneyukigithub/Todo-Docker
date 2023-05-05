import React, { useEffect, useRef, useState } from 'react';
import { Alert, Box, Button, Grid, List, ListItem, ListItemButton, Snackbar, Typography } from '@mui/material';
import styled from 'styled-components';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import { useUser } from './UserContext';

export const HistoryTaskSidebar = ({ historydata, handleRestoreProject, handleGetProject, handleDeleteProject }) => {
    const [loading, setLoading] = useState(true);
    const [projectTitle, setProjectTitle] = useState('');
    const [showPopup, setShowPopup] = useState(false);
    const [successOpen, setSuccessOpen] = useState(false);
    const [failOpen, setfailOpen] = useState(false);
    const [getProjectError, setGetProjectError] = useState(false);
    const popupref = useRef();
    const UserContext = useUser();

    const handleConfirm = (project) => {
        setProjectTitle(project);
        setShowPopup(true);
    };

    const handleReadProject = async () => {
        setShowPopup(false);
        setProjectTitle('');

        try {
            await handleRestoreProject(projectTitle);
            setSuccessOpen(true);
        } catch (error) {
            setfailOpen(true);
        }
    };

    const handlePopupClose = (e) => {
        if (popupref.current && !popupref.current.contains(e.target)) {
            setShowPopup(false);
            setProjectTitle('');
        }
    };

    const handleCloseReadProjectSnack = () => {
        setSuccessOpen(false);
        setfailOpen(false);
    };

    useEffect(() => {
        const handleHistory = async () => {
            try {
                if (UserContext?.user) {
                    await handleGetProject();
                }

            } catch (error) {
                setGetProjectError(true);
            } finally {
                setLoading(false);
            }
        };


        handleHistory();
    }, []);

    if (loading) return <p>...loading</p>;

    return (
        <SidebarDiv>
            <Snackbar open={successOpen} autoHideDuration={6000} onClose={handleCloseReadProjectSnack}>
                <Alert elevation={6} variant={'filled'} severity="success">
                    {'Todoリストの読み込みが完了しました'}
                </Alert>
            </Snackbar>

            <Snackbar open={failOpen} autoHideDuration={6000} onClose={handleCloseReadProjectSnack}>
                <Alert elevation={6} variant={'filled'} severity={'error'}>
                    {'Todoリストの読み込みが失敗しました'}
                </Alert>
            </Snackbar>

            <SidebarTitleDiv>
                <SidebarTitle>{'保存したTodoリスト'}</SidebarTitle>
            </SidebarTitleDiv>

            <List sx={{ width: '100%' }}>
                {historydata.length ? (
                    historydata.map((historyproject, i) => {
                        return (
                            <Grid key={i} container spacing={0} alignItems="center">
                                <Grid item xs={10}>
                                    <ListItem disablePadding onClick={() => handleConfirm(historyproject.project)}>
                                        <ListItemButton>
                                            <ListItemTextDiv>{historyproject.project}</ListItemTextDiv>
                                        </ListItemButton>
                                    </ListItem>
                                </Grid>
                                <Grid item xs={2}>
                                    <IconButton
                                        edge="end"
                                        aria-label="delete"
                                        onClick={() => handleDeleteProject(historyproject.project)}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </Grid>
                            </Grid>
                        );
                    })
                ) : getProjectError ? (
                    <Typography sx={{ textAlign: 'center' }}>{'保存情報の取得中にエラーが発生しました'}</Typography>
                ) : (
                    <Typography sx={{ textAlign: 'center' }}>{'保存されているTodoリストはありません'}</Typography>
                )}
            </List>

            {showPopup && (
                <Overlay onClick={handlePopupClose}>
                    <Popup ref={popupref}>
                        <Typography color="black">{projectTitle}</Typography>
                        <Typography>このTodoリストを読み込みますか？</Typography>
                        <Button onClick={handleReadProject}>読み込む</Button>
                    </Popup>
                </Overlay>
            )}
        </SidebarDiv>
    );
};

const Overlay = styled(Box)`
    z-index: 1200;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(241, 241, 241, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
`;

const Popup = styled(Box)`
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 20px;
    background-color: white;

    border: 1px solid black;
    width: 400px;
    height: 200px;
`;

const ListItemTextDiv = styled.span`
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
`;

const SidebarDiv = styled(Box)`
    height: 50vh;
    overflow-y: scroll;
    padding-bottom: 100px;
`;

const SidebarTitleDiv = styled(Box)`
    display: flex;
    justify-content: center;
`;

const SidebarTitle = styled(Typography)`
    font-size: 1rem;
    width: 100%;
    color: #827f7f;
    font-weight: lighter;
    border-bottom: 0.5px solid black;
    margin: 30px;
    padding-bottom: 20px;
`;
