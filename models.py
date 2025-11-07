from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL
DATABASE_URL = "postgresql://pocuser:password@localhost:5432/pocdb"

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Route Model
class DynamicRoute(Base):
    __tablename__ = "dynamic_routes"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, nullable=False)
    message = Column(String, nullable=True)
    method = Column(String, nullable=False, default="GET")
    code = Column(Text, nullable=True)