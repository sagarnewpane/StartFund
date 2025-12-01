# API Documentation for Startup Pitching Platform

## Base URL
```
http://your-api-domain.com/api
```

## Authentication
Most endpoints require authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## 📋 Table of Contents
1. [Authentication Routes](#authentication-routes)
2. [User Routes](#user-routes)
3. [Startup Routes](#startup-routes)
4. [Investment Routes](#investment-routes)
5. [Dashboard Route](#dashboard-route)
6. [Search & Discovery Routes](#search--discovery-routes)
7. [Response Formats](#response-formats)

---

## Authentication Routes

### Register a new user
- **POST** `/api/auth/register`
- **Auth Required:** No
- **Body:**
  ```json
  {
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }
  ```
- **Success Response (201):**
  ```json
  {
    "id": "user123",
    "email": "john@example.com",
    "full_name": "John Doe"
  }
  ```

### Login user
- **POST** `/api/auth/login`
- **Auth Required:** No
- **Body:**
  ```json
  {
    "email": "john@example.com",
    "password": "password123"
  }
  ```
- **Success Response (200):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- **Note:** Refresh token is set as HTTP-only cookie automatically

### Get current logged-in user
- **GET** `/api/auth/me`
- **Auth Required:** Yes
- **Success Response (200):**
  ```json
  {
    "id": "user123",
    "email": "john@example.com",
    "full_name": "John Doe"
  }
  ```

### Refresh access token
- **POST** `/api/auth/refresh`
- **Auth Required:** No (uses refresh_token cookie)
- **Success Response (200):**
  ```json
  {
    "access_token": "new_access_token_here",
    "token_type": "bearer"
  }
  ```

### Logout user
- **POST** `/api/auth/logout`
- **Auth Required:** No
- **Success Response (200):**
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

---

## User Routes

### Get basic user info
- **GET** `/api/users/{user_id}`
- **Auth Required:** No
- **Success Response (200):**
  ```json
  {
    "id": "user123",
    "email": "john@example.com",
    "full_name": "John Doe",
    "created_at": "2024-01-15T10:30:00"
  }
  ```

### Get complete user profile (RECOMMENDED)
- **GET** `/api/users/{user_id}/profile`
- **Auth Required:** No
- **Description:** Get user info, startups, investments, and stats in ONE call
- **Success Response (200):**
  ```json
  {
    "user": {
      "id": "user123",
      "email": "john@example.com",
      "full_name": "John Doe",
      "created_at": "2024-01-15T10:30:00"
    },
    "startups": [
      {
        "id": "startup123",
        "title": "AI Startup",
        "description": "...",
        "category": "AI",
        "funding_goal": 100000,
        "total_funded": 45000,
        "status": "active",
        "image_url": "...",
        "created_at": "..."
      }
    ],
    "investments": [
      {
        "id": "inv123",
        "amount": 5000,
        "invested_at": "2024-01-20T14:30:00",
        "startup": {
          "id": "startup456",
          "title": "FinTech App",
          "category": "FinTech",
          "image_url": "..."
        }
      }
    ],
    "stats": {
      "total_startups": 3,
      "total_raised": 75000,
      "total_invested": 15000,
      "total_investments": 5
    }
  }
  ```

### Update user profile
- **PUT** `/api/users/{user_id}`
- **Auth Required:** Yes (can only update own profile)
- **Body:**
  ```json
  {
    "full_name": "John Updated Name"
  }
  ```
- **Success Response (200):**
  ```json
  {
    "id": "user123",
    "email": "john@example.com",
    "full_name": "John Updated Name"
  }
  ```

### Get user's startups
- **GET** `/api/users/{user_id}/startups`
- **Auth Required:** No
- **Success Response (200):** Array of startup objects

### Get user's investments
- **GET** `/api/users/{user_id}/investments`
- **Auth Required:** No
- **Success Response (200):**
  ```json
  [
    {
      "id": "inv123",
      "amount": 5000,
      "invested_at": "2024-01-20T14:30:00",
      "startup": {
        "id": "startup456",
        "title": "FinTech App",
        "category": "FinTech",
        "image_url": "...",
        "funding_goal": 100000,
        "total_funded": 65000
      }
    }
  ]
  ```

---

## Startup Routes

### Get all startups (with filters)
- **GET** `/api/startups`
- **Auth Required:** No
- **Query Parameters:**
  - `category` (optional): Filter by category
  - `status` (optional): Filter by status (active, closed)
  - `limit` (optional): Number of results (default: 100)
  - `skip` (optional): Skip N results for pagination (default: 0)
- **Example:** `/api/startups?category=AI&limit=10&skip=0`
- **Success Response (200):** Array of startup cards

### Get single startup details
- **GET** `/api/startups/{startup_id}`
- **Auth Required:** No
- **Success Response (200):**
  ```json
  {
    "id": "startup123",
    "user_id": "user123",
    "title": "AI Startup",
    "description": "Revolutionary AI platform...",
    "category": "AI",
    "image_url": "https://...",
    "video_url": "https://...",
    "pitch": "Full pitch text...",
    "funding_goal": 100000,
    "total_funded": 45000,
    "status": "active",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
  ```

### Create new startup
- **POST** `/api/startups`
- **Auth Required:** Yes
- **Body:**
  ```json
  {
    "title": "My Startup",
    "description": "Short description",
    "category": "AI",
    "image_url": "https://...",
    "video_url": "https://...",
    "pitch": "Full pitch text...",
    "funding_goal": 100000
  }
  ```
- **Success Response (201):**
  ```json
  {
    "id": "startup123",
    "message": "Startup created successfully"
  }
  ```

### Update startup
- **PUT** `/api/startups/{startup_id}`
- **Auth Required:** Yes (only owner can update)
- **Body:** (all fields optional)
  ```json
  {
    "title": "Updated Title",
    "description": "Updated description",
    "category": "FinTech",
    "image_url": "https://...",
    "video_url": "https://...",
    "pitch": "Updated pitch..."
  }
  ```
- **Success Response (200):** Updated startup object

### Delete startup
- **DELETE** `/api/startups/{startup_id}`
- **Auth Required:** Yes (only owner can delete)
- **Success Response (200):**
  ```json
  {
    "message": "Startup deleted successfully"
  }
  ```

### Get startup investments
- **GET** `/api/startups/{startup_id}/investments`
- **Auth Required:** No
- **Success Response (200):**
  ```json
  [
    {
      "id": "inv123",
      "amount": 5000,
      "invested_at": "2024-01-20T14:30:00",
      "investor": {
        "id": "user456",
        "full_name": "Jane Investor"
      }
    }
  ]
  ```

### Get startup analytics
- **GET** `/api/startups/{startup_id}/analytics`
- **Auth Required:** No
- **Success Response (200):**
  ```json
  {
    "startup_id": "startup123",
    "total_funded": 45000,
    "funding_goal": 100000,
    "investor_count": 12,
    "funding_progress": 45.0,
    "recent_investments": [
      {
        "id": "inv123",
        "amount": 5000,
        "invested_at": "2024-01-20T14:30:00",
        "investor": {
          "id": "user456",
          "full_name": "Jane Investor"
        }
      }
    ]
  }
  ```

---

## Investment Routes

### Invest in a startup
- **POST** `/api/startups/{startup_id}/invest`
- **Auth Required:** Yes
- **Body:**
  ```json
  {
    "amount": 5000
  }
  ```
- **Success Response (201):**
  ```json
  {
    "id": "inv123",
    "message": "Investment successful",
    "amount": 5000
  }
  ```
- **Validation:**
  - Amount must be positive
  - Cannot invest in your own startup

---

## Dashboard Route

### Get user dashboard (RECOMMENDED for logged-in user)
- **GET** `/api/dashboard`
- **Auth Required:** Yes
- **Description:** Get complete overview in ONE call
- **Success Response (200):**
  ```json
  {
    "my_startups": [
      {
        "id": "startup123",
        "title": "AI Startup",
        "category": "AI",
        "funding_goal": 100000,
        "total_funded": 45000,
        "status": "active",
        "created_at": "..."
      }
    ],
    "my_investments": [
      {
        "id": "inv123",
        "amount": 5000,
        "invested_at": "2024-01-20T14:30:00",
        "startup": {
          "id": "startup456",
          "title": "FinTech App",
          "category": "FinTech",
          "image_url": "...",
          "total_funded": 65000,
          "funding_goal": 100000
        }
      }
    ],
    "total_raised": 45000,
    "total_invested": 15000,
    "stats": {
      "startups_count": 3,
      "investments_count": 5
    }
  }
  ```

---

## Search & Discovery Routes

### Search startups
- **GET** `/api/search`
- **Auth Required:** No
- **Query Parameters:**
  - `q` (optional): Search query (searches title, description, pitch)
  - `category` (optional): Filter by category
- **Example:** `/api/search?q=artificial+intelligence&category=AI`
- **Success Response (200):** Array of matching startups (max 50)

### Get trending startups
- **GET** `/api/startups/trending`
- **Auth Required:** No
- **Description:** Startups with most recent investment activity
- **Success Response (200):** Array of trending startups (top 10)

### Get top funded startups
- **GET** `/api/startups/top-funded`
- **Auth Required:** No
- **Query Parameters:**
  - `limit` (optional): Number of results (default: 10)
- **Success Response (200):** Array of top funded startups

### Get all categories
- **GET** `/api/categories`
- **Auth Required:** No
- **Success Response (200):**
  ```json
  {
    "categories": ["AI", "FinTech", "HealthTech", "EdTech", "E-commerce"]
  }
  ```

---

## Response Formats

### Success Response
```json
{
  "data": {},
  "message": "Success message"
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error, invalid ID)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (not authorized for this action)
- `404` - Not Found
- `500` - Internal Server Error

---

## 🔥 Important Notes for Frontend

### 1. **Use Optimized Endpoints**
Instead of multiple calls, use these single-call endpoints:
- `/api/users/{id}/profile` - Complete user profile
- `/api/dashboard` - Complete dashboard for logged-in user
- `/api/users/{id}/investments` - Investments with startup details included

### 2. **Authentication Flow**
```javascript
// 1. Login
const { access_token } = await login(email, password);
localStorage.setItem('access_token', access_token);

// 2. Use token for protected routes
fetch('/api/dashboard', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});

// 3. Refresh token when expired
const { access_token: new_token } = await fetch('/api/auth/refresh');
```

### 3. **Pagination Example**
```javascript
// Get startups page by page
const page = 1;
const limit = 10;
const skip = (page - 1) * limit;

fetch(`/api/startups?limit=${limit}&skip=${skip}`);
```

### 4. **Error Handling**
```javascript
try {
  const response = await fetch('/api/startups');
  if (!response.ok) {
    const error = await response.json();
    console.error(error.detail);
  }
} catch (error) {
  console.error('Network error:', error);
}
```

### 5. **Date Formatting**
All datetime fields are in ISO 8601 format: `2024-01-15T10:30:00`

### 6. **Enriched Data**
Most endpoints now return enriched data to avoid multiple API calls:
- Investments include startup details
- Startup investments include investor names
- User profile includes everything in one call

---

## Testing the API

### Using cURL
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"John Doe","email":"john@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Get startups (with token)
curl http://localhost:8000/api/startups \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using JavaScript (Fetch)
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'password123'
  })
});
const { access_token } = await loginResponse.json();

// Get dashboard
const dashboardResponse = await fetch('http://localhost:8000/api/dashboard', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const dashboard = await dashboardResponse.json();
```

---
