import { v4 as uuid4 } from 'uuid';

export const TASK_NAME = "task"
export const SUBTASK_NAME = "subtask"
export const MOTIVATION_NAME = "motivation"

export const STATUS_WAITING = "waiting"
export const STATUS_INPROGRESS = "inprogress"
export const STATUS_END = "end"


export const TaskCardObj = () => ({ tasklist_id: uuid4(), edit: true, status: STATUS_WAITING, tasklist: [] })
// export const TaskListItemObj = (tasktype: string, task: string): TaskListItemType => ({ tasktype: tasktype, task: task })
export const TaskItemObj = (tasktype, task) => ({ tasktype: tasktype, task: task })
export const SubTaskItemObj = (tasktype, task, checked) => ({ tasktype: tasktype, task: task, checked: checked })

// export const TaskFormItemObj = (tasktype: string, task: string, label: string): TaskFormItemType => ({ tasktype: tasktype, task: task, label: label })

// export const TaskCardObj = (): TaskCardType => ({ tasklist_id: uuid4(), edit: true, status: STATUS_WAITING, tasklist: [], taskform: [] })
// export const TaskListItemObj = (tasktype: string, task: string): TaskListItemType => ({ tasktype: tasktype, task: task })
// export const TaskFormItemObj = (tasktype: string, task: string, label: string): TaskFormItemType => ({ tasktype: tasktype, task: task, label: label })

// export const initialTaskCardFormObj = (): TaskFormCard => ({ id: uuid4(), edit: true, taskformlist: [] })

// export const initialTaskObj = () => ({ task: "", complete: false })
// export const initialSubtaskObj = () => ({ subtask: "", complete: false })
// export const initialMotivationObj = () => ({ motivation: "", complete: false })

// export const initialTaskObj = (value?: any) => ({ type: "task", value: (value ? value : ""), complete: false })
// export const initialSubtaskObj = (value?: any) => ({ type: "subtask", value: (value ? value : ""), complete: false })
// export const initialMotivationObj = (value?: any) => ({ type: "motivation", value: (value ? value : ""), complete: false })

// export const initialTaskFormObj = (name: any, value?: any, label?: any) => ({ type: "task", name: name, label: (label ? label : "タスクを入力してください"), value: (value ? value : "") })
// export const initialSubtaskFormObj = (name: any, value?: any, label?: any) => ({ type: "subtask", name: name, label: (label ? label : "サブタスクを入力してください"), value: (value ? value : "") })
// export const initialMotivationFormObj = (name: any, value?: any, label?: any) => ({ type: "motivation", name: name, label: (label ? label : "モチベーションを入力してください"), value: (value ? value : "") })


// const initialFormObj = (type: any, label: any, value: any, name: any) => ({ type: type, label: label, value: value, name: name })

// export const initialCard = () => 
// export const initialTask = () => ({ id: uuid4(), edit: true, motivation: ["testm"], task: ["testtask"], created_at: "", subtask: [], short: false })
// export const initialSubtask = (subtask = "") => ({ id: uuid4(), suntask: subtask, complete: false })
// export const initialMotivation = (subtask = "") => ({ id: uuid4(), suntask: subtask, complete: false })
