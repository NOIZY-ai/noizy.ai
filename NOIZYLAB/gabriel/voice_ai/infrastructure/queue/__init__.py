"""
📬 TASK QUEUE - 100% PERFECT
Perfect task queue implementation
GORUNFREE Protocol
"""

from .celery_tasks import celery_app, generate_voice_task, process_voice_training

__all__ = [
    "celery_app",
    "generate_voice_task",
    "process_voice_training",
]

