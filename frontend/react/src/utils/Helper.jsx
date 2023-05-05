import { v4 as uuid4 } from 'uuid';

export const TASK_NAME = 'task';
export const SUBTASK_NAME = 'subtask';
export const MOTIVATION_NAME = 'motivation';

export const STATUS_WAITING = 'waiting';
export const STATUS_INPROGRESS = 'inprogress';
export const STATUS_END = 'end';

export const TaskCardObj = () => ({ tasklist_id: uuid4(), edit: true, status: STATUS_WAITING, tasklist: [] });
export const TaskItemObj = (tasktype, task) => ({ tasktype: tasktype, task: task });
export const SubTaskItemObj = (tasktype, task, checked) => ({ tasktype: tasktype, task: task, checked: checked });
