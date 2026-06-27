from sqlalchemy import MetaData

metadata = MetaData()

# Import all models over here so they register on metadata
# Add new model files here as you create them
from app.models import jobs
from app.models import users
