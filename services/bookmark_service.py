from model import Session, Bookmark
from datetime import datetime, timezone
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from typing import Optional

def get_favicon_url(url: str) -> Optional[str]:
    """
    Obtém o URL do favicon de um site
    """
    try:
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        # Tenta obter do HTML
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procura por favicon no HTML
        icon_link = soup.find("link", rel=lambda x: x and x.lower() in ["icon", "shortcut icon"])
        if icon_link and icon_link.get("href"):
            return urljoin(base_url, icon_link["href"])
        
        # Tenta o padrão /favicon.ico
        favicon_url = f"{base_url}/favicon.ico"
        response = requests.head(favicon_url, headers=headers, timeout=3)
        if response.status_code == 200:
            return favicon_url
            
    except Exception:
        pass
    
    # Fallback para favicon genérico se não encontrar
    return f"https://www.google.com/s2/favicons?domain={urlparse(url).netloc}"

def add_bookmark_service(form_data: dict):
    """
    Adiciona um novo bookmark com favicon automático
    """
    session = Session()
    try:
        # Obtém favicon
        icon_url = get_favicon_url(form_data['url'])
        
        bookmark = Bookmark(
            title=form_data['title'],
            url=form_data['url'],
            icon_url=icon_url
        )
        
        session.add(bookmark)
        session.commit()
        
        return bookmark.to_dict(), 201
    except Exception as e:
        session.rollback()
        return {'message': f'Erro ao adicionar bookmark: {str(e)}'}, 400


def get_bookmarks_service():
    """
    Retorna todos os bookmarks
    """
    session = Session()
    try:
        bookmarks = session.query(Bookmark).order_by(Bookmark.created_at.desc()).all()
        return {'bookmarks': [b.to_dict() for b in bookmarks]}, 200
    except Exception as e:
        return {'message': f'Erro ao obter bookmarks: {str(e)}'}, 400


def get_bookmark_service(bookmark_id: int):
    """
    Obtém um bookmark específico por ID
    """
    session = Session()
    try:
        bookmark = session.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
        if not bookmark:
            return {'message': 'Bookmark não encontrado'}, 404
        return bookmark.to_dict(), 200
    except Exception as e:
        return {'message': f'Erro ao obter bookmark: {str(e)}'}, 400


def update_bookmark_service(bookmark_id: int, form_data: dict):
    """
    Atualiza um bookmark existente
    """
    session = Session()
    try:
        bookmark = session.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
        if not bookmark:
            return {'message': 'Bookmark não encontrado'}, 404
        
        # Atualiza campos se fornecidos
        if 'title' in form_data:
            bookmark.title = form_data['title']
        if 'url' in form_data and form_data['url'].strip():
            print(f'URL=|{form_data['url']}|')
            bookmark.url = form_data['url']
            # Atualiza favicon se URL mudou
            bookmark.icon_url = get_favicon_url(form_data['url'])
        
        bookmark.updated_at = datetime.now(timezone.utc)
        session.commit()
        
        return bookmark.to_dict(), 200
    except Exception as e:
        session.rollback()
        return {'message': f'Erro ao atualizar bookmark: {str(e)}'}, 400


def delete_bookmark_service(bookmark_id: int):
    """
    Remove um bookmark
    """
    session = Session()
    try:
        bookmark = session.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
        if not bookmark:
            return {'message': 'Bookmark não encontrado'}, 404
        
        session.delete(bookmark)
        session.commit()
        return {'message': 'Bookmark removido com sucesso', 'id': bookmark_id}, 200
    except Exception as e:
        session.rollback()
        return {'message': f'Erro ao remover bookmark: {str(e)}'}, 400
