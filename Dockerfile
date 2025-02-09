# Stage 1: Build the Frontend
FROM node:18-slim AS frontend-builder

# Set the working directory for the frontend
WORKDIR /app/frontend

# Copy package.json and pnpm-lock.yaml
COPY frontend/package.json frontend/pnpm-lock.yaml ./frontend/

# Install pnpm globally
RUN npm install -g pnpm

# Install frontend dependencies
RUN pnpm install

# Copy the rest of the frontend code
COPY frontend ./frontend/

# Build the frontend
RUN pnpm build

# Stage 2: Build the Backend
FROM python:3.9-slim AS backend-builder

# Set the working directory for the backend
WORKDIR /app/backend

# Copy requirements.txt
COPY backend/requirements.txt .

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY backend .

# Stage 3: Final Image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy built frontend files from the frontend-builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy backend files from the backend-builder stage
COPY --from=backend-builder /app/backend ./backend

# Install backend dependencies again (if needed)
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose ports for frontend and backend
EXPOSE 8080 8000

# Set environment variables
ENV DJANGO_SECRET_KEY=your-secret-key
ENV DEBUG=1

# Run both frontend and backend servers
CMD (cd backend && python manage.py runserver 0.0.0.0:8000) & \
    (cd frontend && pnpm serve --port 8080)