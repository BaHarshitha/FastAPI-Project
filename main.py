from fastapi import Depends,FastAPI,HTTPException
from sqlalchemy.orm import Session
import uvicorn
import model,schema,crud
from database import engine,SessionLocal

model.Base.metadata.create_all(bind=engine)
print("database created with tables")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user/",response_model=schema.User)
def create_user(user:schema.UserCreate,db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="Email already registered!")
    return crud.create_user(db=db,user=user)

@app.get("/users",response_model=list[schema.User])
def read_users(skip:int=0,limit:int=0,db:Session= Depends(get_db)):
    users =  crud.get_users(db,skip=skip,limit=limit)
    return users

@app.get("/user/{user_id}",response_model=schema.User)
def read_user(user_id:int,db:Session = Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return db_user

@app.post("/item/",response_model=schema.Item)
def create_item_for_user(user_id:int,item:schema.ItemCreate,db:schema=Depends(get_db)):
    return crud.create_user_item(db=db,item=item,user_id=user_id)

@app.get("/items/",response_model=list[schema.Item])
def read_items(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    items=crud.get_items(db,skip,limit)
    return items

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=3000)