# services/category_service.py
from sqlite3 import IntegrityError
from ..utils import database

class CategoryService:
    def create(self, nome):
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("Nome obrigatório")

        try:
            database.create_categoria(nome)
        except IntegrityError as e:
            # repassa como ValueError para as telas tratarem
            raise ValueError("Categoria já existe") from e

        # retorna a categoria recém-criada (por busca pelo nome)
        cats = database.read_categorias()
        for c in cats:
            if c.nome == nome:
                return c
        return None

    def list(self):
        return database.read_categorias()

    def update(self, id, nome):
        database.update_categoria(id, nome)

    def delete(self, id):
        database.delete_categoria(id)
