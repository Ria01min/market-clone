
#         raise InvalidCredentialsException #user가 아니거나
#     elif password != user['password']: #파이썬은 무조건 else if를 elif라고 쓴다.
#             raise InvalidCredentialsException #비밀번호가 불일치하다면 에러를 낸다.
    


from fastapi import FastAPI,UploadFile,Form,Response,Depends
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from fastapi.encoders import jsonable_encoder
import sqlite3
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

con = sqlite3.connect('db.db',check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
             CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                discription TEXT,
                place TEXT NOT NULL,
                insertAt INTEGER NOT NULL  
                );
            """)

app = FastAPI()

SECRET = "super-coding"
manager = LoginManager(SECRET, 'login')

@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''name="{data["name"]}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post('/login')
def login(id:Annotated[str,Form()], 
           password:Annotated[str,Form()]):
    user = query_user(id)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={
        'sub': {
        'id':user['id'],
        'name':user['name'],
        'email':user['email']
        }
    })
    
    return {'access_token':access_token}
    

@app.post('/signup')
def signup(id:Annotated[str,Form()], 
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES ('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit()
    return '200'

@app.post('/items')
async def create_item(image:UploadFile
                , title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                discription:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()], 
                user=Depends(manager)
                ):
    
    
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO 
                items(title, image, price, discription, place, insertAt)
                VALUES ('{title}', '{image_bytes.hex()}',{price},'{discription}', '{place}', {insertAt})
                """)
    con.commit()
    return '200'

@app.get('/items')
async def get_items(user=Depends(manager)):
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * FROM items;
                       """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))

@app.get("/images/{item_id}")
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes), media_type='/image/*')
    

 
app.mount("/", StaticFiles(directory='frontend', html=True), name='frontend')