from fastapi import  APIRouter, FastAPI, Depends, HTTPException, status, Response

from  database import engine,SessionLocal, Base
from schema import UserSchema
from sqlalchemy.orm import Session
from models import User

#cria a tabela
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/user")   

def get_db():
    try:
        db = SessionLocal()
        #TODO 
        yield db
    finally:
        db.close()




@router.post("/add")
async def add_user(request:UserSchema, db: Session = Depends(get_db)):
    user_on_db = User(id=request.id, username=request.username, password=request.password)
    db.add(user_on_db)
    db.commit()
    db.refresh(user_on_db)
    return user_on_db

@router.get("/{user_name}", description="Listar o usuário pelo nome")
def get_user(user_name,db: Session = Depends(get_db)):
    user_on_db= db.query(User).filter(User.item == user_name).first()
    return user_on_db

@router.get("/user/listar")
async def get_tarefas(db: Session = Depends(get_db)):
    user= db.query(User).all()
    return user


@router.delete("/{id}", description="Deletar o usuário pelo id")
def delete_user(id: int, db: Session = Depends(get_db)):
    user_on_db = db.query(User).filter(User.id == id).first()
    if user_on_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum usuário encontrado com este id')
    db.delete(user_on_db)
    db.commit()
    return f"Banco with id {id} deletado.", Response(status_code=status.HTTP_200_OK)
