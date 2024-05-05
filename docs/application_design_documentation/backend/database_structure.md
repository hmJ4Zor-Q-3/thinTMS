# Database Structure

## Legend

- **"PK"** indicated a primary key
- **"FK"** indicate a foreign key
- **"NN"** indicates not null value
- **"ISO8601"** Must follow IS0 standard 8601

## Tables

### USERS

- **username** - VARCHAR(30) - PK
- **password** - TEXT - NN
- **token** - TEXT
- **token_expiry** - TEXT ISO8601

### TASK_GROUPS

- **group_id** - INTEGER - PK
- **username** - FK for USERS - NN
- **name** - VARCHAR(50) NN

### TASKS

- **task_id** - INTEGER - PK
- **group_id** - FK for TASK_GROUPS - NN
- **title** - VARCHAR(100) NN
- **description** - TEXT NN
- **due_date** - TEXT ISO8601

## ER Diagram

```mermaid
erDiagram
    USERS{
        VARCHAR(30) username PK
        TEXT password
        TEXT token
        TEXT TOKEN_EXPIRY 
    }

    TASK_GROUPS{
        INTEGER group_id PK
        VARCHAR(30) username FK "USERS(username)"
        VARCHAR(50) name
    }

    TASKS{
        INTEGER task_id PK
        INTEGER group_id FK "TASK_GROUPS(group_id)"
        VARCHAR(100) title
        TEXT description
        TEXT due_date
    }
    
    USERS ||--o{TASK_GROUPS : has
    TASK_GROUPS ||--o{TASKS : has
```
