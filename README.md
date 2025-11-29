# ⚽ Automated Soccer Highlight Generator

An end-to-end system for generating soccer match highlights using computer vision and deep learning. This system processes full-length soccer videos, detects key events using **MatchVision** (introduced in the CVPR 2025 paper _Towards Universal Soccer Video Understanding_), and produces structured highlight segments with corresponding metadata.

The project is designed as a modular, scalable pipeline consisting of a web frontend, an API backend, and a GPU-accelerated video processing worker.

---

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 🎥 **Video Upload**: Upload full match videos through an intuitive web interface
- 🚀 **GPU-Accelerated Processing**: Fast event detection using MatchVision on GPU
- ⚡ **Automatic Highlight Extraction**: Intelligent detection and extraction of key moments
- ✂️ **Video Clipping**: Automatic generation of highlight segments using ffmpeg
- 💾 **Structured Storage**: Event data and metadata stored in PostgreSQL
- 🔄 **Asynchronous Processing**: Job queue system for scalable video processing
- 📊 **Interactive Timeline**: Visual timeline view for browsing match highlights
- 🏗️ **Modular Architecture**: Clean separation between frontend, backend, and ML worker

---

## 🏗️ System Architecture

The system consists of three main components that work together to process soccer videos and generate highlights:

### 1. Frontend

A modern Next.js application that provides the user interface for:

- Video upload and management
- Match browsing and search
- Interactive timeline visualization
- Highlight playback and navigation

**Technologies:**

- Next.js (TypeScript)
- Tailwind CSS
- shadcn/ui
- TanStack Query

### 2. Backend API

A FastAPI application responsible for:

- Match creation and metadata management
- Video upload handling and storage
- Job scheduling via Redis Queue
- Highlight retrieval and serving
- API authentication and authorization

**Technologies:**

- FastAPI
- PostgreSQL
- Redis (RQ job queue)
- S3-compatible object storage

### 3. Worker

A GPU-powered Python worker that handles:

- Video downloading and reading
- Frame sampling and preprocessing
- Event classification with MatchVision
- Highlight timestamp extraction
- Video clip generation via ffmpeg
- Writing results to the database

**Technologies:**

- PyTorch
- ffmpeg
- decord / PyAV
- Redis RQ

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.9+ (for backend and worker)
- **Node.js** 18+ and npm/yarn (for frontend)
- **PostgreSQL** 14+ (database)
- **Redis** 6+ (job queue)
- **ffmpeg** (video processing)
- **CUDA-capable GPU** (recommended for worker)
- **Docker** and **Docker Compose** (optional, for containerized deployment)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sa3ed/football-highlights.git
cd football-highlights
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install  # or yarn install
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb football_highlights

# Run migrations (if available)
cd backend
alembic upgrade head
```

### 5. Start Services

**Using Docker Compose (Recommended):**

```bash
docker-compose up -d
```

**Manual Setup:**

1. Start PostgreSQL and Redis:

   ```bash
   # PostgreSQL
   pg_ctl start

   # Redis
   redis-server
   ```

2. Start the backend:

   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. Start the worker:

   ```bash
   cd backend
   rq worker --with-scheduler
   ```

4. Start the frontend:

   ```bash
   cd frontend
   npm run dev
   ```

---

## ⚙️ Configuration

Create environment files for each component:

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/football_highlights

# Redis
REDIS_URL=redis://localhost:6379/0

# S3 Storage
S3_ENDPOINT=your-s3-endpoint
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
S3_BUCKET=football-highlights

# API
API_SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Worker

Uses the same environment variables as the backend.

---

## 📖 Usage

### Upload a Match Video

1. Navigate to the web interface (typically `http://localhost:3000`)
2. Click "Upload Match" or "New Match"
3. Fill in match metadata (teams, date, competition, etc.)
4. Upload the video file
5. The system will automatically queue the video for processing

### Monitor Processing

- View processing status in the match details page
- Check the job queue status in the backend dashboard
- Processing time depends on video length and GPU availability

### View Highlights

- Browse matches from the main page
- Click on a match to view its timeline
- Navigate through detected highlights
- Play individual highlight clips

### API Usage

```bash
# Create a match
curl -X POST http://localhost:8000/api/matches \
  -H "Content-Type: application/json" \
  -d '{
    "home_team": "Team A",
    "away_team": "Team B",
    "date": "2025-01-15"
  }'

# Upload video
curl -X POST http://localhost:8000/api/matches/{match_id}/upload \
  -F "file=@match_video.mp4"

# Get highlights
curl http://localhost:8000/api/matches/{match_id}/highlights
```

---

## 📁 Project Structure

```text
football-highlights/
├── backend/              # FastAPI backend application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── workers/     # Background job definitions
│   ├── alembic/         # Database migrations
│   └── requirements.txt
├── frontend/            # Next.js frontend application
│   ├── app/            # Next.js app directory
│   ├── components/     # React components
│   ├── lib/            # Utilities and hooks
│   └── package.json
├── infra/              # Infrastructure as code
│   ├── docker/        # Dockerfiles
│   └── kubernetes/    # K8s manifests (if applicable)
└── README.md
```

---

## 📚 API Documentation

Once the backend is running, interactive API documentation is available at:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

### Key Endpoints

- `POST /api/matches` - Create a new match
- `GET /api/matches` - List all matches
- `GET /api/matches/{id}` - Get match details
- `POST /api/matches/{id}/upload` - Upload match video
- `GET /api/matches/{id}/highlights` - Get match highlights
- `GET /api/matches/{id}/status` - Get processing status

---

## 🔧 Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Formatting

```bash
# Backend
cd backend
black .
isort .

# Frontend
cd frontend
npm run lint
npm run format
```

### Adding New Features

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Write tests
4. Submit a pull request

---

## 🐛 Troubleshooting

### Common Issues

**Worker not processing jobs:**

- Ensure Redis is running
- Check worker logs for errors
- Verify GPU availability if using GPU acceleration

**Video upload fails:**

- Check file size limits
- Verify S3 credentials
- Ensure sufficient disk space

**Database connection errors:**

- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database exists

**Frontend can't connect to API:**

- Verify NEXT_PUBLIC_API_URL is set correctly
- Check CORS settings in backend
- Ensure backend is running

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the project's style guidelines and includes appropriate tests.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **MatchVision**: Based on the CVPR 2025 paper "Towards Universal Soccer Video Understanding"
- All contributors and open-source libraries that made this project possible

---

## 📧 Contact

For questions or support, please open an issue on GitHub or contact [sa3ed.mostafa@hotmail.com].

---

## 🎯 Made with ⚽ by the Football Highlights team
