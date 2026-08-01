from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)
print("Created tables:", list(Base.metadata.tables.keys()))
