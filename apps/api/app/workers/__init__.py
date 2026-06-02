"""Background workers for async resume analysis."""

import uuid

from arq.connections import RedisSettings

from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


async def analyze_resume_job(ctx: dict, job_id: str) -> None:
    """Process a resume analysis job. Implement extraction + LLM call."""
    setup_logging(get_settings().log_level)
    logger.info("analysis_job_started", job_id=job_id)
    _ = uuid.UUID(job_id)
    # TODO: load job, fetch file from storage, extract text, call LLM, persist result
    logger.info("analysis_job_finished", job_id=job_id)


class WorkerSettings:
    functions = [analyze_resume_job]
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
    max_jobs = 10
    job_timeout = 600
