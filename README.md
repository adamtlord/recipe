# Recipe Robot 🤖

An AI-powered recipe generation application that creates delicious recipes based on ingredients you have on hand. Built with FastAPI (Python) backend and React (TypeScript) frontend.

I figured I should learn more about this generative AI thing, and I wanted some practice with FastAPI and React. I also wanted to explore some current React component libraries. I wrote a working version of the backend and frontend and got them talking to each other, then deployed both on Render. Then I used AI (Cursor) to apply a consistent, good-practice structure to the code. I also leveraged AI to write all the unit tests. Heck, AI wrote this README, with the exception of this paragraph.

## 🌟 Features

- **Smart Recipe Generation**: AI-powered recipe suggestions using Google Gemini
- **Ingredient Search**: Intelligent food database with fuzzy matching
- **Modern UI**: Clean, responsive interface with retro gaming aesthetics
- **Real-time API Health**: Automatic backend connection monitoring
- **Type-Safe**: Full TypeScript coverage with comprehensive testing
- **Modular Architecture**: Well-structured, maintainable codebase

## 🏗️ Architecture

```
recipe/
├── backend/          # FastAPI Python backend
│   ├── app/         # Application modules
│   │   ├── api/     # API routes and dependencies
│   │   ├── core/    # Configuration, database, security
│   │   ├── models/  # Database and Pydantic models
│   │   ├── services/# Business logic layer
│   │   └── utils/   # Utility functions
│   ├── tests/       # Comprehensive test suite
│   └── requirements.txt
├── frontend/         # React TypeScript frontend
│   ├── src/         # Source code
│   │   ├── components/ # Reusable UI components
│   │   ├── hooks/   # Custom React hooks
│   │   ├── services/# API service layer
│   │   ├── types/   # TypeScript definitions
│   │   ├── utils/   # Utility functions
│   │   └── constants/# Application constants
│   ├── tests/       # Component and unit tests
│   └── package.json
└── data/            # Shared data files
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **Google Gemini API Key** (for recipe generation)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   echo "DATABASE_URL=sqlite:///./database.db" >> .env
   ```

5. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   # Create .env file
   echo "VITE_API_URL=http://localhost:8000" > .env
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
python -m pytest

# Run specific test categories
python -m pytest tests/unit/          # Unit tests only
python -m pytest tests/integration/   # Integration tests only

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Use the test runner script
python run_tests.py --unit --coverage
```

### Frontend Tests

```bash
cd frontend

# Run tests in watch mode
npm run test

# Run tests once
npm run test:run

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

### Key Endpoints

- `GET /health` - API health check
- `POST /api/v1/recipes/generate` - Generate recipes from ingredients
- `GET /api/v1/foods` - Search food ingredients

## 🛠️ Development

### Backend Development

The backend follows a clean architecture pattern:

- **API Layer** (`app/api/`): FastAPI routes and dependencies
- **Core Layer** (`app/core/`): Configuration, database, security
- **Models Layer** (`app/models/`): Database and Pydantic schemas
- **Services Layer** (`app/services/`): Business logic
- **Utils Layer** (`app/utils/`): Utility functions

### Frontend Development

The frontend uses modern React patterns:

- **Components** (`src/components/`): Reusable UI components
- **Hooks** (`src/hooks/`): Custom React hooks for state management
- **Services** (`src/services/`): API communication layer
- **Types** (`src/types/`): TypeScript type definitions
- **Utils** (`src/utils/`): Utility functions

#### Path Aliases

The frontend uses `@` alias for clean imports:

```typescript
// Instead of: import { Header } from '../../../components'
import { Header } from '@/components'
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=sqlite:///./database.db
ALLOWED_ORIGINS=["http://localhost:5173"]
APP_TITLE=Recipe Robot API
APP_VERSION=1.0.0
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## 📦 Dependencies

### Backend
- **FastAPI**: Modern, fast web framework
- **SQLModel**: Type-safe database ORM
- **Pydantic**: Data validation and settings
- **Google Generative AI**: Recipe generation
- **Pytest**: Testing framework

### Frontend
- **React 19**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS
- **DaisyUI**: Component library
- **Vitest**: Testing framework
- **Axios**: HTTP client

## 🚀 Deployment

### Backend Deployment

1. **Build for production:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with production server:**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend Deployment

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Serve static files:**
   ```bash
   npm run preview
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for recipe generation capabilities
- **FastAPI** and **React** communities for excellent documentation
- **Tailwind CSS** and **DaisyUI** for beautiful UI components

---

**Happy Cooking! 👨‍🍳👩‍🍳**
