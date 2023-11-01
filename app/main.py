"""Imports needed for the web server"""
import os
from random import randrange
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
# from fastapi.params import Body


app = FastAPI()


class Post(BaseModel):
    """the schema for send_data"""
    title: str
    content: str
    published: bool = True


try:
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    db_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(host=db_url, database="fastapi-course",
                            user="postgres", password=secret_key, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesfully established")
except Exception as error:
    print(error)


my_posts = [
    {
        "title": "title of post one",
        "content": "contennt of post 1",
        "id": 1,
    },
    {
        "title": "favorite food",
        "content": "I like pizza",
        "id": 2
    }
]


@app.get("/")
async def root():
    """Main root of the application"""
    return {"message": "Welcome to my api!!!!"}


@app.get("/posts")
def get_post():
    """Route to retrive posts data"""
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def send_data(post: Post):
    """sends data to the server"""
    post_dict = post.model_dump()
    post_dict["id"] = randrange(10000000000000)
    print(post.model_dump())
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{post_id}")
def get_post_id(post_id: int):
    """Returns a post with the coresponding id"""
    for item in my_posts:
        if item["id"] == post_id:
            return {"data": item}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item not found")


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """deletse a post in the database"""
    for index, item in enumerate(my_posts):
        if item["id"] == post_id:
            my_posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item not found")


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    """Update the item"""
    print(post)
    for index, item in enumerate(my_posts):
        if item["id"] == post_id:
            updated_post = post.model_dump()
            updated_post["id"] = post_id
            my_posts[index] = updated_post
            return {"data": my_posts[index]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item not found")
