import uuid
from typing import Optional, List
from sqlmodel import select, Session
from app.modules.dominio_1.usuario.models import Usuario, Rol

class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    # ¡El cambio clave! Ahora espera un UUID para buscar
    def get_by_id(self, id: uuid.UUID) -> Optional[Usuario]:
        return self.session.get(Usuario, id)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        # Trae al usuario SOLO si no está baneado (deleted_at es nulo)
        statement = select(Usuario).where(Usuario.email == email).where(Usuario.deleted_at.is_(None))
        return self.session.exec(statement).first()

    def get_all_active(self) -> List[Usuario]:
        # Ideal para el Admin: ver la lista limpia
        statement = select(Usuario).where(Usuario.deleted_at.is_(None))
        return self.session.exec(statement).all()

    def add(self, usuario: Usuario):
        self.session.add(usuario)


class RolRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_codigo(self, codigo: str) -> Optional[Rol]:
        return self.session.get(Rol, codigo)