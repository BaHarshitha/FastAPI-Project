from sqlalchemy.orm import Session
import model, schema

def get_user(db:Session,user_id:int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_user_by_email(db:Session,email:str):
    return db.query(model.User).filter(model.User.email == email).first()

def get_users(db:Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

def create_user(db:Session, user: schema.UserCreate):
    fake_hashed_password = user.password + "notrealhasedpassword"
    db_user = model.User(email=user.email,hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db:Session,skip: int = 0, limit: int = 100):
    return db.query(model.Item).offset(skip).limit(limit).all()

def create_user_item(db:Session,item:schema.ItemCreate,user_id:int):
    db_item = model.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item