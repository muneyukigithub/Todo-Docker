import { Box, Snackbar } from '@mui/material'
import Alert from '@mui/material/Alert'
import { Content } from './Content'
import axios from './defaultaxios'
import React, { useState } from 'react'
import { TaskSidebar } from './TaskSidebar'
import { HistoryTaskSidebar } from './HistoryTaskSidebar'
import styled from "styled-components"
import { SUBTASK_NAME, TaskCardObj, TaskItemObj, SubTaskItemObj, TASK_NAME } from 'utils/Helper';

export const MainLayout = ({ drawerWidth, headerHeight }) => {
  const [taskCardList, setTaskCardList] = useState([]);
  const [historydata, setHistoryData] = useState([]);
  const [select, setSelect] = useState(null);
  const [successOpen, setSuccessOpen] = useState(false);
  const [failOpen, setfailOpen] = useState(false);

  const handleGetProject = async () => {
    try {
      const response = await axios.get("/projectlist/");
      setHistoryData(response.data)
    } catch (error) {
      console.log(error)
    }
  }

  const handleDeleteProject = async (project) => {
    try {
      await axios.delete(`projectdelete/?project=${project}`)
      handleGetProject()
    } catch (error) {
      console.log(error)
    }
  }


  const handleRestoreProject = async (project) => {
    try {
      const response = await axios.get(`project/?project=${project}`)
      setTaskCardList(response.data.projectData)
    } catch (error) {
      console.log(error)
      throw error
    }
  }

  const handleCreateProject = async (project) => {
    const projectobj = { project: project, projectData: taskCardList }
    const jsonproject = JSON.stringify(projectobj)

    try {
      await axios.post("projectcreate/", jsonproject, { headers: { "Content-Type": "application/json" } })

      // setSuccessOpen(true);
      handleGetProject()

    } catch (error) {
      console.log(error)
      throw error
      // setfailOpen(true)
    }
  }


  const handleDeleteTaskCard = (taskcard) => {
    setTaskCardList((prevtaskcardlist) => (prevtaskcardlist.filter((prevtaskcard) => prevtaskcard.tasklist_id !== taskcard.tasklist_id)))
  }


  const handleCreateTaskCard = () => {
    const newTaskCard = TaskCardObj()
    newTaskCard.tasklist.push(TaskItemObj(TASK_NAME, "未設定"))
    setTaskCardList([...taskCardList, newTaskCard])
  }

  const handleSelectTaskCard = (selectindex) => {
    setSelect(selectindex)
  }

  const handleChangeTaskStatus = (taskcard, status) => {
    setTaskCardList((prevtaskcardlist) => (prevtaskcardlist.map((prevtaskcard) => (prevtaskcard.tasklist_id === taskcard.tasklist_id ? { ...prevtaskcard, status: status } : prevtaskcard))))
  }


  // const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
  //   if (reason === 'clickaway') {
  //     return;
  //   }

  //   setSuccessOpen(false);
  //   setfailOpen(false);

  // };




  const handleAddSubtask = (targetTaskCard) => {
    setTaskCardList((taskCardList) => (
      taskCardList.map((taskCard) => {
        if (taskCard.tasklist_id === targetTaskCard.tasklist_id) {
          return { ...taskCard, tasklist: [...taskCard.tasklist, SubTaskItemObj(SUBTASK_NAME, "", false)] }
        } else {
          return taskCard
        }
      })))
  }

  const handleChangeListItemChecked = (targetTaskCard, targetindex) => {
    setTaskCardList((taskCardList) => (
      taskCardList.map((taskCard) => {
        if (taskCard.tasklist_id === targetTaskCard.tasklist_id) {

          const newtaskList = taskCard.tasklist.map((task, task_index) => (
            (task_index === targetindex) ? { ...task, checked: !task.checked } : task
          ))
          return { ...taskCard, tasklist: newtaskList }

        } else {
          return taskCard
        }
      }
      )
    ))
  }

  const handleDeleteListItem = (targetTaskCard, targetindex) => {
    setTaskCardList((taskCardList) => (
      taskCardList.map((taskCard) => {
        if (taskCard.tasklist_id === targetTaskCard.tasklist_id) {
          const newtaskList = taskCard.tasklist.filter((List, index) => { return index !== targetindex })
          return { ...taskCard, tasklist: newtaskList }
        } else {
          return taskCard
        }
      })
    ))
  }

  const handleChangetaskListItemValue = (targetTaskCard, inputValue, targetindex) => {
    setTaskCardList((TaskCardList) => (
      TaskCardList.map((taskCard) => {
        console.log(taskCard.tasklist_id, targetTaskCard.tasklist_id)

        if (taskCard.tasklist_id === targetTaskCard.tasklist_id) {
          const newtaskList = targetTaskCard.tasklist.map((task, task_index) => (
            (task_index === targetindex) ? { ...task, task: inputValue } : task
          ))
          return { ...taskCard, tasklist: newtaskList }
        } else {
          return taskCard
        }
      }))
    )
  }




  return (
    <MainLayoutWrapper>
      {/* <Snackbar open={successOpen} autoHideDuration={6000} onClose={handleClose}>
        <Alert elevation={6} variant={"filled"} severity="success">
          {"保存が完了しました。"}

        </Alert>
      </Snackbar>


      <Snackbar open={failOpen} autoHideDuration={6000} onClose={handleClose}>
        <Alert elevation={6} variant={"filled"} severity={"error"}>
          {"保存が失敗しました。"}

        </Alert>
      </Snackbar> */}

      <SidebarWrapper drawerWidth={drawerWidth}>
        <TaskSidebar
          taskCardList={taskCardList}
          handleCreateTaskCard={handleCreateTaskCard}
          handleDeleteTaskCard={handleDeleteTaskCard}
          handleSelectTaskCard={handleSelectTaskCard}
          handleChangeTaskStatus={handleChangeTaskStatus}
          handleCreateProject={handleCreateProject}
        />
        <HistoryTaskSidebar
          historydata={historydata}
          handleRestoreProject={handleRestoreProject}
          handleGetProject={handleGetProject}
          handleDeleteProject={handleDeleteProject}
        />
      </SidebarWrapper>

      <Content
        selectedTaskCard={select !== null ? taskCardList[select] : null}
        drawerWidth={drawerWidth}
        headerHeight={headerHeight}
        handleAddSubtask={handleAddSubtask}
        handleChangeListItemChecked={handleChangeListItemChecked}
        handleDeleteListItem={handleDeleteListItem}
        handleChangetaskListItemValue={handleChangetaskListItemValue}
      />

    </MainLayoutWrapper >
  )
}


const MainLayoutWrapper = styled.div`
min-height: 100vh;
display: flex;
justify-content: end;
color:gray;
`;

// const SidebarWrapper = styled.div < { drawerWidth } > `
const SidebarWrapper = styled.div`
z-index: 100;
height: 100vh;
/* overflow-y: auto; */
background-color:#f0f0f0;
position: fixed;
left:0;
top:64px;
width: ${(props) => props.drawerWidth}px;
`


