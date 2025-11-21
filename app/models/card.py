import sqlite3
from config import DB_NAME
from ..utils.paths import db_path

class Card:
    def __init__(self, banco, responsavel, apelido, ultimos_digitos, id=None):
        self.id = id
        self.banco = banco
        self.responsavel = responsavel
        self.apelido = apelido
        self.ultimos_digitos = ultimos_digitos

    @staticmethod
    def get_all():
        conn = sqlite3.connect(db_path(DB_NAME))
        c = conn.cursor()
        c.execute("SELECT id, banco, responsavel, apelido, ultimos_digitos FROM cartoes ORDER BY apelido ASC")
        rows = c.fetchall()
        conn.close()
        return [Card(row[1], row[2], row[3], row[4], id=row[0]) for row in rows]

    def save(self):
        conn = sqlite3.connect(db_path(DB_NAME))
        c = conn.cursor()

        if self.id:
            c.execute("""
                UPDATE cartoes SET banco=?, responsavel=?, apelido=?, ultimos_digitos=? WHERE id=?
            """, (self.banco, self.responsavel, self.apelido, self.ultimos_digitos, self.id))
        else:
            c.execute("""
                INSERT INTO cartoes (banco, responsavel, apelido, ultimos_digitos)
                VALUES (?, ?, ?, ?)
            """, (self.banco, self.responsavel, self.apelido, self.ultimos_digitos))

        conn.commit()
        conn.close()
