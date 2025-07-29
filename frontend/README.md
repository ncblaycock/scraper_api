# Scraper Admin Frontend

A modern React/Vite/TypeScript admin dashboard for the FastAPI scraper backend.

## Features

- **Dashboard**: Overview with system stats and recent activity
- **User Management**: View, search, and manage users
- **Reports**: Generate and view reports with status tracking
- **Downloads**: Access and download available files
- **Responsive Design**: Built with Tailwind CSS for mobile-first design

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Query** - Data fetching and caching
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Lucide React** - Modern icons

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` and will proxy API requests to the FastAPI backend at `http://localhost:8000`.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Integration

The frontend is configured to work with the FastAPI backend through:

- **Proxy Configuration**: Vite proxies `/api` requests to `http://localhost:8000`
- **CORS**: Backend allows requests from `http://localhost:5173`
- **API Service**: Centralized API client with interceptors for auth and error handling

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── Layout.tsx      # Main layout with sidebar navigation
├── pages/              # Page components
│   ├── Dashboard.tsx   # Dashboard overview
│   ├── Users.tsx       # User management
│   ├── Reports.tsx     # Reports management
│   └── Downloads.tsx   # File downloads
├── services/           # API services
│   └── api.ts         # Axios configuration and endpoints
├── App.tsx            # Main app component with routing
├── main.tsx           # React entry point
└── index.css          # Global styles with Tailwind
```

## Development

Make sure the FastAPI backend is running on `http://localhost:8000` before starting the frontend development server.
