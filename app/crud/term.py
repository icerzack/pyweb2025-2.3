from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.term import Term
from app.schemas.term import TermCreate, TermUpdate


def list_terms(db: Session) -> Sequence[Term]:
    return db.execute(select(Term).order_by(Term.keyword.asc())).scalars().all()


def get_term_by_keyword(db: Session, keyword: str) -> Term | None:
    return db.execute(select(Term).where(Term.keyword == keyword)).scalars().first()


def create_term(db: Session, data: TermCreate) -> Term:
    term = Term(keyword=data.keyword, description=data.description)
    db.add(term)
    db.commit()
    db.refresh(term)
    return term


def update_term(db: Session, keyword: str, data: TermUpdate) -> Term | None:
    term = get_term_by_keyword(db, keyword)
    if term is None:
        return None
    if data.description is not None:
        term.description = data.description
    db.add(term)
    db.commit()
    db.refresh(term)
    return term


def delete_term(db: Session, keyword: str) -> bool:
    term = get_term_by_keyword(db, keyword)
    if term is None:
        return False
    db.delete(term)
    db.commit()
    return True


