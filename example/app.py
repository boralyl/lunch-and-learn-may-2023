from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import select

from .auth import require_api_key
from .db import create_db_and_tables, Session, get_session
from .models.hero import Hero, HeroCreate, HeroRead


app = FastAPI(
    title="Heroes API",
    description="An API for Heroes.",
    version="1.0.1"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/", response_model=HeroRead)
def create_hero(
    *,
    session: Session = Depends(get_session),
    _: None = Depends(require_api_key),
    hero: HeroCreate
):
    """Create a new hero."""
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroRead])
def fetch_heroes(
    *,
    query: str | None = None,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    """Retrieve all heroes."""
    statement = select(Hero)
    if query is not None:
        statement = statement.where(Hero.name == query)
    heroes = session.exec(statement.offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroRead)
def fetch_hero(*, session: Session = Depends(get_session), hero_id: int):
    """Retrieve a hero by ID."""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
