"""
🗄️ GABRIEL DATABASE SCHEMA
PostgreSQL schema for MC96ECOUNIVERSE
100% Perfect Design
GORUNFREE Protocol
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, 
    Float, Text, ForeignKey, JSON, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    VOICE_ACTOR = "voice_actor"
    CLIENT = "client"
    GUEST = "guest"


class LicenseStatus(str, enum.Enum):
    """License status enumeration"""
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class TrainingStatus(str, enum.Enum):
    """Voice training status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ==================== USER MANAGEMENT ====================

class User(Base):
    """User model - Perfect design"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    full_name = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.GUEST, nullable=False)
    
    # OAuth
    oauth_provider = Column(String(50), nullable=True)  # google, apple, github
    oauth_id = Column(String(255), nullable=True)
    
    # Profile
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # 2FA
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    voice_actor_profile = relationship("VoiceActor", back_populates="user", uselist=False)
    client_profile = relationship("Client", back_populates="user", uselist=False)
    api_keys = relationship("APIKey", back_populates="user")
    sessions = relationship("Session", back_populates="user")


class Session(Base):
    """User session model"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    refresh_token = Column(String(500), unique=True, index=True, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="sessions")


class APIKey(Base):
    """API key model"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key_hash = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    last_used = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="api_keys")


# ==================== NOIZYVOX MODELS ====================

class VoiceActor(Base):
    """Voice actor profile model"""
    __tablename__ = "voice_actors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Profile
    stage_name = Column(String(255), nullable=True)
    portfolio_url = Column(String(500), nullable=True)
    demo_reel_url = Column(String(500), nullable=True)
    
    # Voice characteristics
    languages = Column(JSON, nullable=True)  # List of languages
    accents = Column(JSON, nullable=True)  # List of accents
    specialties = Column(JSON, nullable=True)  # List of specialties
    
    # Stats
    total_voices_created = Column(Integer, default=0, nullable=False)
    total_revenue = Column(Float, default=0.0, nullable=False)
    total_usage_minutes = Column(Float, default=0.0, nullable=False)
    
    # Settings
    revenue_share_percentage = Column(Float, default=70.0, nullable=False)  # 70% to actor
    auto_approve_licenses = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="voice_actor_profile")
    voice_models = relationship("VoiceModel", back_populates="actor")
    licenses = relationship("License", back_populates="actor")


class Client(Base):
    """Client profile model"""
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Profile
    company_name = Column(String(255), nullable=True)
    industry = Column(String(100), nullable=True)
    
    # Subscription
    subscription_tier = Column(String(50), default="free", nullable=False)  # free, pro, enterprise
    subscription_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Stats
    total_spent = Column(Float, default=0.0, nullable=False)
    total_usage_minutes = Column(Float, default=0.0, nullable=False)
    total_licenses = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="client_profile")
    licenses = relationship("License", back_populates="client")
    payments = relationship("Payment", back_populates="client")


class VoiceModel(Base):
    """AI voice model model"""
    __tablename__ = "voice_models"
    
    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("voice_actors.id"), nullable=False)
    
    # Model info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    voice_id = Column(String(255), unique=True, index=True, nullable=False)  # From ElevenLabs/Resemble
    
    # Training
    training_status = Column(Enum(TrainingStatus), default=TrainingStatus.PENDING, nullable=False)
    training_started_at = Column(DateTime(timezone=True), nullable=True)
    training_completed_at = Column(DateTime(timezone=True), nullable=True)
    training_error = Column(Text, nullable=True)
    
    # Audio samples
    sample_audio_url = Column(String(500), nullable=True)
    demo_audio_url = Column(String(500), nullable=True)
    
    # Characteristics
    language = Column(String(10), nullable=False, default="en")
    accent = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=True)
    age_range = Column(String(20), nullable=True)
    
    # Pricing
    price_per_minute = Column(Float, default=0.10, nullable=False)
    subscription_price = Column(Float, nullable=True)
    
    # Stats
    total_usage_minutes = Column(Float, default=0.0, nullable=False)
    total_revenue = Column(Float, default=0.0, nullable=False)
    total_generations = Column(Integer, default=0, nullable=False)
    
    # Settings
    is_public = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    actor = relationship("VoiceActor", back_populates="voice_models")
    licenses = relationship("License", back_populates="voice_model")
    generations = relationship("VoiceGeneration", back_populates="voice_model")


class License(Base):
    """Voice license model"""
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("voice_actors.id"), nullable=False)
    voice_model_id = Column(Integer, ForeignKey("voice_models.id"), nullable=False)
    
    # License details
    license_type = Column(String(50), nullable=False)  # one_time, subscription, unlimited
    status = Column(Enum(LicenseStatus), default=LicenseStatus.ACTIVE, nullable=False)
    
    # Usage limits
    usage_limit_minutes = Column(Float, nullable=True)  # Null = unlimited
    used_minutes = Column(Float, default=0.0, nullable=False)
    
    # Pricing
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Terms
    expires_at = Column(DateTime(timezone=True), nullable=True)
    usage_restrictions = Column(JSON, nullable=True)  # Commercial, non-commercial, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    client = relationship("Client", back_populates="licenses")
    actor = relationship("VoiceActor", back_populates="licenses")
    voice_model = relationship("VoiceModel", back_populates="licenses")
    payments = relationship("Payment", back_populates="license")
    generations = relationship("VoiceGeneration", back_populates="license")


class VoiceGeneration(Base):
    """Voice generation record"""
    __tablename__ = "voice_generations"
    
    id = Column(Integer, primary_key=True, index=True)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=False)
    voice_model_id = Column(Integer, ForeignKey("voice_models.id"), nullable=False)
    
    # Generation details
    text = Column(Text, nullable=False)
    audio_url = Column(String(500), nullable=False)
    duration_seconds = Column(Float, nullable=False)
    
    # Metadata
    service_used = Column(String(50), nullable=False)  # elevenlabs, resemble, etc.
    quality = Column(String(20), default="standard", nullable=False)
    language = Column(String(10), nullable=False)
    
    # Cost
    cost = Column(Float, nullable=False)
    revenue_share = Column(Float, nullable=False)  # Amount to actor
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    license = relationship("License", back_populates="generations")
    voice_model = relationship("VoiceModel", back_populates="generations")


class Payment(Base):
    """Payment record"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=True)
    
    # Payment details
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    payment_method = Column(String(50), nullable=False)  # stripe, paypal, etc.
    payment_intent_id = Column(String(255), unique=True, index=True, nullable=True)  # Stripe ID
    
    # Status
    status = Column(String(50), nullable=False)  # pending, completed, failed, refunded
    
    # Revenue split
    platform_fee = Column(Float, nullable=False)
    actor_revenue = Column(Float, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    client = relationship("Client", back_populates="payments")
    license = relationship("License", back_populates="payments")


# ==================== REMOTEDESKTOPKILLA MODELS ====================

class RemoteConnection(Base):
    """Remote desktop connection model"""
    __tablename__ = "remote_connections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Connection details
    connection_name = Column(String(255), nullable=False)
    target_host = Column(String(255), nullable=False)
    target_port = Column(Integer, default=21116, nullable=False)  # RustDesk default
    
    # Authentication
    password_hash = Column(String(255), nullable=True)
    key_pair_id = Column(String(255), nullable=True)
    
    # Settings
    auto_connect = Column(Boolean, default=False, nullable=False)
    quality = Column(String(20), default="high", nullable=False)  # low, medium, high, ultra
    resolution = Column(String(20), default="1080p", nullable=False)
    
    # Stats
    total_connections = Column(Integer, default=0, nullable=False)
    total_duration_seconds = Column(Integer, default=0, nullable=False)
    last_connected_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class FileTransfer(Base):
    """File transfer record"""
    __tablename__ = "file_transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("remote_connections.id"), nullable=False)
    
    # Transfer details
    file_name = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    direction = Column(String(10), nullable=False)  # upload, download
    status = Column(String(50), nullable=False)  # pending, in_progress, completed, failed
    
    # Progress
    bytes_transferred = Column(Integer, default=0, nullable=False)
    transfer_speed_mbps = Column(Float, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


# ==================== SYSTEM MODELS ====================

class SystemLog(Base):
    """System log entry"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    module = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)


class SystemMetric(Base):
    """System metric record"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20), nullable=True)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

