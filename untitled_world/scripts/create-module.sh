#!/bin/bash

# Script to create a new module with standard structure

set -e

if [ -z "$1" ]; then
    echo "Usage: ./create-module.sh <module-name>"
    echo "Example: ./create-module.sh compliance"
    exit 1
fi

MODULE_NAME=$1
MODULE_DIR="modules/$MODULE_NAME"

if [ -d "$MODULE_DIR" ]; then
    echo "Error: Module '$MODULE_NAME' already exists"
    exit 1
fi

echo "Creating module: $MODULE_NAME"

# Create directory structure
mkdir -p "$MODULE_DIR"/{backend,frontend/{components,pages,hooks},tests,docs}

# Create module.json
cat > "$MODULE_DIR/module.json" << EOF
{
  "name": "$MODULE_NAME",
  "version": "1.0.0",
  "displayName": "$(echo $MODULE_NAME | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')",
  "description": "$MODULE_NAME module",
  "author": "Platform Team",
  "type": "standard",
  "dependencies": {
    "core": ">=0.1.0",
    "modules": []
  },
  "backend": {
    "enabled": true,
    "apiPrefix": "/api/v1/$MODULE_NAME",
    "models": ["backend/models.py"],
    "routes": ["backend/api.py"]
  },
  "frontend": {
    "enabled": true,
    "routes": [
      {
        "path": "/$MODULE_NAME",
        "component": "Dashboard"
      }
    ],
    "menuItems": [
      {
        "label": "$(echo $MODULE_NAME | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')",
        "icon": "box",
        "path": "/$MODULE_NAME"
      }
    ]
  },
  "permissions": [
    "$MODULE_NAME.view",
    "$MODULE_NAME.edit",
    "$MODULE_NAME.delete"
  ],
  "config": {}
}
EOF

# Create backend __init__.py
cat > "$MODULE_DIR/backend/__init__.py" << EOF
"""
$MODULE_NAME Module
"""
__version__ = "1.0.0"
EOF

# Create backend models.py
cat > "$MODULE_DIR/backend/models.py" << EOF
"""
$MODULE_NAME Module - Database Models
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
import sys
from pathlib import Path

# Import core Base
core_path = Path(__file__).parent.parent.parent.parent / "core" / "backend"
sys.path.insert(0, str(core_path))

from app.core.database import Base


# Add your models here
# Example:
# class MyModel(Base):
#     __tablename__ = "${MODULE_NAME}_items"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(200), nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
EOF

# Create backend api.py
cat > "$MODULE_DIR/backend/api.py" << EOF
"""
$MODULE_NAME Module - API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import sys
from pathlib import Path

# Import core dependencies
core_path = Path(__file__).parent.parent.parent.parent / "core" / "backend"
sys.path.insert(0, str(core_path))

from app.core.database import get_db

router = APIRouter()


@router.get("/")
def get_module_info():
    """Get module information."""
    return {
        "module": "$MODULE_NAME",
        "version": "1.0.0",
        "status": "active"
    }


# Add your endpoints here
EOF

# Create README
cat > "$MODULE_DIR/README.md" << EOF
# $MODULE_NAME Module

## Overview

Description of the $MODULE_NAME module.

## Features

- Feature 1
- Feature 2
- Feature 3

## API Endpoints

- \`GET /api/v1/$MODULE_NAME/\` - Module info

## Configuration

\`\`\`json
{
  "$MODULE_NAME": {
    "enabled": true
  }
}
\`\`\`

## Usage

\`\`\`python
# Example usage
\`\`\`

## Development

\`\`\`bash
# Run tests
pytest modules/$MODULE_NAME/tests/
\`\`\`
EOF

# Create test file
cat > "$MODULE_DIR/tests/test_api.py" << EOF
"""
Tests for $MODULE_NAME module
"""
import pytest


def test_module_info():
    """Test module info endpoint."""
    # Add tests here
    pass
EOF

echo "✓ Module '$MODULE_NAME' created successfully!"
echo ""
echo "Next steps:"
echo "1. Edit $MODULE_DIR/module.json with your module details"
echo "2. Add models to $MODULE_DIR/backend/models.py"
echo "3. Add API endpoints to $MODULE_DIR/backend/api.py"
echo "4. Add frontend components to $MODULE_DIR/frontend/"
echo "5. Enable module in customer config.json"
echo ""
echo "Module location: $MODULE_DIR"
