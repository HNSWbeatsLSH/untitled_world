# Modular Architecture Design

## Overview

The platform is designed with a **clear separation between core functionality and customer-specific customizations**. This enables:

- 🏢 Multi-tenant deployments with customer-specific features
- 🔌 Plugin-based architecture for easy customization
- 🔄 Easy upgrades to core functionality without affecting customizations
- 📦 Reusable modules across different customers
- 🎯 Clean separation of concerns

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Customer Layer                        │
│  (Customer-specific UI, workflows, business logic)      │
├─────────────────────────────────────────────────────────┤
│                    Module Layer                          │
│  (Pluggable modules: fraud detection, compliance, etc.) │
├─────────────────────────────────────────────────────────┤
│                    Core Platform                         │
│  (Standard ontology engine, API, visualization)         │
├─────────────────────────────────────────────────────────┤
│                    Infrastructure                        │
│  (Database, auth, caching, monitoring)                  │
└─────────────────────────────────────────────────────────┘
```

## Directory Structure

```
untitled_world/
├── core/                          # CORE PLATFORM (DO NOT MODIFY)
│   ├── backend/
│   │   ├── app/
│   │   │   ├── api/              # Standard REST API
│   │   │   ├── models/           # Base data models
│   │   │   ├── schemas/          # Base schemas
│   │   │   ├── services/         # Core services
│   │   │   └── core/             # Core configuration
│   │   └── requirements.txt
│   └── frontend/
│       └── src/
│           ├── components/       # Standard components
│           ├── pages/            # Standard pages
│           ├── services/         # Standard services
│           └── core/             # Core utilities
│
├── modules/                       # PLUGGABLE MODULES
│   ├── fraud-detection/          # Module: Fraud Detection
│   │   ├── backend/
│   │   │   ├── models.py        # Module-specific models
│   │   │   ├── api.py           # Module-specific endpoints
│   │   │   └── services.py      # Module business logic
│   │   ├── frontend/
│   │   │   ├── components/      # Module UI components
│   │   │   └── pages/           # Module pages
│   │   └── module.json          # Module metadata
│   │
│   ├── compliance/               # Module: Compliance
│   ├── kyc/                      # Module: KYC
│   ├── network-analysis/         # Module: Network Analysis
│   └── README.md                 # Module development guide
│
├── customers/                     # CUSTOMER CUSTOMIZATIONS
│   ├── customer-a/               # Customer A
│   │   ├── config.json          # Customer configuration
│   │   ├── backend/
│   │   │   ├── custom_api.py    # Custom endpoints
│   │   │   └── custom_logic.py  # Custom business logic
│   │   ├── frontend/
│   │   │   ├── theme.ts         # Custom theme
│   │   │   ├── components/      # Custom components
│   │   │   └── pages/           # Custom pages
│   │   └── data/
│   │       └── seed.py          # Customer-specific data
│   │
│   ├── customer-b/               # Customer B
│   └── README.md                 # Customer customization guide
│
├── shared/                        # SHARED UTILITIES
│   ├── utils/                    # Common utilities
│   ├── types/                    # Shared types
│   └── constants/                # Shared constants
│
├── deployments/                   # DEPLOYMENT CONFIGURATIONS
│   ├── customer-a/
│   │   ├── docker-compose.yml
│   │   └── .env.example
│   ├── customer-b/
│   └── README.md
│
└── docs/                          # DOCUMENTATION
    ├── core/                     # Core platform docs
    ├── modules/                  # Module development docs
    └── customers/                # Customer setup docs
```

## Module System

### Module Structure

Each module is self-contained with:

```
module-name/
├── module.json              # Module metadata
├── README.md                # Module documentation
├── backend/
│   ├── __init__.py
│   ├── models.py           # Additional DB models
│   ├── api.py              # API endpoints
│   ├── services.py         # Business logic
│   └── requirements.txt    # Module dependencies
├── frontend/
│   ├── components/         # UI components
│   ├── pages/              # Pages
│   ├── hooks/              # React hooks
│   └── package.json        # Frontend dependencies
└── tests/
    ├── test_api.py
    └── test_services.py
```

### Module Metadata (module.json)

```json
{
  "name": "fraud-detection",
  "version": "1.0.0",
  "displayName": "Fraud Detection",
  "description": "Advanced fraud detection and pattern analysis",
  "author": "Platform Team",
  "type": "standard",
  "dependencies": {
    "core": ">=0.1.0",
    "modules": []
  },
  "backend": {
    "enabled": true,
    "apiPrefix": "/api/v1/fraud",
    "models": ["backend/models.py"],
    "routes": ["backend/api.py"]
  },
  "frontend": {
    "enabled": true,
    "routes": [
      {
        "path": "/fraud-detection",
        "component": "FraudDashboard"
      }
    ],
    "menuItems": [
      {
        "label": "Fraud Detection",
        "icon": "shield-alert",
        "path": "/fraud-detection"
      }
    ]
  },
  "permissions": [
    "fraud.view",
    "fraud.investigate",
    "fraud.manage"
  ],
  "config": {
    "riskThreshold": 0.7,
    "alertingEnabled": true
  }
}
```

### Customer Configuration (customers/customer-a/config.json)

```json
{
  "customerId": "customer-a",
  "customerName": "Acme Corporation",
  "deployment": "cloud",
  "database": {
    "schema": "customer_a"
  },
  "modules": {
    "enabled": [
      "fraud-detection",
      "compliance",
      "kyc"
    ],
    "config": {
      "fraud-detection": {
        "riskThreshold": 0.8,
        "alertingEnabled": true,
        "customRules": [
          "velocity-check",
          "geo-anomaly"
        ]
      }
    }
  },
  "branding": {
    "logo": "assets/logo.png",
    "primaryColor": "#1e40af",
    "companyName": "Acme Corporation"
  },
  "features": {
    "authentication": "sso",
    "dataRetention": 365,
    "exportFormats": ["pdf", "excel", "json"]
  },
  "customizations": {
    "backend": "customers/customer-a/backend",
    "frontend": "customers/customer-a/frontend"
  }
}
```

## Implementation

### Backend Module Loader

```python
# core/backend/app/core/module_loader.py
```

### Frontend Module System

```typescript
// core/frontend/src/core/ModuleRegistry.ts
```

## Development Workflow

### 1. Developing Core Features
```bash
# Work in core/ directory
cd core/backend
# Make changes to core functionality
# All customers benefit from improvements
```

### 2. Creating a New Module
```bash
# Create module structure
./scripts/create-module.sh module-name

# Develop module independently
cd modules/module-name
# Develop backend logic
# Develop frontend UI
# Write tests

# Register module
# Module automatically available to customers
```

### 3. Customer Customization
```bash
# Create customer configuration
./scripts/create-customer.sh customer-name

# Enable modules for customer
# Edit customers/customer-name/config.json

# Add customer-specific code
cd customers/customer-name
# Add custom endpoints
# Add custom UI components
# Add custom business logic
```

## Best Practices

### ✅ DO

- **Keep core clean**: Core should be generic and reusable
- **Use modules**: Put industry-specific logic in modules
- **Customer config**: Use configuration over code for customer differences
- **Test modules**: Each module should have comprehensive tests
- **Document modules**: Clear documentation for each module
- **Version modules**: Semantic versioning for module releases
- **Isolate data**: Customer data isolated by schema/database

### ❌ DON'T

- **Don't modify core for one customer**: Create a module or customization
- **Don't hard-code customer logic**: Use configuration
- **Don't duplicate code**: Share common code via modules
- **Don't break interfaces**: Maintain backward compatibility
- **Don't mix concerns**: Keep modules independent

## Deployment Strategies

### Strategy 1: Multi-Tenant (Shared Infrastructure)
```
┌─────────────────────────────────────┐
│         Load Balancer               │
└──────────┬──────────────────────────┘
           │
    ┌──────▼──────┐
    │   API       │ ← Module Registry
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Database   │ ← Schema per customer
    │  customer_a │
    │  customer_b │
    └─────────────┘
```

### Strategy 2: Isolated (Per-Customer Infrastructure)
```
Customer A          Customer B
┌─────────┐        ┌─────────┐
│   API   │        │   API   │
├─────────┤        ├─────────┤
│   DB    │        │   DB    │
└─────────┘        └─────────┘
```

### Strategy 3: Hybrid
```
┌──────────────────────────┐
│    Shared Services       │
│  (Auth, Monitoring)      │
└──────────┬───────────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼───┐     ┌───▼───┐
│ Cust A│     │ Cust B│
│ Stack │     │ Stack │
└───────┘     └───────┘
```

## Module Types

### 1. Standard Modules (Provided by Platform)
- Fraud Detection
- Compliance & Audit
- KYC/AML
- Network Analysis
- Document Management

### 2. Industry Modules
- Financial Services
- Healthcare
- Retail
- Telecommunications
- Government

### 3. Customer Modules
- Customer-specific integrations
- Custom workflows
- Proprietary algorithms
- Legacy system connectors

## Upgrade Path

### Core Updates
```bash
# Pull latest core
git pull origin main

# Test with customer configurations
./scripts/test-customer.sh customer-a

# Deploy to customers
./scripts/deploy.sh --customer customer-a
```

### Module Updates
```bash
# Update module version
cd modules/fraud-detection
# Update code

# Test module
pytest tests/

# Publish module
./scripts/publish-module.sh fraud-detection

# Customers can opt-in to upgrade
```

## Configuration Management

### Environment Variables
```bash
# Core configuration
CORE_DATABASE_URL=postgresql://...
CORE_SECRET_KEY=...

# Customer configuration
CUSTOMER_ID=customer-a
CUSTOMER_CONFIG_PATH=customers/customer-a/config.json

# Module configuration
ENABLED_MODULES=fraud-detection,compliance,kyc
```

### Configuration Hierarchy
```
1. Core defaults
2. Module defaults
3. Customer configuration
4. Environment variables
5. Runtime overrides
```

## Security & Isolation

### Data Isolation
- **Database schemas**: Separate schema per customer
- **Row-level security**: Filter by customer_id
- **API isolation**: Customer-specific API keys

### Code Isolation
- **Module sandboxing**: Modules run in isolated context
- **Permission system**: Fine-grained permissions
- **Resource limits**: CPU/memory limits per customer

## Monitoring & Observability

### Per-Customer Metrics
- Request rates
- Error rates
- Performance metrics
- Module usage

### Module Metrics
- Module load times
- Module errors
- API call rates per module

## Example Use Cases

### Use Case 1: Financial Services Platform
```
Core Platform
+ Standard Modules:
  - Fraud Detection
  - Compliance
  - KYC
+ Customer A (Bank):
  - Custom: Wire transfer rules
  - Custom: Regulatory reporting
+ Customer B (Payment Processor):
  - Custom: Merchant risk scoring
  - Custom: Chargeback analysis
```

### Use Case 2: Healthcare Analytics
```
Core Platform
+ Standard Modules:
  - Network Analysis
  - Document Management
+ Customer A (Hospital):
  - Custom: Patient journey analysis
  - Custom: HIPAA compliance
+ Customer B (Pharma):
  - Custom: Drug interaction analysis
  - Custom: Clinical trial tracking
```

## Migration Path

### From Monolith to Modular
1. **Phase 1**: Identify core vs custom code
2. **Phase 2**: Extract modules from core
3. **Phase 3**: Move customer code to customizations
4. **Phase 4**: Test and validate
5. **Phase 5**: Deploy modular architecture

## Next Steps

1. Review this architecture document
2. Implement core module system
3. Create first standard module
4. Create example customer customization
5. Test multi-customer deployment
6. Document module development guide
