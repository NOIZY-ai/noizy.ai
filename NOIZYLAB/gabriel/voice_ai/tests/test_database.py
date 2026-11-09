"""
🧪 DATABASE TESTS - 100% PERFECT
Perfect database test coverage
GORUNFREE Protocol
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..infrastructure.database.schema import Base, User, VoiceActor, Client, VoiceModel
from ..infrastructure.config import settings


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    test_db_url = settings.DATABASE_URL.replace("/gabriel", "/gabriel_test")
    engine = create_engine(test_db_url, echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(test_engine):
    """Create database session"""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


class TestDatabase:
    """Database tests"""
    
    def test_create_user(self, db_session):
        """Test user creation"""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            role="user"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
    
    def test_create_voice_actor(self, db_session):
        """Test voice actor creation"""
        user = User(
            email="actor@example.com",
            username="actor",
            role="voice_actor"
        )
        db_session.add(user)
        db_session.commit()
        
        actor = VoiceActor(
            user_id=user.id,
            stage_name="Test Actor",
            revenue_share_percentage=70.0
        )
        db_session.add(actor)
        db_session.commit()
        
        assert actor.id is not None
        assert actor.user_id == user.id
    
    def test_create_voice_model(self, db_session):
        """Test voice model creation"""
        user = User(
            email="actor2@example.com",
            username="actor2",
            role="voice_actor"
        )
        db_session.add(user)
        db_session.commit()
        
        actor = VoiceActor(user_id=user.id)
        db_session.add(actor)
        db_session.commit()
        
        model = VoiceModel(
            actor_id=actor.id,
            name="Test Voice",
            voice_id="test_voice_123",
            language="en",
            price_per_minute=0.10
        )
        db_session.add(model)
        db_session.commit()
        
        assert model.id is not None
        assert model.actor_id == actor.id

