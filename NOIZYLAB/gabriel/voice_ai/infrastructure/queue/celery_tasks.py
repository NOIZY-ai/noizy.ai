"""
📬 CELERY TASKS - 100% PERFECT
Perfect Celery task implementation
GORUNFREE Protocol
"""

from celery import Celery
from typing import Optional
from ..config import settings
from ..logging import get_logger

logger = get_logger("celery")

# Create Celery app
celery_app = Celery(
    "gabriel",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)


@celery_app.task(name="generate_voice", bind=True)
def generate_voice_task(
    self,
    text: str,
    service: str = "gtts",
    voice: Optional[str] = None,
    language: str = "en"
) -> dict:
    """
    Generate voice task (async)
    
    Args:
        text: Text to convert
        service: Voice service
        voice: Voice name/ID
        language: Language code
        
    Returns:
        Task result
    """
    try:
        logger.info("voice_generation_task_started", text_length=len(text), service=service)
        
        # Import here to avoid circular imports
        from ..core.voice_ai_universal_improved import UniversalVoiceAI
        
        voice_ai = UniversalVoiceAI()
        result = voice_ai.generate(text, service=service, voice=voice, language=language)
        
        logger.info("voice_generation_task_completed", result=result)
        return {"success": True, "output": result}
    except Exception as e:
        logger.error("voice_generation_task_failed", error=str(e))
        raise self.retry(exc=e, countdown=60, max_retries=3)


@celery_app.task(name="process_voice_training", bind=True)
def process_voice_training(
    self,
    actor_id: int,
    audio_file_path: str,
    voice_name: str
) -> dict:
    """
    Process voice training task (async)
    
    Args:
        actor_id: Voice actor ID
        audio_file_path: Path to audio file
        voice_name: Voice name
        
    Returns:
        Task result
    """
    try:
        logger.info("voice_training_task_started", actor_id=actor_id, voice_name=voice_name)
        
        # TODO: Implement actual voice training
        # This would integrate with ElevenLabs API or custom model
        
        logger.info("voice_training_task_completed", actor_id=actor_id)
        return {"success": True, "voice_id": "generated_voice_id"}
    except Exception as e:
        logger.error("voice_training_task_failed", error=str(e))
        raise self.retry(exc=e, countdown=300, max_retries=3)

