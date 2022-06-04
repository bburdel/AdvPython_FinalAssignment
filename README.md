# Introduction
You are to build a python todo application for your personal use. It will keep track of your tasks and report upon them. 
You can use whatever programming model you deem most appropriate (OO or functions).

## Part 1
The app will be driven by the command line. Thus, you will use simple terminal IO (input and print) as a user interface 
for now. It will support the following commands:

   1. add new task
   2. list tasks
   3. set a start date for the task
   4. set a due date for the task
   5. mark the task as completed
   6. delete a task
   7. change task name
   8. change task description

All tasks will be stored in a database. You can use sqlite, mongodb, or any other database of your choice.

The following data is kept for each task:

1. Task number (not editable after adding)
2. Task name
3. Task descrption
4. Task start date
5. Task due date
6. Task priority
7. Task name and task description are mandatory when adding a new task. 
** All other fields are optional, and can be added via the command line.

The task app must produce the following lists:

1. List all tasks sorted by task number
2. List all tasks sorted by priority
3. List all open tasks sorted by due date
4. List all closed tasks between specified dates
5. List all overdue tasks
6. All lists must be correctly formatted for display in a terminal.

You should develop extensive automated tests as part of building this system.