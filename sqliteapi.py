import sqlite3
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

connection = sqlite3.connect(database="practice.db", check_same_thread=False)
cursor = connection.cursor()
'''
# Creating Database
cursor.execute(
    """create table if not exists items
               (id integer primary key autoincrement, 
               name text not null, 
               rating integer )
               """
)
connection.commit()

# Inserting Data
cursor.execute(
    "insert into items(name, rating) values(?,?)",
    (
        "Item1",
        5,
    ),
)
connection.commit()
cursor.execute(
    "insert into items(name, rating) values(?,?)",
    (
        "Item2",
        4,
    ),
)
connection.commit()'''


@app.get("/")
def root():
    return {"message": "Welcome to the Sqlite API"}


# get all items
@app.get("/items")
def get_items():
    try:
        cursor.execute("select * from items")
        rows = cursor.fetchall()
        return [{"id": item[0], "name": item[1], "rating": item[2]} for item in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get single item
@app.get("/items/{name}")
def get_item(name: str):
    try:
        cursor.execute("select * from items where name=?", (name,))
        row = cursor.fetchone()
        return {"id": row[0], "name": row[1], "rating": row[2]}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# add new item
@app.post("/items/create")
async def add_item(req: Request) -> dict:
    data = await req.json()
    name = data.get("name")
    rating = data.get("rating")
    try:
        cursor.execute(
            "insert into items(name, rating) values(?,?)",
            (
                name,
                rating,
            ),
        )
        connection.commit()
        return {"message": "Item added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# update item
@app.put("/items/update")
async def update_item(req: Request) -> dict:
    data = await req.json()
    item_id = data.get("id")
    name = data.get("name")
    rating = data.get("rating")
    try:
        cursor.execute(
            "update items set name=?, rating=? where id=?",
            (
                name,
                rating,
                item_id,
            ),
        )
        connection.commit()
        return {"message": "Item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# delete item
@app.delete("/items/delete/{item_id}")
def delete_item(item_id: int):
    try:
        cursor.execute("delete from items where id=?", (item_id,))
        connection.commit()
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
