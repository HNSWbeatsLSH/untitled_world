"""
Fraud Detection Module - API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import sys
from pathlib import Path

# Import core dependencies
core_path = Path(__file__).parent.parent.parent.parent / "core" / "backend"
sys.path.insert(0, str(core_path))

from app.core.database import get_db
from .models import FraudCase, FraudAlert, FraudRule

router = APIRouter()


@router.get("/cases")
def list_fraud_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List fraud cases with optional filtering."""
    query = db.query(FraudCase)

    if status:
        query = query.filter(FraudCase.status == status)

    cases = query.order_by(FraudCase.created_at.desc()).offset(skip).limit(limit).all()
    return cases


@router.post("/cases", status_code=201)
def create_fraud_case(
    case_data: dict,
    db: Session = Depends(get_db),
):
    """Create a new fraud case."""
    # Generate case number
    case_count = db.query(FraudCase).count()
    case_number = f"FRAUD-{case_count + 1:06d}"

    fraud_case = FraudCase(
        case_number=case_number,
        title=case_data.get('title'),
        description=case_data.get('description'),
        status=case_data.get('status', 'open'),
        priority=case_data.get('priority', 'medium'),
        risk_score=case_data.get('risk_score', 0.0),
        subject_entity_id=case_data.get('subject_entity_id'),
        fraud_type=case_data.get('fraud_type'),
        detection_method=case_data.get('detection_method', 'manual'),
        metadata=case_data.get('metadata', {}),
    )

    db.add(fraud_case)
    db.commit()
    db.refresh(fraud_case)
    return fraud_case


@router.get("/cases/{case_id}")
def get_fraud_case(case_id: int, db: Session = Depends(get_db)):
    """Get fraud case details."""
    case = db.query(FraudCase).filter(FraudCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Fraud case not found")
    return case


@router.put("/cases/{case_id}")
def update_fraud_case(
    case_id: int,
    case_data: dict,
    db: Session = Depends(get_db),
):
    """Update a fraud case."""
    case = db.query(FraudCase).filter(FraudCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Fraud case not found")

    for key, value in case_data.items():
        if hasattr(case, key):
            setattr(case, key, value)

    if case_data.get('status') == 'closed' and not case.closed_at:
        case.closed_at = datetime.utcnow()

    db.commit()
    db.refresh(case)
    return case


@router.get("/alerts")
def list_fraud_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    status: Optional[str] = None,
    case_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List fraud alerts."""
    query = db.query(FraudAlert)

    if status:
        query = query.filter(FraudAlert.status == status)

    if case_id:
        query = query.filter(FraudAlert.case_id == case_id)

    alerts = query.order_by(FraudAlert.created_at.desc()).offset(skip).limit(limit).all()
    return alerts


@router.post("/alerts", status_code=201)
def create_fraud_alert(
    alert_data: dict,
    db: Session = Depends(get_db),
):
    """Create a new fraud alert."""
    alert = FraudAlert(
        case_id=alert_data.get('case_id'),
        alert_type=alert_data.get('alert_type'),
        severity=alert_data.get('severity', 'medium'),
        risk_score=alert_data.get('risk_score', 0.0),
        title=alert_data.get('title'),
        description=alert_data.get('description'),
        rule_name=alert_data.get('rule_name'),
        triggered_by=alert_data.get('triggered_by', {}),
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@router.get("/rules")
def list_fraud_rules(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    enabled: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """List fraud detection rules."""
    query = db.query(FraudRule)

    if enabled is not None:
        query = query.filter(FraudRule.enabled == (1 if enabled else 0))

    rules = query.order_by(FraudRule.priority.desc()).offset(skip).limit(limit).all()
    return rules


@router.post("/rules", status_code=201)
def create_fraud_rule(
    rule_data: dict,
    db: Session = Depends(get_db),
):
    """Create a new fraud detection rule."""
    rule = FraudRule(
        name=rule_data.get('name'),
        display_name=rule_data.get('display_name'),
        description=rule_data.get('description'),
        rule_type=rule_data.get('rule_type'),
        enabled=rule_data.get('enabled', 1),
        priority=rule_data.get('priority', 100),
        conditions=rule_data.get('conditions', {}),
        actions=rule_data.get('actions', {}),
        threshold_config=rule_data.get('threshold_config', {}),
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.get("/stats")
def get_fraud_stats(db: Session = Depends(get_db)):
    """Get fraud detection statistics."""
    total_cases = db.query(FraudCase).count()
    open_cases = db.query(FraudCase).filter(FraudCase.status == 'open').count()
    closed_cases = db.query(FraudCase).filter(FraudCase.status == 'closed').count()

    total_alerts = db.query(FraudAlert).count()
    new_alerts = db.query(FraudAlert).filter(FraudAlert.status == 'new').count()

    return {
        "total_cases": total_cases,
        "open_cases": open_cases,
        "closed_cases": closed_cases,
        "total_alerts": total_alerts,
        "new_alerts": new_alerts,
    }
