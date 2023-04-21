import { Checkbox, TextField } from '@mui/material';
import React from 'react';
export const SubtaskListItem = ({ Task, handleChangetaskListItemValue, handleChangeListItemChecked }) => {
    return <>
        <Checkbox checked={Task.checked} onChange={handleChangeListItemChecked} />
        <TextField
            sx={{ borderLeft: "0.5px dashed black", padding: "0.5rem" }}
            InputProps={{
                disableUnderline: true,
                style: {
                    color: Task.checked ? 'gray' : "black",
                    textDecoration: Task.checked ? "line-through" : "none",
                }
            }}
            fullWidth
            type="text"
            variant="standard"
            value={Task.task}
            onChange={handleChangetaskListItemValue}
        />
    </>
}


