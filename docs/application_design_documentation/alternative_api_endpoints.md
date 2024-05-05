# Routes
- **/api/user** [POST] (/api/register)
  - **/api/user/\<username>** [DELETE] (new) [GET] (could be used for future user data, like default locale) [PUT] (could eventually be used to update info like the default locale)
- **/api/auth/\<username>** [DELETE] (/api/logout) [GET] (/api/auth)

- **/api/\<username>/task_groups** [GET] (get a users task groups)
- **/api/task_group** [POST]
  - **/api/task_group/\<task_group_id>** [DELETE] (/api/task_group) [GET] (/api/task_group) [PUT] (/api/task_group)

- **/api/\<task_group_id>/tasks** [GET] (get all a group's task)
- **/api/task** [POST]
  - **/api/task/\<task_id>** [DELETE] (/api/task) [GET] (/api/task) [PUT] (/api/task)

# Format and usage