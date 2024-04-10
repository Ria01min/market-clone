from fastapi import FastAPI, UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
	            id INTEGER PRIMARY KEY,
	            title TEXT NOT NULL,
	            image BLOB,
	            price INTEGER NOT NULL,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGER NOT NULL
            );
            """)

app = FastAPI()

#자바스크립트에서 보내는 데이터
@app.post('/items')
async def create_item(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()],
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                
                ):
    
    image_bytes = await image.read() #이미지 크기가 커서 먼저 읽을 시간을 줘야함
    cur.execute(f"""
                INSERT INTO items(title,image,price,description,place,insertAt)
                VALUES ('{title}', '{image_bytes.hex()}',{price},'{description}','{place}',{insertAt}) 
                """) #price는 int이므로 문자열을 나타내는 ''표시 제외 , 이미지는 hex 16진법
    con.commit()
    
    return '200'

@app.get ('/items')
async def get_items():
    con.row_factory = sqlite3.Row #컬럼명도 같이 가져오는 문법
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * from items;
                       """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows)) #rows = [['id',1], ['title':'가위팝니다'], ...]  배열 형식을 돌면서 dictionary(객체)형태로 만들어줌


@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0]
    
    return Response(content=bytes.fromhex(image_bytes), media_type='image/*')

#회원가입
@app.post('/signup') #사용자가 POST요청을 보내면 아래의 함수가 실행됨
def signup(id:Annotated[str,Form()], 
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]): #Form()은 HTML에서 해당 필드의 값을 추출함
    #1. 받은 정보 DB에 저장 로직  2. DBever에서 테이블 생성
    cur.execute(f"""
                INSERT INTO users (id, name, email, password)
                VALUES ('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit()
    return '200' #단순히 문자열 '200'을 반환. 클라이언트에게 성공적인 요청을 알림. 여기서 HTTP응답코드 200은 "OK"를 나타냄.

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")