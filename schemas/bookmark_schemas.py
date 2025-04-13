from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

from model.bookmark_model import Bookmark

class BookmarkSchema(BaseModel):
    title:str = Field(..., examples='MyRepository | GitHub')
    url:HttpUrl = Field(..., examples='https://github.com/joaovitorfrv')
    icon_url:Optional[HttpUrl] = Field(None,examples='https://github.com/favicon.ico')

class BookmarkViewSchema(BaseModel):
    id:int = 1
    title:str = 'MyRepository | GitHub'
    url:str = 'https://github.com/joaovitorfrv'
    icon_url:str = 'https://github.com/favicon.ico'

class BookmarkPostSchema(BaseModel):
    title: str = Field(None, min_length=1, max_length=200,description='Título da bookmark')
    url:str = Field(None, max_length=500, description='URL da Bookmark.')

class BookmarkPutSchema(BaseModel):
    title: str = Field(None, min_length=1, max_length=200,description='Título da bookmark')
    url:str = Field(None, max_length=500, description='URL da Bookmark.')

class BookmarkSearchForIdSchema(BaseModel):
    id:str

class BookmarksListSchema(BaseModel):
    bookmarks:List[BookmarkViewSchema] ## Não pode ser return por ser class. Deve ser representada pela variável da lista.

class BookmarkDelSchema(BaseModel):
    id:int
    message:str

def show_bookmarks(bookmarks: List[Bookmark]):
    result = []
    for bookmark in bookmarks:
        result.append({
            'id':bookmark.id,
            'title':bookmark.title,
            'url':bookmark.url,
            'icon_url':bookmark.icon_url,
            'created-at':bookmark.created_at
        })
    return {'task':result}

def show_bookmark(bookmark:Bookmark):
    return ({
        'id':bookmark.id,
        'title':bookmark.title,
        'url':bookmark.url,
        'icon_url':bookmark.icon_url,
        'created-at':bookmark.created_at,
        'updated_at':bookmark.updated_at
    })

