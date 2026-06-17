from asyncpg import Record

from app.models.schemas import JobResponse, AuditResponse


def generate_report(job: Record) -> JobResponse:
    return JobResponse(
        job_id=job["job_id"],
        url=job["url"],
        status=job["status"],
        result=AuditResponse(**job["result"]) if job["result"] else None,
        error_message=job["error_message"] if job["error_message"] else None,
        created_at=job["created_at"],
        updated_at=job["updated_at"] if job["updated_at"] else None,
        completed_at=job["completed_at"] if job["completed_at"] else None,
    )
