# Global

## Tool bar

- **Access**: Should be uniformly present accross all webpages. Ideally written once and dynamically added across all pages for consistency.

- Should contain on the left side a website logo, or website name. Doubling as a button to return to the **homepage**.

- Should contain on the right a button to access the **user actions menu**. When a user's logged in the text should be their username. When logged out, the button should say "account" or similar. The two states should likely be styled distinctly to distinguish them.

## User actions menu

- **Access**: Should be displayed when the **account button** in the **tool bar** is clicked. Possibly visually dropping down from that button.

- When logged in, should give a user the option to open up their **workspace**.

- When logged in, should give a user the option to log out.

- When logged out, should give the option to log in.

- When logged out, should give the option to register account.

## Create account menu

- **Access**: opened through the **user actions menu** while logged out.

- Should take in a username and password.

- Should validate the username and password in the menu.

- Should contain a submit button. Should only be interactable when form entries are valid.

- On submit should indicate success, or if the username was already used, or if the password didn't meet criteria(this should usually not happen, the rules should be coordinated).

- If successful automatically log into the account, and open up the **workspace**.

## Login menu

- **Access**: opened through the **user actions menu** while logged out. Or when navigating to the **workspace** url without being logged in.

- Should take in a username and password.

- Should contain a submit button. Should only be interactable when form entries are filled.

- On submit should indicate success, or if the username wasn't currently registerd, or if the password didn't match with the account.

- If successful open the **workspace**.

# Home page

- **Access**: the default landing page of the website, should be located at the domain with no subdirectories. Should be redirected to when a user logs out, manually or otherwise.

- Gives information about the webapp, and it's usage, and the project goal probably, maybe also something about the git repo.

# Workspace

- **Access**: Should be located at the subdirectory "workspace" of the current domain. Should be accessable through the URL directly. Should be opened when a logged in user selects the **workspace option** in the **user actions menu**. Should be opened when a user registers or signs in to their account.

- Should open the **login menu** if opened by a non logged in session.

## Group toolbar

- **Access**: innate part of the **workspace**.

- Should contain a button to add a new group, which on click opens up the **add group menu**.

- Should contain a sidebar listing the user's task groups, should scroll if it's necessary. 

- Groups should be radio buttons, only one selected at once. Selecting one should set the **task view** to display it's tasks.

## Add Group Menu

- **Access**: Selecting the **add group** button in the **group toolbar**, or selecting the add new group prompt in the **task view** when no group's selected.

- Should accept a group name, with no conditions beside the maximum length.

- Should include a button to add the new group.

## Task toolbar

- **Access**: innate part of the **workspace**.

- Should be horizontal, underneath the **toolbar**, but not going over the **group toolbar**.

- Should contain a button to add a new task, which when click on opens the **add task menu**. This should be hidden when no group is selected.

- With a task or tasks actively selected, a delete button should appear, when clicked it should open the **delete task menu**.

- Should contain the page number, and navigation options. This should be hidden when no group is selected, or when the number of tasks is low enough that only one page is possible.

### Add task menu

- **Access**: opened through clicking the **add task** button in the **task toolbar**.

- Should accept a title string, and validate it.

- Should have a field for entering a task description, should be validated.

- Should have an entry field for a due date. Which's also validated and constrained.

- Should contain a submit button, which submits the information to the server, and displays any error states, or if successful closes and adds in the new task entry to the task view(unless it's off the page).

## Task view

- **Access**: innate part of the **workspace**.

- If no group is selected, suggest selecting one(if any are available), or give create group option.

- If a group is selected, should display a list of **task instance**s, the current page number will relate to which tasks are shown, should possibly scroll if necessary.

### Task instance

- **Access**: part of the **task view** when a group that contains a task's selected.

- Should contain the ability to be selected, I suggest a check box on the left side of them.

- Should contain an edit button, on which clicking opens up the **update task menu**.

- Should be expandable to show full description and information.

- In collapsed form should list the title, and due date.

### Update task menu

- **Access**: opened by clicking on the edit button on a **task instance**.

- Should be visually and functionally almost the same as the **add task menu**, but named different, and different in final effect.
