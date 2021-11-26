from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
    
app = FastAPI()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Aqui para baixo Usuario

#cadastrar um usuario
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = crud.create_user(db=db, user=user)
    
    return user


#entrega uma lista de usuarios
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users



@app.get("/users/{user_id}", response_model=schemas.User)
def get_user_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)


#Aqui para baixo Measure

#cadastrar um usuario
@app.post("/users/{user_id}/measures/", response_model=schemas.Measure)
def create_measure(user_id: int, measure: schemas.MeasureCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        return crud.create_user_measure(db, measure, user_id)

    

#entrega uma lista de usuarios
@app.get("/measures/", response_model=List[schemas.Measure])
def read_measures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_measures(db, skip=skip, limit=limit)
    return users
