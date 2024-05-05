// When the login button is clicked, redirect to the login page
document.getElementById('login-button').addEventListener('click', function() {
    window.location.href = 'login.html';
});

// When the register button is clicked, redirect to the register page
document.getElementById('register-button').addEventListener('click', function() {
    window.location.href = 'register.html';
});

// When the login form is submitted, prevent the default form submission and validate the form
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    // Validate the username and password
    // If valid, log the user in and redirect to the workspace
    // If not valid, show an error message
});

// Add code to handle the dropdown menu
var isLoggedIn = checkIfUserIsLoggedIn(); // Placeholder function to check if a user is logged in
var dropdownContent = document.querySelector('.dropdown-content');

if (isLoggedIn) {
    dropdownContent.innerHTML = `
        <a href="workspace.html" id="workspace-link">Workspace</a>
        <a href="logout.html" id="logout-link">Logout</a>
    `;
} else {
    dropdownContent.innerHTML = `
        <a href="workspace.html" id="workspace-link">Workspace</a>
        <a href="login_menu.html" id="login-link">Login</a>
        <a href="register_menu.html" id="register-link">Register</a>
    `;
}

// When the logo is clicked, redirect to the home page
document.getElementById('toolbar').addEventListener('click', function() {
    window.location.href = '/';
    alert('You clicked the logo!');
});

// When the account is clicked, display the user actions menu
document.getElementById('account').addEventListener('click', function() {
    document.getElementById('user-actions-menu').style.display = 'block';
});

// When the register button is clicked, display the create account menu
document.getElementById('register-button').addEventListener('click', function() {
    document.getElementById('create-account-menu').style.display = 'block';
});

document.getElementById('create-group').addEventListener('click', function() {
    var groupName = document.getElementById('new-group-name').value;
    var groupItem = document.createElement('div');
    groupItem.className = 'group-item';
    groupItem.innerHTML = `
        <h3>${groupName}</h3>
        <button class="edit-group">Edit</button>
        <button class="delete-group">Delete</button>
        <button class="add-task">Add Task</button>
    `;
    document.getElementById('groups').appendChild(groupItem);
});

window.onload = function() {
    var logoutLink = document.getElementById('logout-link');

    // Check if user is logged in
    if (/* condition to check if user is logged in- this depends on how we are implementing this - placeholder until we connect to backend */) {
        // If user is logged in, show the logout link
        logoutLink.style.display = 'block';
    } else {
        // If user is not logged in, hide the logout link
        logoutLink.style.display = 'none';
    }
};