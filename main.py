from gettext import find
from http.client import responses
from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
# We will use this to define our schema for our data .
from pydantic import BaseModel

# Defining Schema here .....


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: int = randrange(0, 10000000)


# Creating a instance of fastApi :
app = FastAPI()

my_posts = [{"title": "title of our first post ", "content": "This is content for our first post.", "id": 1}, {
    "title": "title 2", "content": "Content for second post.", "id": 2}]


def find_post(id):
    for post in my_posts:
        if(post['id'] == id):
            return post
    return False
# Get all posts.


@app.get("/posts")
def getAllPosts(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"data": my_posts}


# Get a particular post by its id :


@app.get("/posts/{id}")
def getAPost(id: int, response: Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": "Post not found ...."}
    else:
        response.status_code = status.HTTP_200_OK
        my_posts.remove(post)
        return {"data": post}

# # Post method .
# @app.post("/posts")
# # To extract the data form your params.
# def createPost(post: Post):
#     print(post.dict())  # To convert a pydantic model into a dictionary ...
#     return{"data": f"{post.dict()}"}

# Post method in array ....


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# Delete method in array .....

@app.delete("/posts/{id}")
def deletePost(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found , check if this {id} exists!")
    else:
        my_posts.remove(post)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post method in array ....

@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    print(post)
    return {'message': "updated post"}
