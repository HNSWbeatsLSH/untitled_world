#!/bin/bash

# Script to create a new customer configuration

set -e

if [ -z "$1" ]; then
    echo "Usage: ./create-customer.sh <customer-id> [customer-name]"
    echo "Example: ./create-customer.sh acme-corp 'Acme Corporation'"
    exit 1
fi

CUSTOMER_ID=$1
CUSTOMER_NAME=${2:-$(echo $1 | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')}
CUSTOMER_DIR="customers/$CUSTOMER_ID"

if [ -d "$CUSTOMER_DIR" ]; then
    echo "Error: Customer '$CUSTOMER_ID' already exists"
    exit 1
fi

echo "Creating customer: $CUSTOMER_ID ($CUSTOMER_NAME)"

# Create directory structure
mkdir -p "$CUSTOMER_DIR"/{backend,frontend/{components,pages,assets},data,docs}

# Create config.json
cat > "$CUSTOMER_DIR/config.json" << EOF
{
  "customerId": "$CUSTOMER_ID",
  "customerName": "$CUSTOMER_NAME",
  "deployment": "cloud",
  "database": {
    "schema": "${CUSTOMER_ID//-/_}",
    "retentionDays": 365
  },
  "modules": {
    "enabled": [],
    "config": {}
  },
  "branding": {
    "logo": "customers/$CUSTOMER_ID/assets/logo.png",
    "primaryColor": "#3b82f6",
    "secondaryColor": "#10b981",
    "companyName": "$CUSTOMER_NAME"
  },
  "features": {
    "authentication": {
      "method": "jwt",
      "mfaRequired": false
    },
    "dataRetention": {
      "entities": 365,
      "auditLogs": 730
    },
    "exportFormats": ["pdf", "json", "csv"]
  },
  "customizations": {
    "backend": {
      "enabled": false,
      "path": "customers/$CUSTOMER_ID/backend"
    },
    "frontend": {
      "enabled": false,
      "path": "customers/$CUSTOMER_ID/frontend"
    }
  },
  "limits": {
    "maxEntities": 1000000,
    "maxRelationships": 5000000,
    "maxConcurrentUsers": 50,
    "apiRateLimit": 100
  }
}
EOF

# Create README
cat > "$CUSTOMER_DIR/README.md" << EOF
# $CUSTOMER_NAME - Customer Customization

## Overview

This directory contains $CUSTOMER_NAME specific customizations.

## Customer Information

- **Customer ID**: $CUSTOMER_ID
- **Customer Name**: $CUSTOMER_NAME
- **Deployment Type**: Cloud

## Configuration

See \`config.json\` for complete configuration.

## Customizations

### Backend

Located in \`backend/\`:
- Custom API endpoints
- Custom business logic
- Integration code

### Frontend

Located in \`frontend/\`:
- Custom branding
- Custom components
- Custom pages

### Data

Located in \`data/\`:
- Customer-specific seed data
- Sample datasets

## Deployment

\`\`\`bash
# Deploy for $CUSTOMER_NAME
CUSTOMER_ID=$CUSTOMER_ID docker-compose up -d
\`\`\`

## Development

When developing customizations:
1. Keep core platform code in \`core/\`
2. Keep module code in \`modules/\`
3. Only customer-specific code goes here
EOF

# Create empty custom API file
cat > "$CUSTOMER_DIR/backend/custom_api.py" << EOF
"""
$CUSTOMER_NAME - Custom API Endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/info")
def get_customer_info():
    """Get customer information."""
    return {
        "customerId": "$CUSTOMER_ID",
        "customerName": "$CUSTOMER_NAME",
        "version": "1.0.0"
    }
EOF

# Create deployment config
mkdir -p "deployments/$CUSTOMER_ID"
cat > "deployments/$CUSTOMER_ID/docker-compose.yml" << EOF
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: \${DB_PASSWORD:-postgres}
      POSTGRES_DB: investigation_platform
    volumes:
      - ${CUSTOMER_ID}_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build:
      context: ../../core/backend
    environment:
      DATABASE_URL: postgresql://postgres:\${DB_PASSWORD:-postgres}@db:5432/investigation_platform
      CUSTOMER_ID: $CUSTOMER_ID
      SECRET_KEY: \${SECRET_KEY:-change-this-in-production}
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ../../:/app

  frontend:
    build:
      context: ../../core/frontend
    environment:
      VITE_API_URL: http://localhost:8000
      VITE_CUSTOMER_ID: $CUSTOMER_ID
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ../../core/frontend:/app

volumes:
  ${CUSTOMER_ID}_data:
EOF

cat > "deployments/$CUSTOMER_ID/.env.example" << EOF
# Customer: $CUSTOMER_NAME
CUSTOMER_ID=$CUSTOMER_ID
DB_PASSWORD=postgres
SECRET_KEY=change-this-in-production
EOF

echo "✓ Customer '$CUSTOMER_ID' created successfully!"
echo ""
echo "Next steps:"
echo "1. Edit $CUSTOMER_DIR/config.json to configure modules and features"
echo "2. Add custom branding to $CUSTOMER_DIR/frontend/assets/"
echo "3. Add custom backend code to $CUSTOMER_DIR/backend/"
echo "4. Add custom frontend code to $CUSTOMER_DIR/frontend/"
echo "5. Deploy with: cd deployments/$CUSTOMER_ID && docker-compose up -d"
echo ""
echo "Customer location: $CUSTOMER_DIR"
echo "Deployment config: deployments/$CUSTOMER_ID"
