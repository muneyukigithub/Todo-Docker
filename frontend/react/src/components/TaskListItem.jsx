import { TextField } from '@mui/material'
import React from 'react'

export const TaskListItem = ({ Task, handleChangetaskListItemValue, }) => {

    return (
        <TextField
            inputProps={{
                style: { fontSize: "1.5rem" }
            }}
            fullWidth
            label={"Todoを入力"}
            type="text"
            variant="standard"
            value={Task.task}
            onChange={handleChangetaskListItemValue}
        />
    )
}

