from fastapi import FastAPI

app = FastAPI()

items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
]


# Seeing all items
@app.get("/items")
def get_all_items():
    return items


# seeing single item
@app.get("/items/{item_id}")
def get_single_items(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"Item not found"}


# Adding one item
@app.post("/post/item_name")
def create_iteam(item: dict):
    new_id = len(items) + 1
    item["id"] = new_id
    items.append(item)
    return {"Item added successfully"}


# Modifying the item
@app.put("/put/{item_id}")
def update_id(item_id: int, new_data: dict):
    for item in items:
        if item["id"] == item_id:
            item.update(new_data)
            return {"Updated"}
    return {"Item not found"}


# Delete the item
@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return {"Removed"}
    return "Item not founded"
