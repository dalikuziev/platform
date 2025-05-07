# Madad Hybrid Learing Platform API

This is an official API for Education platform using Django REST Framework.

## Endpoints
### API_V1_URL = /api/v1/

<details>
    <summary>Courses</summary>

### Permissions: IsAuthenticated, IsCourseOwnerOrReadOnly
### 1. GET /courses/
User-created courses.
#### Response:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Matematika",
            "price": 100,
            "is_active": true,
            "owner": 2
        }
    ]
}
```

### 2. POST /courses/
Create a new course.
#### Request:
```json
{
    "title": "Matematika",
    "description": "hisoblash"
}
```
#### Response:
```json
{
    "id": 1,
    "title": "Matematika",
    "description": "hisoblash",
    "is_active": true,
    "owner": 2
}
```
### 3. GET /courses/{id}/
Retrieve a specific course.
#### Response:
```json
{
    "id": 1,
    "title": "Matematika",
    "is_active": true,
    "owner": 2
}
```
### 4. GET /courses/{id}/lessons/
User-created course lessons.
#### Response:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Matematika",
            "price": 100,
            "is_active": true,
            "owner": 2
        }
    ]
}
```

### 2. POST /courses/
Create a new course.
#### Request:
```json
{
    "title": "Matematika",
    "description": "hisoblash"
}
```
#### Response:
```json
{
    "id": 1,
    "title": "Matematika",
    "description": "hisoblash",
    "is_active": true,
    "owner": 2
}
```

</details>