Automated Soccer Highlight Generator

This repository contains an end-to-end system for generating soccer match highlights using computer vision and deep learning. The system processes full-length soccer videos, detects key events using MatchVision (introduced in the CVPR 2025 paper Towards Universal Soccer Video Understanding), and produces structured highlight segments with corresponding metadata.

The project is designed as a modular, scalable pipeline consisting of a web frontend, an API backend, and a GPU-accelerated video processing worker.

⸻

Features
• Upload full match videos through a web interface
• GPU-accelerated event detection using MatchVision
• Automatic extraction of highlight timestamps
• Generation of clipped video segments using ffmpeg
• Structured event data stored in PostgreSQL
• Asynchronous processing through a job queue
• Interactive timeline view for matches
• Modular architecture separating frontend, backend, and ML worker

⸻

System Architecture

The system consists of three main components:

1. Frontend

A Next.js application that provides:
• Video upload interface
• Match management and browsing
• Timeline visualization and highlight playback

Technologies used:
• Next.js (TypeScript)
• Tailwind CSS
• shadcn/ui
• TanStack Query

2. Backend API

A FastAPI application responsible for:
• Match creation and metadata management
• Video upload handling
• Job scheduling via Redis
• Highlight retrieval

Technologies used:
• FastAPI
• PostgreSQL
• Redis (RQ job queue)
• S3-compatible object storage

3. Worker

A GPU-powered Python worker responsible for:
• Downloading and reading match videos
• Sampling frames and running inference
• Event classification with MatchVision
• Highlight timestamp extraction
• Clip generation through ffmpeg
• Writing results to the database

Technologies used:
• PyTorch
• ffmpeg
• decord or PyAV
• Redis RQ
