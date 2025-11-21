# services/card_service.py
from ..utils import database

class CardService:
    def create(self, banco, responsavel, apelido, ultimos_digitos):
        banco = banco or ""
        responsavel = responsavel or ""
        apelido = apelido or ""
        ultimos_digitos = ultimos_digitos or ""
        database.create_cartao(banco, responsavel, apelido, ultimos_digitos)

        # retorna lista completa; o caller pode filtrar se quiser
        cards = database.read_cartoes()
        # tenta retornar o último inserido por apelido (se único), senão None
        for c in cards:
            if c.apelido == apelido:
                return c
        return None

    def list(self):
        return database.read_cartoes()

    def get(self, id):
        cards = database.read_cartoes()
        for c in cards:
            if c.id == id:
                return c
        return None

    def update(self, id, banco, responsavel, apelido, ultimos_digitos):
        database.update_cartao(id, banco, responsavel, apelido, ultimos_digitos)

    def delete(self, id):
        database.delete_cartao(id)
