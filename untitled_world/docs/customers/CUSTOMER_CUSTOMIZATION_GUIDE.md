# Customer Customization Guide

## Overview

This guide explains how to create and manage customer-specific customizations for the Data Investigation Platform.

## What are Customer Customizations?

**Customer customizations** are code and configuration specific to ONE customer that:
- Don't belong in core (not generic enough)
- Don't belong in modules (not reusable enough)
- Are unique to customer's business needs

**Examples:**
- Integration with customer's legacy systems
- Custom branding and logos
- Customer-specific workflows
- Proprietary algorithms
- Regulatory requirements unique to customer

## When to Use Each Layer

```
┌─────────────────────────────────────────┐
│ Is it needed by ALL customers?          │
│ → YES: Put in CORE                       │
└─────────────────────────────────────────┘
                  ↓ NO
┌─────────────────────────────────────────┐
│ Is it reusable by MULTIPLE customers?   │
│ → YES: Create a MODULE                   │
└─────────────────────────────────────────┘
                  ↓ NO
┌─────────────────────────────────────────┐
│ Is it specific to ONE customer?          │
│ → YES: Create CUSTOMER CUSTOMIZATION    │
└─────────────────────────────────────────┘
```

## Creating a New Customer

### Quick Start

```bash
# Create customer configuration
./scripts/create-customer.sh customer-id "Customer Name"

# Navigate to customer directory
cd customers/customer-id
```

### Manual Creation

#### 1. Directory Structure

```
customers/customer-id/
├── config.json              # Customer configuration
├── README.md                # Customer documentation
├── backend/
│   ├── custom_api.py       # Custom API endpoints
│   ├── custom_logic.py     # Custom business logic
│   └── integrations.py     # External integrations
├── frontend/
│   ├── theme.ts            # Custom theme
│   ├── components/         # Custom components
│   ├── pages/              # Custom pages
│   └── assets/
│       ├── logo.png        # Customer logo
│       └── favicon.ico     # Customer favicon
├── data/
│   └── seed.py             # Customer-specific seed data
└── docs/
    └── setup.md            # Customer-specific docs
```

#### 2. Customer Configuration (config.json)

```json
{
  "customerId": "customer-id",
  "customerName": "Customer Name",
  "deployment": "cloud",
  "database": {
    "schema": "customer_schema",
    "retentionDays": 365
  },
  "modules": {
    "enabled": ["fraud-detection", "compliance"],
    "config": {
      "fraud-detection": {
        "riskThreshold": 0.85
      }
    }
  },
  "branding": {
    "logo": "customers/customer-id/assets/logo.png",
    "primaryColor": "#1e40af",
    "companyName": "Customer Name"
  },
  "features": {
    "authentication": {
      "method": "sso",
      "provider": "okta"
    },
    "dataRetention": {
      "entities": 365,
      "auditLogs": 730
    }
  },
  "customizations": {
    "backend": {
      "enabled": true,
      "path": "customers/customer-id/backend"
    },
    "frontend": {
      "enabled": true,
      "path": "customers/customer-id/frontend"
    }
  }
}
```

## Configuration Options

### Database Configuration

```json
{
  "database": {
    "schema": "customer_schema",   // PostgreSQL schema for data isolation
    "retentionDays": 365,           // Data retention period
    "backup": {
      "enabled": true,
      "schedule": "0 2 * * *"       // Daily at 2 AM
    }
  }
}
```

### Module Configuration

```json
{
  "modules": {
    "enabled": [
      "fraud-detection",
      "compliance",
      "kyc"
    ],
    "config": {
      "fraud-detection": {
        "riskThreshold": 0.85,
        "autoBlock": false,
        "customRules": ["velocity-check", "geo-anomaly"]
      },
      "compliance": {
        "regulations": ["SOX", "GDPR", "PCI"],
        "reportingEnabled": true
      }
    }
  }
}
```

### Branding Configuration

```json
{
  "branding": {
    "logo": "customers/customer-id/assets/logo.png",
    "favicon": "customers/customer-id/assets/favicon.ico",
    "primaryColor": "#1e40af",
    "secondaryColor": "#dc2626",
    "companyName": "Customer Name",
    "tagline": "Customer Tagline",
    "customCSS": "customers/customer-id/frontend/custom.css"
  }
}
```

### Feature Flags

```json
{
  "features": {
    "authentication": {
      "method": "sso",        // jwt, sso, saml
      "provider": "okta",     // okta, auth0, custom
      "mfaRequired": true
    },
    "exportFormats": ["pdf", "excel", "json", "csv"],
    "notifications": {
      "email": true,
      "slack": true,
      "webhook": true
    },
    "compliance": {
      "gdpr": true,
      "sox": true,
      "pci": true
    }
  }
}
```

### Integration Configuration

```json
{
  "integrations": [
    {
      "name": "crm-system",
      "type": "database",
      "config": {
        "host": "${CRM_DB_HOST}",
        "database": "crm",
        "readonly": true
      }
    },
    {
      "name": "alert-webhook",
      "type": "webhook",
      "config": {
        "url": "${ALERT_WEBHOOK_URL}",
        "headers": {
          "Authorization": "Bearer ${API_KEY}"
        }
      }
    }
  ]
}
```

## Backend Customizations

### Custom API Endpoints

```python
# customers/customer-id/backend/custom_api.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
from pathlib import Path

# Import core dependencies
core_path = Path(__file__).parent.parent.parent.parent / "core" / "backend"
sys.path.insert(0, str(core_path))

from app.core.database import get_db

router = APIRouter()


@router.get("/custom-endpoint")
def custom_endpoint(db: Session = Depends(get_db)):
    """Customer-specific endpoint."""
    # Custom logic here
    return {"message": "Customer-specific data"}


@router.post("/integrate/legacy-system")
def integrate_legacy_system(data: dict, db: Session = Depends(get_db)):
    """Integrate with customer's legacy system."""
    # Integration logic
    return {"status": "success"}
```

### Custom Business Logic

```python
# customers/customer-id/backend/custom_logic.py

def calculate_custom_risk_score(entity_data: dict) -> float:
    """
    Customer-specific risk scoring algorithm.

    This implements the proprietary risk model
    developed for this specific customer.
    """
    # Custom scoring logic
    score = 0.0

    # Customer-specific rules
    if entity_data.get('flag_a'):
        score += 0.3

    if entity_data.get('value') > 1000000:
        score += 0.5

    return min(score, 1.0)
```

### External Integration

```python
# customers/customer-id/backend/integrations.py

import requests

class LegacySystemClient:
    """Client for customer's legacy system."""

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def fetch_customer_data(self, customer_id: str):
        """Fetch data from legacy system."""
        response = requests.get(
            f"{self.api_url}/customers/{customer_id}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()
```

## Frontend Customizations

### Custom Theme

```typescript
// customers/customer-id/frontend/theme.ts

export const customTheme = {
  colors: {
    primary: '#1e40af',
    secondary: '#dc2626',
    background: '#f9fafb',
    text: '#111827',
  },
  fonts: {
    heading: 'Arial, sans-serif',
    body: 'Helvetica, sans-serif',
  },
  logo: '/customers/customer-id/assets/logo.png',
};
```

### Custom Components

```tsx
// customers/customer-id/frontend/components/CustomDashboard.tsx

import { useQuery } from '@tanstack/react-query';

export const CustomDashboard = () => {
  const { data } = useQuery({
    queryKey: ['custom-data'],
    queryFn: () => fetch('/api/v1/custom-endpoint').then(r => r.json()),
  });

  return (
    <div className="custom-dashboard">
      <h1>Customer-Specific Dashboard</h1>
      {/* Custom visualizations */}
    </div>
  );
};
```

### Custom Pages

```tsx
// customers/customer-id/frontend/pages/CustomReport.tsx

export const CustomReport = () => {
  return (
    <div>
      <h1>Regulatory Report</h1>
      {/* Customer-specific reporting interface */}
    </div>
  );
};
```

## Data Isolation

### Schema-Based Isolation

Each customer gets their own PostgreSQL schema:

```sql
-- Customer A data
CREATE SCHEMA customer_a;
CREATE TABLE customer_a.entities (...);

-- Customer B data
CREATE SCHEMA customer_b;
CREATE TABLE customer_b.entities (...);
```

### Row-Level Security

```python
# Add customer_id to all queries
from app.core.database import get_db

def get_entities(customer_id: str, db: Session):
    return db.query(Entity).filter(
        Entity.customer_id == customer_id
    ).all()
```

## Deployment

### Single Customer Deployment

```bash
# Navigate to customer deployment
cd deployments/customer-id

# Configure environment
cp .env.example .env
# Edit .env with customer credentials

# Start services
docker-compose up -d
```

### Multi-Tenant Deployment

```bash
# Set customer ID environment variable
export CUSTOMER_ID=customer-a

# Start platform
cd core/backend
uvicorn app.main:app --reload
```

## Environment Variables

```bash
# Customer Configuration
CUSTOMER_ID=customer-id

# Database
DATABASE_URL=postgresql://user:pass@host/db

# Customer-specific
CRM_DB_HOST=customer-crm.example.com
ALERT_WEBHOOK_URL=https://alerts.customer.com/webhook
API_KEY=customer-secret-key

# Features
ENABLE_SSO=true
SSO_PROVIDER=okta
```

## Testing Customizations

### Backend Tests

```python
# customers/customer-id/tests/test_custom_api.py

import pytest
from fastapi.testclient import TestClient

def test_custom_endpoint(client):
    response = client.get("/api/v1/custom-endpoint")
    assert response.status_code == 200
    assert "message" in response.json()
```

### Frontend Tests

```typescript
// customers/customer-id/tests/CustomDashboard.test.tsx

import { render } from '@testing-library/react';
import { CustomDashboard } from '../components/CustomDashboard';

test('renders custom dashboard', () => {
  const { getByText } = render(<CustomDashboard />);
  expect(getByText(/Customer-Specific Dashboard/i)).toBeInTheDocument();
});
```

## Best Practices

### ✅ DO

- **Isolate customer data**: Use schemas or customer_id filters
- **Document customizations**: Clear README for each customer
- **Use configuration over code**: Prefer config.json changes
- **Version control**: Track customer code in version control
- **Test thoroughly**: Test customizations separately
- **Follow naming conventions**: `customer_*` prefix for custom code
- **Handle errors gracefully**: Don't break platform for other customers

### ❌ DON'T

- **Don't modify core**: Keep core pristine
- **Don't modify modules**: Fork if needed, don't modify
- **Don't hard-code secrets**: Use environment variables
- **Don't duplicate code**: Share via modules if reusable
- **Don't leak data**: Respect data isolation
- **Don't break interfaces**: Maintain API compatibility

## Migration Guide

### Migrating from Monolith

1. **Identify customer code**: Find customer-specific code in monolith
2. **Create customer directory**: `./scripts/create-customer.sh customer-id`
3. **Move custom code**: Copy to `customers/customer-id/`
4. **Update imports**: Fix import paths
5. **Test**: Ensure everything works
6. **Deploy**: Deploy with customer configuration

### Upgrading Core

1. **Pull latest core**: `git pull origin main`
2. **Test with customer config**: Run tests
3. **Check breaking changes**: Review changelog
4. **Update customizations**: If needed
5. **Deploy**: Roll out to customers

## Troubleshooting

### Customization Not Loading

Check:
1. `customizations.backend.enabled: true` in config.json
2. Path is correct in config.json
3. CUSTOMER_ID environment variable is set
4. Check backend logs for import errors

### Integration Failing

Check:
1. Environment variables are set correctly
2. Network connectivity to external system
3. API keys and credentials are valid
4. Check integration logs

### Branding Not Showing

Check:
1. Asset files exist at specified paths
2. Paths are correct in config.json
3. Frontend is rebuilding assets
4. Check browser console for 404 errors

## Example Customers

### 1. Acme Bank

- **Industry**: Financial Services
- **Modules**: Fraud Detection, Compliance, KYC
- **Customizations**:
  - Wire transfer monitoring
  - Regulatory reporting
  - Core banking integration

### 2. TechCorp Retail

- **Industry**: Retail
- **Modules**: Network Analysis, Document Management
- **Customizations**:
  - Inventory system integration
  - Customer journey mapping
  - Sales analytics

## Support

For customer-specific issues:
1. Check customer documentation in `customers/{id}/docs/`
2. Review customer configuration in `config.json`
3. Check deployment logs
4. Contact customer success team
5. Escalate to engineering if needed
