from fastapi import FastAPI,Query,Path,Body,Depends
from pydantic import BaseModel,EmailStr
from typing import Optional
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Item(BaseModel):
    id: int 
    name:str
    description:Optional[str] = Query(None,max_length=50)
    price: float
    tax: Optional[float]=None

@app.get('/')
async def main():
    return {'message':'aho vatija aho'}
@app.post('/items')
async def create(item:Item):
    item_dict = item.dict()
    #print(item_dict)
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price with tax":price_with_tax})
    return item_dict
"""
@app.get('/items/{id}')
async def show(id:int = Path(...,title='the id of the iteam to get',gt=0,le=100)):
    results = {'id':id}
    return results
"""

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
@app.get('/items/{item_id}')
async def show(id:int= Depends(oauth2_scheme)):
    return {"item":Item}

#UUID check
@app.put('/citizen/{id}')
async def citizen_show_up(citizen_id:UUID,name:str):
    return{"id_number":citizen_id,'name':name}


class UserIn(BaseModel):
    username:str
    password:str
    email:EmailStr

class UserOut(BaseModel):
    username:str
    email:EmailStr

class UserInDB(BaseModel):
    username:str
    hashed_password:str
    email:EmailStr

def fake_password_hashed(raw_passord:str):
    return 'secret@'+raw_passord
def fake_save(user_in:UserIn):
    hash_pass = fake_password_hashed(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hash_pass)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save(user_in)
    return user_saved


