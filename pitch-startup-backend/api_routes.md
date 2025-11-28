# API Routes for Startup Pitching Platform

## Authentication Routes

### Register a new user
- **POST** `/api/auth/register`
- **Body:**
  ```json
  {
    "full_name": "string",
    "email": "string",
    "password": "string"
  }
  ```

### Login user
- **POST** `/api/auth/login`
- **Body:**
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```

### Logout user
- **POST** `/api/auth/logout`

### Get current logged-in user
- **GET** `/api/auth/me`

---

## User Routes

### Get user profile
- **GET** `/api/users/:id`

### Update user profile
- **PUT** `/api/users/:id`
- **Body:**
  ```json
  {
    "full_name": "string"
  }
  ```

### Delete user account
- **DELETE** `/api/users/:id`

---

## Startup Routes

### Get all startups (with filters)
- **GET** `/api/startups`
- **Query Parameters:** `?category=tech&status=active&limit=10&page=1`

### Get single startup details
- **GET** `/api/startups/:id`

### Create new startup
- **POST** `/api/startups`
- **Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "category": "string",
    "image_url": "string",
    "video_url": "string",
    "pitch": "string",
    "funding_goal": "number"
  }
  ```

### Update startup
- **PUT** `/api/startups/:id`
- **Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "status": "string"
  }
  ```

### Delete startup
- **DELETE** `/api/startups/:id`

### Get startups by user
- **GET** `/api/users/:id/startups`

---

## Investment Routes

### Get all investments for a startup
- **GET** `/api/startups/:id/investments`

### Create investment (fund a startup)
- **POST** `/api/startups/:id/invest`
- **Body:**
  ```json
  {
    "amount": "number"
  }
  ```

### Get user's investment history
- **GET** `/api/users/:id/investments`

### Get single investment details
- **GET** `/api/investments/:id`

---

## Comment Routes

### Get all comments for a startup
- **GET** `/api/startups/:id/comments`

### Add comment to startup
- **POST** `/api/startups/:id/comments`
- **Body:**
  ```json
  {
    "content": "string"
  }
  ```

### Update comment
- **PUT** `/api/comments/:id`
- **Body:**
  ```json
  {
    "content": "string"
  }
  ```

### Delete comment
- **DELETE** `/api/comments/:id`

---

## Analytics/Dashboard Routes

### Get dashboard overview (for any user)
- **GET** `/api/dashboard`
- **Response:**
  ```json
  {
    "my_startups": [],
    "my_investments": [],
    "total_raised": "number",
    "total_invested": "number"
  }
  ```

### Get startup analytics
- **GET** `/api/startups/:id/analytics`
- **Response:**
  ```json
  {
    "total_funded": "number",
    "investor_count": "number",
    "funding_progress": "number",
    "recent_investments": []
  }
  ```

### Get trending/top startups
- **GET** `/api/startups/trending`
- **GET** `/api/startups/top-funded`

---

## Search & Filter Routes

### Search startups
- **GET** `/api/search`
- **Query Parameters:** `?q=tech+startup&category=fintech`

### Get all categories
- **GET** `/api/categories`

---

## Response Formats

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "statusCode": 400
}
```

### Pagination Response
```json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10
  }
}
```
