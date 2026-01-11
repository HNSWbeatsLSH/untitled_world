# Acme Bank - Customer Customization

## Overview

This directory contains Acme Bank-specific customizations to the Data Investigation Platform.

## Customer Information

- **Customer ID**: acme-bank
- **Customer Name**: Acme Bank Corporation
- **Deployment Type**: Cloud
- **Support Tier**: Enterprise

## Enabled Modules

- **Fraud Detection**: Advanced fraud detection with custom rules and thresholds

## Customizations

### Backend Customizations

Located in `backend/`:
- Custom API endpoints for Acme Bank specific workflows
- Integration with core banking system
- Custom business logic for risk scoring
- Compliance reporting endpoints

### Frontend Customizations

Located in `frontend/`:
- Custom branding (logo, colors)
- Acme Bank specific dashboards
- Custom reporting views
- Regulatory compliance screens

### Data

Located in `data/`:
- Customer-specific seed data
- Sample fraud patterns
- Test datasets

## Configuration

See `config.json` for complete configuration including:
- Module settings
- Feature flags
- Integration settings
- Compliance requirements

## Deployment

```bash
# Deploy for Acme Bank
CUSTOMER_ID=acme-bank docker-compose up -d

# Or manually
export CUSTOMER_ID=acme-bank
cd core/backend
uvicorn app.main:app --reload
```

## Development

When developing customizations for Acme Bank:

1. Keep core platform code in `core/`
2. Keep module code in `modules/`
3. Only Acme Bank-specific code goes here
4. Follow naming convention: `acme_*` for custom functions/classes

## Support

For support contact:
- **Technical Lead**: John Smith
- **Email**: john.smith@acmebank.com
- **Phone**: +1-555-0100
