#!/bin/bash

# Quick start script for Data Investigation Platform

set -e

echo "=================================="
echo "Data Investigation Platform Setup"
echo "=================================="
echo ""

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✓ Docker detected"
    echo ""
    echo "Starting services with Docker..."
    docker-compose up -d

    echo ""
    echo "Waiting for services to be ready..."
    sleep 10

    echo ""
    echo "Seeding database with sample data..."
    docker-compose exec -T backend python seed_data.py

    echo ""
    echo "=================================="
    echo "✓ Setup Complete!"
    echo "=================================="
    echo ""
    echo "Access the application:"
    echo "  Frontend:  http://localhost:3000"
    echo "  Backend:   http://localhost:8000"
    echo "  API Docs:  http://localhost:8000/docs"
    echo ""
    echo "To stop: docker-compose down"
    echo ""
else
    echo "⚠ Docker not found. Please install Docker or follow manual setup in SETUP.md"
    exit 1
fi
