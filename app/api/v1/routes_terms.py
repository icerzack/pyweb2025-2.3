from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.term import TermOut, TermCreate, TermUpdate
from app.crud.term import list_terms, get_term_by_keyword, create_term, update_term, delete_term


router = APIRouter()


@router.get("/terms", response_model=list[TermOut])
def api_list_terms(db: Session = Depends(get_db_session)):
    return list_terms(db)


@router.get("/terms/{keyword}", response_model=TermOut)
def api_get_term(keyword: str, db: Session = Depends(get_db_session)):
    term = get_term_by_keyword(db, keyword)
    if term is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Term not found")
    return term


@router.post("/terms", response_model=TermOut, status_code=status.HTTP_201_CREATED)
def api_create_term(payload: TermCreate, db: Session = Depends(get_db_session)):
    existing = get_term_by_keyword(db, payload.keyword)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Term with this keyword already exists")
    return create_term(db, payload)


@router.put("/terms/{keyword}", response_model=TermOut)
def api_update_term(keyword: str, payload: TermUpdate, db: Session = Depends(get_db_session)):
    term = update_term(db, keyword, payload)
    if term is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Term not found")
    return term


@router.delete("/terms/{keyword}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_term(keyword: str, db: Session = Depends(get_db_session)):
    deleted = delete_term(db, keyword)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Term not found")
    return None


