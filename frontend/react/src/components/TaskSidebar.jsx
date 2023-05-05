import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import { Box, Button, Grid, List, ListItem, ListItemButton, Menu, MenuItem } from '@mui/material';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import React, { useState } from 'react';
import styled from 'styled-components';
import { STATUS_END, STATUS_INPROGRESS, STATUS_WAITING } from 'utils/Helper';
import { SidebarTitle } from './SidebarTitle';

export const TaskSidebar = ({
    taskCardList,
    handleCreateTaskCard,
    handleDeleteTaskCard,
    handleSelectTaskCard,
    handleChangeTaskStatus,
    handleCreateProject,
}) => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [menuValue, setMenuValue] = useState(null);
    const open = Boolean(anchorEl);

    const handleClick = (event, value) => {
        setAnchorEl(event.currentTarget);
        setMenuValue(value);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleAction = (func) => {
        func();
        setAnchorEl(null);
    };

    const taskstatus = (taskcard) => {
        if (taskcard.status === STATUS_WAITING) {
            return <Chip label="未着手" size="small" color="primary" />;
        } else if (taskcard.status === STATUS_INPROGRESS) {
            return <Chip label="作業中" size="small" color="error" />;
        } else if (taskcard.status === STATUS_END) {
            return <Chip label="完了" size="small" color="success" />;
        }
    };

    return (
        <SidebarDiv>
            <SidebarTitle handleCreateProject={handleCreateProject} />

            <ActionDiv>
                <Button onClick={handleCreateTaskCard} size={'small'} variant="outlined">
                    <AddIcon />
                    {'Todo追加'}
                </Button>
            </ActionDiv>

            <List sx={{ width: '100%' }}>
                {taskCardList.map((taskcard, i) => {
                    return (
                        <Grid key={taskcard.tasklist_id} container spacing={0} alignItems="center">
                            <Grid item xs={8}>
                                <ListItem
                                    key={taskcard.tasklist_id}
                                    disablePadding
                                    onClick={() => handleSelectTaskCard(i)}
                                >
                                    <ListItemButton>
                                        <ListItemTextDiv>
                                            {taskcard.tasklist[0] && taskcard.tasklist[0].task}
                                        </ListItemTextDiv>
                                    </ListItemButton>
                                </ListItem>
                            </Grid>

                            <Grid item xs={2}>
                                <Button onClick={(event) => handleClick(event, taskcard)}>
                                    {taskstatus(taskcard)}
                                </Button>
                            </Grid>
                            <Grid item xs={2}>
                                <IconButton
                                    edge="end"
                                    aria-label="delete"
                                    onClick={() => handleDeleteTaskCard(taskcard)}
                                >
                                    <DeleteIcon />
                                </IconButton>
                            </Grid>
                        </Grid>
                    );
                })}
            </List>

            <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
                <MenuItem onClick={() => handleAction(() => handleChangeTaskStatus(menuValue, 'waiting'))}>
                    {'未着手にする'}
                </MenuItem>
                <MenuItem onClick={() => handleAction(() => handleChangeTaskStatus(menuValue, 'inprogress'))}>
                    {'作業中にする'}
                </MenuItem>
                <MenuItem onClick={() => handleAction(() => handleChangeTaskStatus(menuValue, 'end'))}>
                    {'完了にする'}
                </MenuItem>
            </Menu>
        </SidebarDiv>
    );
};

const ActionDiv = styled(Box)`
    display: flex;
    justify-content: center;
`;

const ListItemTextDiv = styled.span`
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
`;

const SidebarDiv = styled(Box)`
    border-bottom: 0.5px solid black;
    height: 50vh;
    overflow-y: scroll;
    padding-bottom: 100px;
`;
