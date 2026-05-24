from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/notes",tags=["notes"])

# dependency injection, it creates a session and it gives it to the route
# it closes once done.Yield stops it from closing until request is complete.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# root directory get request
@router.get("/",response_model=list[schemas.NoteResponse])
def read_notes(db: Session = Depends(get_db)):
    return crud.get_notes(db)



@router.get("/{note_id}",response_model=schemas.NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db,note_id)
    if note is None:
        raise HTTPException(status_code=404,detail="Note not found")
    return note


@router.post("/",response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db,note)


@router.put("/{note_id}",response_model=schemas.NoteResponse)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    updated = crud.update_note(db,note_id,note)
    if updated is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@router.delete("/{note_id}",response_model=schemas.NoteResponse)
def delete_note(note_id: int,db: Session = Depends(get_db)):
    deleted = crud.delete_note(db,note_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return deleted
