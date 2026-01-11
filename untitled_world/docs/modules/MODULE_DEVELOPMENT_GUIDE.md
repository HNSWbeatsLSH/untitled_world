# Module Development Guide

## Overview

This guide explains how to develop reusable modules for the Data Investigation Platform.

## What is a Module?

A **module** is a self-contained piece of functionality that can be:
- Enabled/disabled per customer
- Configured independently
- Developed and tested separately
- Reused across multiple customers

**Examples:**
- Fraud Detection
- Compliance & Audit
- KYC/AML Verification
- Network Analysis
- Document Management

## Module vs Core vs Customer

| Layer | Purpose | Examples | Changes Affect |
|-------|---------|----------|----------------|
| **Core** | Base platform functionality | Ontology engine, auth, API | All customers |
| **Module** | Reusable features | Fraud detection, compliance | Customers using module |
| **Customer** | Customer-specific code | Custom integrations, branding | Single customer only |

## Creating a New Module

### Quick Start

```bash
# Create module structure
./scripts/create-module.sh my-module

# Navigate to module
cd modules/my-module
```

### Manual Creation

#### 1. Directory Structure

```
modules/my-module/
├── module.json              # Module metadata
├── README.md                # Module documentation
├── backend/
│   ├── __init__.py
│   ├── models.py           # Database models
│   ├── api.py              # API endpoints
│   ├── services.py         # Business logic
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── components/         # React components
│   ├── pages/              # Page components
│   ├── hooks/              # Custom hooks
│   └── package.json        # Frontend dependencies
└── tests/
    ├── test_api.py
    └── test_services.py
```

#### 2. Module Metadata (module.json)

```json
{
  "name": "my-module",
  "version": "1.0.0",
  "displayName": "My Module",
  "description": "Module description",
  "author": "Platform Team",
  "type": "standard",
  "dependencies": {
    "core": ">=0.1.0",
    "modules": []
  },
  "backend": {
    "enabled": true,
    "apiPrefix": "/api/v1/my-module",
    "models": ["backend/models.py"],
    "routes": ["backend/api.py"]
  },
  "frontend": {
    "enabled": true,
    "routes": [
      {
        "path": "/my-module",
        "component": "Dashboard"
      }
    ],
    "menuItems": [
      {
        "label": "My Module",
        "icon": "box",
        "path": "/my-module",
        "order": 10
      }
    ]
  },
  "permissions": [
    "my-module.view",
    "my-module.edit",
    "my-module.delete"
  ],
  "config": {
    "defaultOption": "value",
    "threshold": 0.8
  }
}
```

#### 3. Backend Models

```python
# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
import sys
from pathlib import Path

# Import core Base
core_path = Path(__file__).parent.parent.parent.parent / "core" / "backend"
sys.path.insert(0, str(core_path))

from app.core.database import Base


class MyModel(Base):
    """My module model."""
    __tablename__ = "my_module_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

#### 4. Backend API

```python
# backend/api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
from pathlib import Path

core_path = Path(__file__).parent.parent.parent.parent / "core" / "backend"
sys.path.insert(0, str(core_path))

from app.core.database import get_db
from .models import MyModel

router = APIRouter()


@router.get("/items")
def list_items(db: Session = Depends(get_db)):
    """List all items."""
    items = db.query(MyModel).all()
    return items


@router.post("/items")
def create_item(item_data: dict, db: Session = Depends(get_db)):
    """Create a new item."""
    item = MyModel(**item_data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
```

#### 5. Frontend Components

```tsx
// frontend/components/ItemList.tsx
import { useQuery } from '@tanstack/react-query';
import api from '@/services/api';

export const ItemList = () => {
  const { data: items } = useQuery({
    queryKey: ['my-module-items'],
    queryFn: () => api.get('/api/v1/my-module/items').then(res => res.data),
  });

  return (
    <div>
      {items?.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  );
};
```

## Module Configuration

### Default Configuration

Set in `module.json`:

```json
{
  "config": {
    "defaultOption": "value",
    "threshold": 0.8
  }
}
```

### Customer Override

In `customers/{customer-id}/config.json`:

```json
{
  "modules": {
    "config": {
      "my-module": {
        "threshold": 0.9
      }
    }
  }
}
```

### Access in Code

```python
from app.core.module_loader import module_loader

customer_id = os.getenv("CUSTOMER_ID")
config = module_loader.get_module_config_for_customer(
    customer_id,
    "my-module"
)

threshold = config.get("threshold", 0.8)
```

## Testing Modules

### Backend Tests

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient


def test_list_items(client):
    response = client.get("/api/v1/my-module/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_item(client):
    data = {"name": "Test Item"}
    response = client.post("/api/v1/my-module/items", json=data)
    assert response.status_code == 201
```

### Frontend Tests

```typescript
// tests/ItemList.test.tsx
import { render, screen } from '@testing-library/react';
import { ItemList } from '../components/ItemList';

test('renders item list', () => {
  render(<ItemList />);
  expect(screen.getByText(/items/i)).toBeInTheDocument();
});
```

## Module Dependencies

### Depend on Core

All modules depend on core platform:

```json
{
  "dependencies": {
    "core": ">=0.1.0"
  }
}
```

### Depend on Other Modules

```json
{
  "dependencies": {
    "core": ">=0.1.0",
    "modules": ["fraud-detection"]
  }
}
```

## Best Practices

### ✅ DO

- **Keep modules independent**: Minimize dependencies
- **Use configuration**: Make modules configurable
- **Document well**: Clear README and API docs
- **Write tests**: Comprehensive test coverage
- **Follow naming conventions**: `module_*` for custom code
- **Handle errors gracefully**: Don't crash the whole platform
- **Log appropriately**: Use structured logging

### ❌ DON'T

- **Don't modify core**: Keep core pristine
- **Don't hard-code**: Use configuration
- **Don't break interfaces**: Maintain backward compatibility
- **Don't leak customer data**: Respect data isolation
- **Don't duplicate code**: Share via utilities

## Module Lifecycle

### 1. Development

```bash
# Create module
./scripts/create-module.sh my-module

# Develop features
cd modules/my-module

# Test
pytest tests/
```

### 2. Registration

Module is automatically discovered when placed in `modules/` directory.

### 3. Enabling for Customer

```json
// customers/customer-a/config.json
{
  "modules": {
    "enabled": ["my-module"]
  }
}
```

### 4. Deployment

```bash
# Deploy with module enabled
CUSTOMER_ID=customer-a docker-compose up -d
```

### 5. Updates

```bash
# Update module code
cd modules/my-module

# Test changes
pytest tests/

# Deploy update
# Module updates automatically loaded on restart
```

## Advanced Topics

### Dynamic Model Registration

Models are automatically registered with SQLAlchemy when module loads.

### Route Registration

Routes are automatically added to FastAPI app via module loader.

### Permission System

```python
from fastapi import Depends
from app.core.auth import require_permission

@router.get("/secure")
@require_permission("my-module.view")
def secure_endpoint():
    return {"data": "secret"}
```

### Database Migrations

```bash
# Create migration for module
cd core/backend
alembic revision -m "Add my_module tables"

# Edit migration file to create module tables
# Run migration
alembic upgrade head
```

### Frontend Integration

Modules can register menu items and routes in `module.json`:

```json
{
  "frontend": {
    "menuItems": [
      {
        "label": "My Module",
        "icon": "box",
        "path": "/my-module",
        "order": 10
      }
    ]
  }
}
```

## Module Distribution

### Internal Modules

Place in `modules/` directory - automatically available.

### External Modules

```bash
# Clone external module
git clone <module-repo> modules/my-module

# Install dependencies
cd modules/my-module
pip install -r backend/requirements.txt
npm install
```

## Example Modules

### 1. Fraud Detection

- **Purpose**: Detect fraudulent patterns
- **Models**: FraudCase, FraudAlert, FraudRule
- **APIs**: Cases, alerts, rules, stats
- **Frontend**: Dashboard, case management

### 2. Compliance

- **Purpose**: Regulatory compliance tracking
- **Models**: ComplianceCheck, AuditLog, Policy
- **APIs**: Checks, audits, policies
- **Frontend**: Compliance dashboard, reporting

### 3. KYC

- **Purpose**: Know Your Customer verification
- **Models**: KYCProfile, Verification, Document
- **APIs**: Profiles, verifications, documents
- **Frontend**: KYC workflow, document upload

## Troubleshooting

### Module Not Loading

Check:
1. `module.json` is valid JSON
2. Module is in `modules/` directory
3. Module is enabled in customer config
4. Check backend logs for import errors

### API Endpoints Not Appearing

Check:
1. `backend.enabled: true` in module.json
2. Router is created in `backend/api.py`
3. `router` variable is exported
4. Module successfully loaded (check logs)

### Frontend Components Not Showing

Check:
1. `frontend.enabled: true` in module.json
2. Routes are configured correctly
3. Components are properly exported
4. Check browser console for errors

## Support

For help with module development:
- Check example modules in `modules/`
- Review core API in `core/backend/app/`
- See customer examples in `customers/`
- Contact platform team
