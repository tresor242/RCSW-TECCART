from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ---------------------------
# Modèle de données utilisateur
# ---------------------------
class User(BaseModel):
    id: int
    name: str
    email: str

# "Base de données" temporaire en mémoire
fake_users_db: List[User] = []

# ---------------------------
# GET : Liste des utilisateurs
# ---------------------------
@app.get("/users", response_model=List[User])
def get_users():
    return fake_users_db

# ---------------------------
# POST : Ajouter un utilisateur
# ---------------------------
@app.post("/users", response_model=User)
def create_user(user: User):
    # Vérifie si ID existe déjà
    for u in fake_users_db:
        if u.id == user.id:
            raise HTTPException(status_code=400, detail="ID déjà existant.")
    fake_users_db.append(user)
    return user

# ---------------------------
# GET : Obtenir un utilisateur par ID
# ---------------------------
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in fake_users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

# ---------------------------
# DELETE : Supprimer un utilisateur
# ---------------------------
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(fake_users_db):
        if user.id == user_id:
            del fake_users_db[i]
            return {"message": "Utilisateur supprimé."}
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
