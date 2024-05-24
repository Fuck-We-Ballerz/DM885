🚀 Using the API
===

To interface with the application there exists these following interfaces.

# Teacher

## `GET /api/v1/teachers`

### Description

Returns all the teachers

### returns

```JSON
{
    "message": string,
    "teacher": [
        {
            "id": string,
            "name": string,
            "username": string,
            "is_paused": bool
        }
    ]
}
```


## `GET /api/v1/teachers/[id]`


### Description

Gets the information about a teacher

### returns

```JSON
{
    "message": string,
    "teacher": [
        {
            "id": string,
            "name": string,
            "username": string,
            "is_paused": bool
        }
    ]
}
```

## `GET /api/v1/teachers/[id]/submission/[submission_id]/`

### Description

Get the status, logs and the result for a given submission

#### Unused

* `[id]`

#### returns

```JSON
[
    {
        "status": string,
        "stdout": string,
        "stderr": string,
        "result": string,
    }
]
```

## `POST /api/v1/teachers/[id]/submission/[submission_id]/status`


### Description

Sets the status of the given submission

### Unused

* `[id]`

### Body

```JSON
{
    "status": "pending" | "running" | "completed" | "failed" | "cancelled"
}
```

### returns

```JSON
{
    "message": string
}
``` 

## `GET /api/v1/teachers/[id]/courses`

### Description

Returns a list of all the courses

### Unused

* `[id]`

### returns

```JSON
{
    "message": string,
    "courses": [
        {
            "id": number,
            "name": string,
        }
    ]
}
```

## `POST /api/v1/teachers/[id]/assignment`

### Description

Enrolls a student into the given assignment

### Unused

* `[id]`

### Body

```json
{
    student_id: [ number ]
}
```

### returns

```JSON
{
    "message": string,
}
```

## `GET /api/v1/teachers/[id]/assignment`

### Description

Returns all the submissions made by a student for a given assignment

### Unused

* `[id]`

### Body

```json
{
    student_id: number,
    assignment_id: number,
}
```

### returns

```JSON
{
    "message": string,
    "submissions": [
        {
            "id": number,
            "grade": string,
            "status": string,
            "submission": string,
            "submission_std": string,
            "submission_err": string,
            "submission_time": date,
            "assignment_id": number,
            "student_id": number,
        }
    ]
}
```

## `DELETE /api/v1/teachers/[id]/assignment`

### Description

Unenrolls a student from the given assignment

### Unused

* `[id]`

### Body

```json
{
    student_id: number,
    assignment_id: number,
}
```

### returns

```JSON
{
    "message": string
}
```

## `GET /api/v1/teachers/[id]/assignment/student`

### Description

Returns all the submissions made by the given student for the given assignment

### Unused

* `[id]`

### Body

```json
{
    student_id: number,
    assignment_id: number,
}
```

### returns

```JSON
{
    "message": string,
    "submissions": [
        {
            "id": number,
            "grade": string,
            "status": string,
            "submission": string,
            "submission_std": string,
            "submission_err": string,
            "submission_time": date,
            "assignment_id": number,
            "student_id": number,
        }
    ]
}
```

## `POST /api/v1/teachers/[id]/assignment/student/[student_id]`

### Description

Enrolls the specific student into the assignment

### Unused

* `[id]`

### Body

```json
{
    assignment_id: number,
}
```

### returns

```JSON
{
    "message": string
}
```

## `POST /api/v1/teachers/[id]/assignment/stop/[assignment_id]`

### Description

Cancels the evaluation of all submissions for an assignment

### Unused

* `[id]`

### returns

```JSON
{
    "message": string
}
```

## `POST /api/v1/teachers/[id]/assignment/pause/[assignment_id]`

### Description

Pauses or unpauses an assignment.

### Unused

* `[id]`

### Body

```json
{
    is_visible: bool,
    assignment_id: number,
}
```

### returns

```JSON
{
    "message": string,
    "is_visible": bool
}
```

## `GET /api/v1/teachers/[id]/assignment/metadata`

### Description

Returns a csv file containing the metadata for a given student for a given assignment

### Unused

* `[id]`

### Body

```json
{
    student_id: number,
    assignment_id: number,
}
```

### returns

```JSON
{
    "message": string,
    "csv": string
}
```


## `GET /api/v1/teachers/[id]/assignment/metadata/[assignment_id]`

### Description

Returns a csv file containing the metadata for each student for a given assignment

### Unused

* `[id]`

### Body

```json
{
    assignment_id: number,
}
```

### returns

```JSON
{
    "message": string,
    "csv": string
}
```


## `GET /api/v1/teachers/[id]/assignment/logs`

### Description

Retuns a zip file containing for a given student a folder and within that folder a file for stdout and another for stderr for a given assignment

### Unused

* `[id]`

### Body

```json
{
    assignment_id: number,
    student_id: number,
}
```

### returns

```JSON
zil file blob
```


## `GET /api/v1/teachers/[id]/assignment/logs/[assignment_id]`

### Description

Retuns a zip file containing for each student a folder and within that folder a file for stdout and another for stderr for a given assignment

### Unused

* `[id]`

### returns

```JSON
zil file blob
```


## `GET /api/v1/teachers/[id]/assignment/delete/[assignment_id]`

### Description

Deletes an assignment and unassigns the teachers and students that were assigned to that assignment.

### Unused

* `[id]`

### returns

```JSON
{
    "message": string,
    deleted_assignment: number
}
```