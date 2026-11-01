from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
    version="1.0.0"
)

class Post(BaseModel):
    title: str
    content: Optional[str] = Field(
        default=None, 
        min_length=2,
        description="The content of the post",
        example="This is the content of the post."
    )

class PostCreate(BaseModel):
    id: int
    title: str
    content: Optional[str] = Field(
        default=None, 
        min_length=2,
        description="The content of the post",
        example="This is the content of the post."
    )

BLOG_POST = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."},
    {"id": 3, "title": "Third Post", "content": "This is the third post."}
]

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}

@app.get("/posts")
def read_posts(query: str | None = Query(default=None, description="Search query")) -> list[Post]:
    if query is None:
        return [Post(**post) for post in BLOG_POST]
    else:
        return [Post(**post) for post in BLOG_POST if query.lower() in post["title"].lower() or query.lower() in post["content"].lower()]
    
@app.get("/posts/{post_id}")
def read_post(post_id: int) -> Post:
    post = next((p for p in BLOG_POST if p["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(**post)


@app.post("/posts")
def create_post(post: PostCreate) -> Post:
    if any(p["id"] == post.id for p in BLOG_POST):
        raise HTTPException(status_code=400, detail="Post with this ID already exists")
    if not post.title or not post.content:
        raise HTTPException(status_code=400, detail="Title and content cannot be empty")
    BLOG_POST.append(post.dict())
    return post

@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: Post) -> Post:
    post = next((p for p in BLOG_POST if p["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if not updated_post.title or not updated_post.content:
        raise HTTPException(status_code=400, detail="Title and content cannot be empty")
    post.update(updated_post.dict())
    return Post(**post)

@app.delete("/posts/{post_id}")
def delete_post(post_id: int) -> dict[str, str]:
    post = next((p for p in BLOG_POST if p["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    BLOG_POST.remove(post)
    return {"message": "Post deleted successfully"}