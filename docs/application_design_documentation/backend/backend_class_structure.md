# Data holders

```mermaid
classDiagram
    class UnIDTask{
        +group_identifier int
        +name str
        +description str
        +due_date str | None
    }
    class Task{
        +identifier int
    }
    UnIDTask <|-- Task
    
    class UnIDTaskGroup{
        +username: str
        +name str
    }
    class TaskGroup{
        +identifier int
    }
    UnIDTaskGroup <|-- TaskGroup
```

# Data access interfaces

```mermaid
classDiagram
    class IUserAccess{
        +login(str username, bytes password_hash) bytes*
        +logout(str username, bytes auth_token)*
        +register_user(str username, bytes password_hash)*
        +is_user_registered(str username) bool*
        +is_user_login(str username, bytes password_hash) bool*
        +is_valid_session(str username, bytes token) bool*
    }
    
    class ITaskGroupAccess{
        +add_task_group(UnIDTaskGroup task_group) TaskGroup*
        +delete_task(int group_id)*
        +get_task_groups(str username) list[TaskGroup]*
        +get_task_group(int group_id) TaskGroup*
        +update_task_group(TaskGroup task_group)*
        +is_group_registered(int group_id) bool*
    }
    
    class ITaskAccess{
        +add_task(UnIDTask task) Task*
        +delete_task(int task_id)*
        +get_tasks(int group_id) list[Task]*
        +get_task(int task_id) Task*
        +update_task(Task task)*
        +is_task_registered(int task_id) bool*
    }
    IUserAccess *-- ITaskGroupAccess
    ITaskGroupAccess *-- ITaskAccess
    note for ITaskAccess "Leverages an ITaskGroupAccess implementation to validate task group identifiers"
    note for ITaskGroupAccess "Leverages an IUserAccess implementation to validate usernames"
```

# Security standard interface

```mermaid
classDiagram
    class ISecurityStandard{
        +create_auth_token() bytes*
        +create_auth_token_expiry() datetime*
        +hash(str password) bytes*
        +is_password_valid(str password) bool*
    }
```

# TMS security standard

```mermaid
classDiagram
    class TMSSecurityStandard{
        +int PASSWORD_MIN_LENGTH$
        +int AUTH_TOKEN_BYTES$
        +int AUTH_TOKEN_LIFESPAN_HOURS$
    }
    
    ISecurityStandard <|.. TMSSecurityStandard
```

# SQLite Database implementations

```mermaid
classDiagram
    class DataBaseManager{
        +str db_path
        +Cursor cursor
        +Connection conn
        
        -__init__(str db_path)
        +connection() object
    }
    
    class UserDatabaseManager{
        +int USERNAME_LENGTH$
        +ISecurityStandard security_standard
        -_initialize_db()
    }
    
    class TaskGroupDatabaseManager{
        +int NAME_LENGTH$
        -_initialize_db()
    }
    
    class TaskDatabaseManager{
        +int TITLE_LENGTH$
        -_initialize_db()
    }
    
    DataBaseManager <|-- UserDatabaseManager
    DataBaseManager <|-- TaskGroupDatabaseManager
    DataBaseManager <|-- TaskDatabaseManager

    IUserAccess <|.. UserDatabaseManager
    ITaskGroupAccess <|.. TaskGroupDatabaseManager
    ITaskAccess <|.. TaskDatabaseManager
    
    ISecurityStandard *-- UserDatabaseManager
```

# Request data validators
```mermaid
classDiagram
    class DateValidator{
        +validate_datetime(str date) Response | datetime
    }
    
    class TaskValidator{
        +validate_task_id(str task_id) Response | int
    }
    
    class TaskGroupValidator{
        +validate_group_id(str group_id) Response | int
    }
    
    class UserValidator{
        +validate_session(str username, str token) Response | bytes
        +validate_username(str username) Response | None
        +validate_login(str username, bytes password_hash) Response | None
    }
    
    IUserAccess *-- UserValidator
    ITaskGroupAccess *-- TaskGroupValidator
    ITaskAccess *-- TaskValidator
```

# API route interfaces
```mermaid
classDiagram
    class ITaskApiImpl{
        +get_task_groups(str username, str token) Response
        +delete_task_group(str username, str token, str group_id) Response
        +get_task_group(str username, str token, str group_id) Response
        +post_task_group(str username, str token, str | None group_id, str | None name) Response
        +delete_task(str username, str token, str task_id) Response
        +get_task(str username, str token, str task_id) Response
        +post_task(str username, str token, str group_id, str | None task_id, str | None title, str | None description, str | None due_date) Response
    }
    
    class IUserApiImpl{
        +auth(str username, str password) Response
        +logout(str username, str token) Response
        +register(str username, str password) Response
    }
    
```

# API route implementation
```mermaid
classDiagram
    ITaskApiImpl <|.. TMSTaskApiImpl
    IUserApiImpl <|.. TMSUserApiImpl
    
    DateValidator *-- TMSTaskApiImpl
    TaskValidator *-- TMSTaskApiImpl
    TaskGroupValidator *-- TMSTaskApiImpl
    UserValidator *-- TMSTaskApiImpl
```

# Flask route providers
```mermaid
classDiagram
    
    class UserApi{
         +str AUTH_TOKEN_KEY$
         +str PASSWORD_KEY$
         +str USERNAME_KEY$

         +str AUTH_ENDPOINT_PATH$
         +str LOGOUT_ENDPOINT_PATH$
         +str REGISTER_ENDPOINT_PATH$
    }
    
    class TaskApi{
        +str GROUP_ID_KEY$
        +str GROUP_NAME_KEY$
        +str TASK_ID_KEY$
        +str TASK_TITLE_KEY$
        +str TASK_DESCRIPTION_KEY$
        +str TASK_DATE_KEY$

        +str TASK_GROUPS_ENDPOINT_PATH$
        +str TASK_GROUP_ENDPOINT_PATH$
        +str TASK_ENDPOINT_PATH$
    }
    
    class  TMSWebsiteRoutes{
        +str HOMEPAGE_FILE_PATH$
        +str HOMEPAGE_ROUTE$
        
        +str TEMPLATES_PATH
        +str STATIC_PATH
    }
    

    class IFlaskRoutes{
        +get_blueprint() Blueprint
    }
    
    IFlaskRoutes <|.. UserApi
    IFlaskRoutes <|.. TMSWebsiteRoutes
    IFlaskRoutes <|.. TaskApi
    
    IUserApiImpl *-- UserApi
    ITaskApiImpl *-- TaskApi
```
