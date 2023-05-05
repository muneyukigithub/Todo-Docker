import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import { Button, Grid, IconButton } from '@mui/material';
import React from 'react';
import styled from 'styled-components';
import { TASK_NAME } from 'utils/Helper';
import { SubtaskListItem } from './SubtaskListItem';
import { TaskListItem } from './TaskListItem';

export const TaskList = ({
    selectedTaskCard,
    handleAddSubtask,
    handleChangeListItemChecked,
    handleDeleteListItem,
    handleChangetaskListItemValue,
}) => {
    const selectList = (task, index) => {
        if (task.tasktype === TASK_NAME) {
            return (
                <Grid item xs={12}>
                    <TaskListItem
                        key={index}
                        Task={task}
                        handleChangetaskListItemValue={(e) =>
                            handleChangetaskListItemValue(selectedTaskCard, e.target.value, index)
                        }
                    />
                </Grid>
            );
        } else {
            return (
                <Grid item xs={12} display={'flex'} borderBottom={'0.5px solid black'}>
                    <SubtaskListItem
                        key={index}
                        Task={task}
                        handleChangetaskListItemValue={(e) =>
                            handleChangetaskListItemValue(selectedTaskCard, e.target.value, index)
                        }
                        handleChangeListItemChecked={() => handleChangeListItemChecked(selectedTaskCard, index)}
                    />

                    <IconButton onClick={() => handleDeleteListItem(selectedTaskCard, index)}>
                        <DeleteIcon />
                    </IconButton>
                </Grid>
            );
        }
    };

    return (
        <>
            <Grid container spacing={0} alignItems="center">
                {selectedTaskCard.tasklist &&
                    selectedTaskCard.tasklist.map((List, index) => {
                        return <>{selectList(List, index)}</>;
                    })}
            </Grid>

            <SubtaskCreateButton
                onClick={() => {
                    handleAddSubtask(selectedTaskCard);
                }}
            >
                <AddIcon />
                {'Todoを細かくする'}
            </SubtaskCreateButton>
        </>
    );
};

const SubtaskCreateButton = styled(Button)`
    color: gray;
`;
