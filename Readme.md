- https://app.eraser.io/workspace/1ha6t003bf3vz5TKfeaQ
- https://www.figma.com/design/roJ1UKYCqk1eCR6mEgB7ue/PitchStartUp?node-id=0-1&t=nSXoaDTrrB1pDNrZ-1

# Startup Pitching Platform

A full-stack platform where entrepreneurs can pitch their startups and connect with potential investors.

## Overview

This platform enables entrepreneurs to create and showcase startup pitches, allows investors to discover and invest in promising startups, and provides tools for tracking funding progress and analytics.

## Features

### For Entrepreneurs
- Create detailed startup pitches with media support (images/videos)
- Track funding progress and goals
- View investor activity and analytics
- Categorize startups by industry

### For Investors
- Search and filter startups by category
- Invest in promising ventures
- Track investment portfolio
- Discover trending and top-funded startups

### Platform Features
- Secure JWT-based authentication
- RESTful API architecture
- Category-based startup discovery
- Real-time analytics and statistics
- Optimized endpoints for performance

## Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL / SQLite
- **Authentication**: JWT tokens with refresh mechanism
- **API**: RESTful with comprehensive documentation

## Getting Started

### Prerequisites
- Python 3.8+
- pip or poetry
- PostgreSQL (or SQLite for development)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/startup-pitching-platform.git
cd startup-pitching-platform
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations
```bash
alembic upgrade head
```

5. Start the server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Project Structure
```
startup-pitching-platform/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # API endpoints
│   ├── schemas/        # Pydantic schemas
│   ├── auth/          # Authentication logic
│   └── database.py    # Database configuration
├── tests/             # Test suite
├── alembic/           # Database migrations
├── main.py            # Application entry point
├── requirements.txt   # Python dependencies
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout user

### Startups
- `GET /api/startups` - List all startups (with filters)
- `POST /api/startups` - Create new startup (auth required)
- `GET /api/startups/{id}` - Get startup details
- `PUT /api/startups/{id}` - Update startup (auth required)
- `DELETE /api/startups/{id}` - Delete startup (auth required)

### Investments
- `POST /api/startups/{id}/invest` - Invest in startup (auth required)
- `GET /api/startups/{id}/investments` - Get startup investments
- `GET /api/users/{id}/investments` - Get user investments

### Discovery
- `GET /api/search` - Search startups
- `GET /api/startups/trending` - Get trending startups
- `GET /api/startups/top-funded` - Get top funded startups
- `GET /api/categories` - Get all categories

### User & Dashboard
- `GET /api/users/{id}` - Get user info
- `GET /api/users/{id}/profile` - Get complete user profile
- `GET /api/dashboard` - Get user dashboard (auth required)

## Security Features

- JWT-based authentication with access and refresh tokens
- Password hashing with bcrypt
- HTTP-only cookies for refresh tokens
- Protected routes with authorization middleware
- Input validation with Pydantic

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
