from datetime import datetime

fake_job_id = "123e4567-e89b-12d3-a456-426614174000" 

fake_successful_job_response = {
    "job_id": fake_job_id,
    "url": "https://example.com",
    "status": "SUCCESS",
    "result": None,
    "error_message": None,
    "created_at": datetime.now(),
    "updated_at": None,
    "completed_at": None
}
