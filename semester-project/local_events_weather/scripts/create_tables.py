from app.db.postgres import Base, engine
from app.models import models  

Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully in Postgres.")
