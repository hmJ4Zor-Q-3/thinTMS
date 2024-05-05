//v3.0

// Function to add a new group to the select dropdown
function addGroupToSelect(groupName) {
    // Create a new option element
    var option = document.createElement('option');
    option.value = groupName;
    option.textContent = groupName;

    // Append the option to the select element
    document.getElementById('group-select').appendChild(option);
}

// Function to filter tasks based on a group name
function filterTasks(groupName) {
    // Get all tasks
    var tasks = document.querySelectorAll('#task-list li');

    // Loop through the tasks
    tasks.forEach(function(task) {
        // If the "All" group is selected, show all tasks
        if (groupName === 'All') {
            task.style.display = '';
        }
        // Otherwise, show only tasks in the selected group
        else if (task.dataset.group === groupName) {
            task.style.display = '';
        }
        // Hide tasks in other groups
        else {
            task.style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    let returnToHomepage = () => window.location.href = $("#var_homepage_route").html();
    document.addEventListener(LOGOUT_EVENT_NAME, returnToHomepage);
    if(!hasSession())
        returnToHomepage(); 
 
    // Event listener for the "Create Group" button
    document.getElementById('create-group').addEventListener('click', function(event) {
        // Get the new group name from the input field
        var newGroupName = document.getElementById('new-group-name').value;

         // If the group name is empty or contains only whitespace, display an error message and return
        if (!newGroupName.trim()) {
            alert('Group name must contain at least one non-whitespace character.');
            return;
        }

        // Add the new group to the select dropdown
        addGroupToSelect(newGroupName);

        // Create a new div for the group
        var groupDiv = document.createElement('div');
        groupDiv.textContent = newGroupName;
        groupDiv.classList.add('group-item'); // Add a class to style the group div as a button
        groupDiv.dataset.group = newGroupName; // Add a data attribute to store the group name

        // Add a click event listener to the group div
        groupDiv.addEventListener('click', function() {
            // Filter the tasks based on the group name
            filterTasks(newGroupName);
        });

        // Append the group div to the groups container
        document.getElementById('groups-container').appendChild(groupDiv);
    });

    // Create an "All Tasks" button
    var allTasksButton = document.createElement('button');
    allTasksButton.textContent = 'All Tasks';
    allTasksButton.classList.add('group-item'); // Add a class to style the button

    // Add a click event listener to the button
    allTasksButton.addEventListener('click', function() {
        // Show all tasks
        filterTasks('All');

    // Hide the placeholder text and image
    document.getElementById('placeholder').style.display = 'none';
    document.getElementById('placeholder-image').style.display = 'none';
    });

    // Add the button to the group toolbar
    document.getElementById('groups-container').appendChild(allTasksButton);

    document.getElementById('add-task').addEventListener('click', function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Get the selected group
        var selectedGroup = document.getElementById('group-select').value;

        // If no group is selected, show an alert
        if (!selectedGroup) {
            alert('Please select a group before adding a task.');
            return; // Prevent the rest of the code from executing
        }

        // Get the task details from the input fields
        var taskName = document.getElementById('task-name').value;
        var taskDesc = document.getElementById('task-desc').value;

        // Get the due date, create a Date object from it, and format it as "Month Day, Year"
        var taskDueDate = document.getElementById('due-date').value;
        var taskDueDateString = '';
        if (taskDueDate) {
            var dueDate = new Date(taskDueDate);
            var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
            taskDueDateString = ' &nbsp; &nbsp; Due Date: ' + monthNames[dueDate.getMonth()] + ' ' + dueDate.getDate().toString() + ', ' + dueDate.getFullYear();
        }

        // Get the task time, create a Date object from it, and format it as AM/PM
        var taskTime = document.getElementById('new-task-time').value;
        var taskTimeString = '';
        if (taskTime) {
            var time = new Date('1970-01-01T' + taskTime + 'Z');
            var hours = time.getUTCHours();
            var minutes = time.getUTCMinutes();
            var ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12;
            hours = hours ? hours : 12; // the hour '0' should be '12'
            minutes = minutes < 10 ? '0'+minutes : minutes;
            taskTimeString = ' &nbsp; Time: ' + hours + ':' + minutes + ' ' + ampm;
        }

        // Create a new list item for the task
        var taskItem = document.createElement('li');
        taskItem.dataset.group = selectedGroup; // Add a data attribute to store the group name

        // Create a string with the task details and add it to the list item
        taskItem.innerHTML = `${taskName}: <br> -&nbsp;&nbsp;${taskDesc} <br><br> ${taskDueDateString}${taskTimeString} 

        <button class="edit-task">Edit Task</button> <button class="delete-task">Delete Task</button>`;

        // Add the task item to the task list
        document.getElementById('task-list').appendChild(taskItem);

        // Add event listeners to the buttons
        taskItem.querySelector('.edit-task').addEventListener('click', function() {
            // Prompt the user to enter new task details
            var newTaskName = prompt('Enter a new task name:', taskName);
            var newTaskDesc = prompt('Enter a new task description:', taskDesc);
            var newTaskDueDate = prompt('Enter a new due date:', taskDueDate);
            var newTaskTime = prompt('Enter a new time:', taskTime);

            // Update the task details
            taskName = newTaskName || taskName;
            taskDesc = newTaskDesc || taskDesc;
            taskDueDate = newTaskDueDate || taskDueDate;
            taskTime = newTaskTime || taskTime;

            // Generate the due date string
            var taskDueDateString = '';
            if (taskDueDate) {
                var dueDate = new Date(taskDueDate);
                var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                taskDueDateString = ' &nbsp; &nbsp; Due Date: ' + monthNames[dueDate.getMonth()] + ' ' + dueDate.getDate().toString() + ', ' + dueDate.getFullYear();
            }

            // Generate the task time string
            var taskTimeString = '';
            if (taskTime) {
                var time = new Date('1970-01-01T' + taskTime + 'Z');
                var hours = time.getUTCHours();
                var minutes = time.getUTCMinutes();
                var ampm = hours >= 12 ? 'PM' : 'AM';
                hours = hours % 12;
                hours = hours ? hours : 12; // the hour '0' should be '12'
                minutes = minutes < 10 ? '0'+minutes : minutes;
                taskTimeString = ' &nbsp; Time: ' + hours + ':' + minutes + ' ' + ampm;
            }

            // Update the task item
            taskItem.innerHTML = `${taskName}: <br> -&nbsp;&nbsp;${taskDesc} <br><br> ${taskDueDateString}${taskTimeString} 
            <button class="edit-task">Edit Task</button> <button class="delete-task">Delete Task</button>`;
        });

        taskItem.querySelector('.delete-task').addEventListener('click', function() {
            // Remove the task item from the task list
            document.getElementById('task-list').removeChild(taskItem);
        });

        // Hide the placeholder text
        document.getElementById('placeholder').style.display = 'none';
    });

    document.getElementById('task-list').addEventListener('click', function(event) {
        // Check if the clicked element is a "Delete Task" button
        if (event.target.classList.contains('delete-task')) {
            // Get the task item
            var taskItem = event.target.parentElement;
    
            // Remove the task item from the task list
            this.removeChild(taskItem);
        }
    });
});