# Modular Architecture - Quick Reference

## Overview

The platform is now structured with **clear separation between core, modules, and customers**:

```
📦 Core Platform          → Standard functionality for ALL customers
📦 Modules (Plugins)      → Reusable features for SOME customers
📦 Customer Customizations → Specific to ONE customer
```

## Directory Structure

```
untitled_world/
│
├── core/                      ← CORE PLATFORM (don't modify)
│   ├── backend/              → Standard API, ontology, database
│   └── frontend/             → Standard UI components
│
├── modules/                   ← PLUGGABLE MODULES (reusable features)
│   ├── fraud-detection/      → Example: Fraud detection module
│   ├── compliance/
│   └── kyc/
│
├── customers/                 ← CUSTOMER CUSTOMIZATIONS (one-off)
│   ├── acme-bank/            → Example: Acme Bank customization
│   ├── techcorp/
│   └── retailco/
│
├── shared/                    ← SHARED UTILITIES
├── deployments/               ← DEPLOYMENT CONFIGS (per customer)
├── scripts/                   ← HELPER SCRIPTS
└── docs/                      ← DOCUMENTATION
    ├── core/
    ├── modules/
    └── customers/
```

## Quick Commands

### Create a New Module

```bash
./scripts/create-module.sh my-module-name
```

Creates a complete module structure with:
- Backend API endpoints
- Database models
- Frontend components
- Configuration template

### Create a New Customer

```bash
./scripts/create-customer.sh customer-id "Customer Name"
```

Creates customer configuration with:
- Configuration file (config.json)
- Backend customization directory
- Frontend customization directory
- Deployment configuration

### Deploy for a Customer

```bash
# Set customer ID
export CUSTOMER_ID=acme-bank

# Start platform
cd core/backend
uvicorn app.main:app --reload

# Or using Docker
cd deployments/acme-bank
docker-compose up -d
```

## When to Use Each Layer

| Scenario | Layer | Action |
|----------|-------|--------|
| All customers need this feature | **Core** | Add to `core/` |
| Multiple customers might need this | **Module** | Create module in `modules/` |
| Only one customer needs this | **Customer** | Add to `customers/{id}/` |
| Customer-specific branding | **Customer** | Update `config.json` |
| Customer-specific data model | **Module** | Create module, enable for customer |

## Example Module: Fraud Detection

```
modules/fraud-detection/
├── module.json              # Metadata: name, version, config
├── backend/
│   ├── models.py           # FraudCase, FraudAlert, FraudRule
│   └── api.py              # /api/v1/fraud/* endpoints
└── frontend/
    ├── components/         # UI components
    └── pages/              # Fraud dashboard, alerts
```

Enable for customer:

```json
// customers/acme-bank/config.json
{
  "modules": {
    "enabled": ["fraud-detection"]
  }
}
```

## Example Customer: Acme Bank

```
customers/acme-bank/
├── config.json              # Configuration
│   ├── modules: enabled modules
│   ├── branding: colors, logo
│   └── features: SSO, compliance
├── backend/
│   ├── custom_api.py       # Custom endpoints
│   └── integrations.py     # Legacy system integration
└── frontend/
    ├── components/         # Custom components
    └── assets/             # Logo, favicon
```

Deploy:

```bash
CUSTOMER_ID=acme-bank docker-compose up -d
```

## Configuration Hierarchy

```
1. Core defaults (in code)
   ↓
2. Module defaults (module.json)
   ↓
3. Customer config (customers/{id}/config.json)
   ↓
4. Environment variables
```

## Module System

### How Modules Work

1. **Discovery**: Platform scans `modules/` directory
2. **Loading**: Reads `module.json` for each module
3. **Registration**: Registers models and API routes
4. **Activation**: Enables based on customer config

### Module Metadata

```json
{
  "name": "fraud-detection",
  "version": "1.0.0",
  "displayName": "Fraud Detection",
  "backend": {
    "enabled": true,
    "apiPrefix": "/api/v1/fraud",
    "models": ["backend/models.py"],
    "routes": ["backend/api.py"]
  },
  "frontend": {
    "enabled": true,
    "menuItems": [
      {
        "label": "Fraud Detection",
        "icon": "shield-alert",
        "path": "/fraud-detection"
      }
    ]
  }
}
```

## Development Workflow

### Adding Core Functionality

```bash
# Work in core directory
cd core/backend/app

# Make changes
# All customers automatically get this
```

### Creating a Module

```bash
# Create module
./scripts/create-module.sh compliance

# Develop
cd modules/compliance
# Add models, APIs, UI

# Test
pytest tests/

# Enable for customer
# Edit customers/{id}/config.json
```

### Customer Customization

```bash
# Create customer
./scripts/create-customer.sh customer-x

# Configure
# Edit customers/customer-x/config.json

# Add custom code
cd customers/customer-x/backend
# Add custom_api.py

# Deploy
CUSTOMER_ID=customer-x docker-compose up -d
```

## Key Files

| File | Purpose |
|------|---------|
| `core/backend/app/core/module_loader.py` | Module loading system |
| `modules/{name}/module.json` | Module metadata |
| `customers/{id}/config.json` | Customer configuration |
| `deployments/{id}/docker-compose.yml` | Customer deployment |

## API Structure

```
/api/v1/                     ← Core API
    /entities/               → Core ontology
    /relationships/          → Core relationships
    /graph/                  → Core graph operations

/api/v1/fraud/               ← Module: Fraud Detection
    /cases/                  → Fraud cases
    /alerts/                 → Fraud alerts
    /rules/                  → Detection rules

/api/v1/custom/              ← Customer: Custom endpoints
    /high-risk-accounts/     → Customer-specific
    /regulatory-report/      → Customer-specific
```

## Data Isolation

Each customer gets isolated data:

### Schema-Based (Recommended)

```sql
CREATE SCHEMA customer_a;
CREATE SCHEMA customer_b;

-- Customer A data in customer_a schema
-- Customer B data in customer_b schema
```

### Customer ID Filter

```python
# All queries filtered by customer_id
entities = db.query(Entity).filter(
    Entity.customer_id == current_customer_id
).all()
```

## Environment Variables

```bash
# Core
DATABASE_URL=postgresql://...
SECRET_KEY=...

# Customer
CUSTOMER_ID=acme-bank

# Customer-specific
CRM_DB_HOST=...
ALERT_WEBHOOK_URL=...
```

## Documentation

- **[Modular Architecture Design](ARCHITECTURE_MODULAR.md)** - Complete architecture overview
- **[Module Development Guide](docs/modules/MODULE_DEVELOPMENT_GUIDE.md)** - How to create modules
- **[Customer Customization Guide](docs/customers/CUSTOMER_CUSTOMIZATION_GUIDE.md)** - How to customize for customers

## Benefits

### For Platform Development

- ✅ **Clean core**: Core stays simple and generic
- ✅ **Reusable modules**: Write once, use for many customers
- ✅ **Easy upgrades**: Upgrade core without breaking customizations
- ✅ **Parallel development**: Teams can work on different modules

### For Customers

- ✅ **Fast deployment**: Enable/disable features via config
- ✅ **Customization**: Add customer-specific code without forking
- ✅ **Isolation**: Customer data and code isolated
- ✅ **Scalability**: Add features without core changes

## Migration from Old Structure

```bash
# Old structure
backend/         → Move to core/backend/
frontend/        → Move to core/frontend/

# Extract modules
# Identify reusable features
# Move to modules/{name}/

# Extract customer code
# Identify customer-specific code
# Move to customers/{id}/
```

## Common Patterns

### Pattern 1: Standard Module for All

```json
// Enable for all customers
{
  "modules": {
    "enabled": ["fraud-detection"]
  }
}
```

### Pattern 2: Module with Custom Config

```json
// Enable with custom settings
{
  "modules": {
    "enabled": ["fraud-detection"],
    "config": {
      "fraud-detection": {
        "riskThreshold": 0.9
      }
    }
  }
}
```

### Pattern 3: Custom Integration

```python
// customers/{id}/backend/integrations.py
# Customer-specific integration code
```

## Troubleshooting

### Module Not Loading

1. Check `module.json` is valid
2. Module is in `modules/` directory
3. Enabled in customer config
4. Check logs for errors

### Customer Config Not Applied

1. `CUSTOMER_ID` environment variable set
2. Config file at `customers/{id}/config.json`
3. JSON is valid
4. Restart backend

### Custom Code Not Working

1. Path correct in config.json
2. Customizations enabled
3. Import paths correct
4. Check logs

## Examples

See:
- `modules/fraud-detection/` - Example module
- `customers/acme-bank/` - Example customer
- `deployments/acme-bank/` - Example deployment

## Support

- Read docs in `docs/` directory
- Check example modules and customers
- Review configuration files
- Contact platform team

---

**Quick Start:**

1. Create module: `./scripts/create-module.sh my-module`
2. Create customer: `./scripts/create-customer.sh my-customer`
3. Deploy: `CUSTOMER_ID=my-customer docker-compose up -d`
