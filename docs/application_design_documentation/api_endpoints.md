# API ENDPOINTS

## unofficial http statuses:
- 452: approximately: not valid username.
- 453: approximately: not valid password.
- 454: approximately: not valid identifier.

## /api/auth

API endpoint for letting an already registered user login.

**Input**: a username and a password to check against the user database. The password should be hashed after it's received to be compared against the stored password hash, for security the actual password's never stored. The password's hashed since any given password will only correlate with one hash, but the hash can't easily be used to find a password that hashes to it, so in the event of security breaches it's usefulness is limited, and account security's relatively maintained.
**Input Format**: {
                    "username": string,
                    "password": string
                  }

**Returns on no username matching**: a unique error code that represents this, so the client can display a specific error message.
**error code**: 452

**Returns on password no matching**: a unique error code that represents this, so the client can display a specific error message.
**Error code** 453

**Returns on match**: a unique and temporary token associated with the user. The token should be recorded in a database table along with the associated user's id, and the time it was created at. This token will be used to identify the user as logged in, the client will send it with requests for that users information.

When the server receives the token the server should call a function that verifies that the token isn't expired. If the token is expired it's record should be removed from the database. And a response indicating this should be sent back. If the token is valid, the associated user's id should be acquired, and used to gather all the requested information from the database.

If the user is already logged in their current token should be replaced with a new one.

**Response format**: {"token": string}

## /api/logout

API endpoint allowing a logged in client to invalidate their authentication token prior to it's natural expiry.

**Input**: takes in an authentication token and username.
**Input Format**: {
                    "username": string,
                    "token": string
                  }

**Returns**: nothing, or perhaps a standard success code 200. An incorrect token should produce an unauthorized status code, i.e code 401.

## /api/register

API endpoint for creating a new account.

**Input**: a username and a password to attempt to register. If both are valid the password should be hashed, and the username and hash should be recorded to the database.
**Input Format**: {
                    "username": string,
                    "password": string
                  }

**Returns on username already used**: a unique error code that represents this, so the client can display a specific error message.

To prevent somebody rapidly registering thousands of accounts we could require an email, and email confirmation. But to send a registration email and receive a response may be challenging without a dedicated server.
**error code**: 452

**Returns on weak password entry**: a unique error code that represents this, so the client can display a specific error message. The default web client should also validate this before submitting the registration request, this doesn't prevent direct api access though so validation is necessary here too.
**Error code** 453

**Returns on success**: an authentication token created identically to in api/auth to allow the new user to be automatically logged in to their new account.

**Response format**: {"token": string}



## /api/task_groups [GET]

- Get all tasksgroups for the given user, names and ids, but not the related tasks.
- If credentials aren't valid return status code: 452 or 401.

**Input Format**: {"username": string, "token": string}

**Response format**: [{"group_id": numeric, ["name": string]} ...]



## /api/task_group [DELETE/GET/POST]

- remove a group/get the tasks belonging to the group/add a new task group 
- If credentials aren't valid return status code: 452 or 401.
- If invalid group id return status code: 454

**Input Format**:
- [DELETE]: {"username": string, "token": string, "group_id": numeric}
- [GET]: {"username": string, "token": string, "group_id": numeric} // add page constraint later on
- [POST]: {"username": string, "token": string, ["group_id": numeric], ["name": string]}

**Response format**: 
- \[GET]: {name: string, contents: [{"task_id": numeric, ["title": string], ["date": string]} ...]}
- [POST]: {"group_id": numeric}



## /api/task [DELETE/GET/POST]

- remove a task/get the task/add or update a task 
- If credentials aren't valid return status code: 452 or 401.
- If invalid task id return status code: 454

**Input Format**:
- [DELETE]: {"username": string, "token": string, "task_id": value}
- [GET]: {"username": string, "token": string, "task_id": numeric} // add page constraint later on
- [POST]: {"username": string, "token": string, [group_id: numeric], ["task_id": numeric], ["title": string], ["description": string], ["date": string]}

**Response format**: 
- \[GET]: [{"task_id": numeric, ["title": string], ["description": string], ["date": string]}...]
- [POST]: {"task_id": numeric}
