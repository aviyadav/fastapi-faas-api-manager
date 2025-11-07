from typing import Callable, Dict
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, DynamicRoute, Base, engine
from schemas import RouteCreate, RouteResponse
from crud import get_routes, create_route
from fastapi.responses import JSONResponse
import logging


Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DynamicRoutes")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await load_routes()
    yield
    # Shutdown (if needed)

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_dynamic_route(message: str):
    async def endpoint():
        return JSONResponse(content={"message": message})
    
    return endpoint

def create_dynamic_route_from_code(code: str) -> Callable:
    local_scope: Dict[str, Callable] = {}

    try:
        exec(code, {}, local_scope)

        if "handler" not in local_scope:
            raise ValueError("The provided code must define a 'handler' function.")
        
        return local_scope["handler"]
    except Exception as e:
        raise ValueError(f"Error in provided code: {str(e)}")
    
# Add existing routes from the database
async def load_routes():
    db = SessionLocal()
    routes = get_routes(db)

    for route in routes:
        if route.code:
            handler_function = create_dynamic_route_from_code(route.code)
            app.add_api_route(
                route.path,
                handler_function,
                methods=[route.method],
            )
        else:
            app.add_api_route(
                route.path,
                create_dynamic_route(route.message),
                methods=[route.method],
            )

@app.post("/add-route/", response_model=RouteResponse)
async def add_route(route: RouteCreate, db: Session = Depends(get_db)):
    # check if route already exists
    existing_route = db.query(DynamicRoute).filter(DynamicRoute.path == route.path).first()
    if existing_route:
        raise HTTPException(status_code=400, detail="Route already exists")
    
    handler_function = create_dynamic_route_from_code(route.code)

    new_route = create_route(db, route)
    app.add_api_route(
        new_route.path,
        handler_function,
        methods=[new_route.method],
    )

    # Rebuild the OpenAPI schema
    app.openapi_schema = None
    app.openapi()
    return new_route
