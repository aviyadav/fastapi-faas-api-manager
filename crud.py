from sqlalchemy.orm import Session
from models import DynamicRoute
from schemas import RouteCreate

# Fetch all routes
def get_routes(db: Session):
    return db.query(DynamicRoute).all()

# Add a new route
def create_route(db: Session, route: RouteCreate):
    db_route = DynamicRoute(
        path=route.path,
        message=route.message,
        method=route.method
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route