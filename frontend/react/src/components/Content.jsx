import { Box, Typography } from '@mui/material'
import React from 'react'
import styled from "styled-components"
import { ContentTitle } from './ContentTitle'
import { TaskList } from './TaskList'

export const Content = ({
  selectedTaskCard,
  drawerWidth,
  headerHeight,
  handleAddSubtask,
  handleChangeListItemChecked,
  handleDeleteListItem,
  handleChangetaskListItemValue
}) => {

  const TaskCardContent = selectedTaskCard
    ? <TaskList
      selectedTaskCard={selectedTaskCard}
      handleAddSubtask={handleAddSubtask}
      handleChangeListItemChecked={handleChangeListItemChecked}
      handleDeleteListItem={handleDeleteListItem}
      handleChangetaskListItemValue={handleChangetaskListItemValue}

    />
    : <Typography>{"タスクは選択されていません"}</Typography>

  return (
    <ContentWrapper headerHeight={headerHeight} drawerWidth={drawerWidth}>
      <ContentTitle title={"Todo"} />
      <ContentContent>
        {TaskCardContent}
      </ContentContent>
    </ContentWrapper>

  )
}



// const ContentWrapper = styled.div < { drawerWidth, headerHeight } > `
const ContentWrapper = styled.div`
  width: calc(100% - ${props => props.drawerWidth}px);
  position: relative;
  top: ${props => props.headerHeight}px;
`

const ContentContent = styled(Box)`
padding: 0 30px;
`