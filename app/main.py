from fastapi import FastAPI
from .database import Base, engine, get_db
from .routes import auth_routes, users, transactions, portfolio
from .seed_prices import seed_prices

def create_app() -> FastAPI:
    app = FastAPI(title="WealthWise Portfolio Tracker", version="1.0.0",root_path="/")

   
    Base.metadata.create_all(bind=engine)

    @app.on_event("startup")
    def _seed():
        from sqlalchemy.orm import Session
        db: Session = next(get_db())
        seed_prices(db)

    # routes
    app.include_router(auth_routes.router)
    app.include_router(users.router)
    app.include_router(transactions.router)
    app.include_router(portfolio.router)


    @app.get("/")
    def home():
        return {"message": "WealthWise API is running "}

    return app


app = create_app()
