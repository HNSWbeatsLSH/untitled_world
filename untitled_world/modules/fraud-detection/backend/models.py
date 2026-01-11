"""
Fraud Detection Module - Database Models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import sys
from pathlib import Path

# Import core Base
core_path = Path(__file__).parent.parent.parent.parent / "core" / "backend"
sys.path.insert(0, str(core_path))

from app.core.database import Base


class FraudCase(Base):
    """
    Fraud case investigation.
    """
    __tablename__ = "fraud_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="open")  # open, investigating, closed
    priority = Column(String(20), nullable=False, default="medium")  # low, medium, high, critical
    risk_score = Column(Float, nullable=False, default=0.0)

    # Link to core entities
    subject_entity_id = Column(Integer, ForeignKey("entities.id"), nullable=True)

    # Fraud-specific data
    fraud_type = Column(String(100), nullable=True)  # payment, identity, account_takeover, etc.
    detection_method = Column(String(100), nullable=True)  # rule, ml_model, manual
    metadata = Column(JSON, nullable=False, default={})

    # Timestamps
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    alerts = relationship("FraudAlert", back_populates="case", cascade="all, delete-orphan")


class FraudAlert(Base):
    """
    Fraud alert/signal.
    """
    __tablename__ = "fraud_alerts"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("fraud_cases.id"), nullable=False, index=True)
    alert_type = Column(String(100), nullable=False)  # velocity, anomaly, rule_match
    severity = Column(String(20), nullable=False, default="medium")
    risk_score = Column(Float, nullable=False, default=0.0)

    # Alert details
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    rule_name = Column(String(200), nullable=True)
    triggered_by = Column(JSON, nullable=False, default={})  # What triggered this alert

    # Status
    status = Column(String(50), nullable=False, default="new")  # new, reviewed, false_positive, confirmed
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    case = relationship("FraudCase", back_populates="alerts")


class FraudRule(Base):
    """
    Configurable fraud detection rule.
    """
    __tablename__ = "fraud_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Rule configuration
    rule_type = Column(String(100), nullable=False)  # velocity, threshold, pattern, ml
    enabled = Column(Integer, default=1)
    priority = Column(Integer, default=100)

    # Rule definition
    conditions = Column(JSON, nullable=False, default={})
    actions = Column(JSON, nullable=False, default={})
    threshold_config = Column(JSON, nullable=False, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
