from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import update
 
 
#Usuario
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
 
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
 
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
 
 
#Criar usuario
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
 
 
#ediçao_user
def edi_user(db: Session, user_id: int, new_value: schemas.UserEdit):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        if new_value.email != None:
            db.query(models.User).filter(models.User.id == user_id).\
                update({"email": new_value.email})
        if new_value.name != None:
            db.query(models.User).filter(models.User.id == user_id).\
                update({"name": new_value.name})
        if new_value.birth_date != None:
            db.query(models.User).filter(models.User.id == user_id).\
                update({"birth_date": new_value.birth_date})
 
    db.commit()
    db.refresh(db_user)
    return db_user
       
 
#deletear usuario
def remove_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
 
 
 
#Medidas
def get_measures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Measure).offset(skip).limit(limit).all()
 
 
#Usuario medidas
def get_user_measure(db: Session, user_id: int):
    return db.query(models.Measure).filter(models.Measure.user_id == user_id).all()
 
 
#Criar medidas
def create_user_measure(db: Session, measure: schemas.MeasureCreate, user_id: int):
    db_measure = models.Measure(**measure.dict(), owner_id=user_id)
    db.add(db_measure)
    db.commit()
    db.refresh(db_measure)
    return db_measure
 
