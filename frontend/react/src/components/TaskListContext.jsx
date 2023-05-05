import React, { createContext } from 'react';
import { useState } from 'react';
import { useContext } from 'react';

const TaskListContext = createContext(null);

export const useTaskList = () => {
    return useContext(TaskListContext);
};

export const TaskListProvider = ({ children }) => {
    const [taskCardList, setTaskCardList] = useState([]);

    const value = {
        tasklist: taskCardList,
        setTasklist: setTaskCardList,
    };

    return <TaskListContext.Provider value={value}>{children}</TaskListContext.Provider>;
};
