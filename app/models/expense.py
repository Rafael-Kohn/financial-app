import sqlite3
from config import DB_NAME
from ..utils.paths import db_path

class Expense:
    def __init__(self, cartao_id, tipo, valor, parcelas, data_recorrencia,
                 frequencia, nome, categoria, id=None):
        self.id = id
        self.cartao_id = cartao_id
        self.tipo = tipo
        self.valor = valor
        self.parcelas = parcelas
        self.data_recorrencia = data_recorrencia
        self.frequencia = frequencia
        self.nome = nome
        self.categoria = categoria

    @staticmethod
    def get_all():
        conn = sqlite3.connect(db_path(DB_NAME))
        c = conn.cursor()
        c.execute("""
            SELECT id, cartao_id, tipo, valor, parcelas, data_recorrencia,
                   frequencia, nome, categoria
            FROM gastos ORDER BY id DESC
        """)
        rows = c.fetchall()
        conn.close()
        return [Expense(*row[1:], id=row[0]) for row in rows]

    def delete(self):
        if not self.id:
            return
        conn = sqlite3.connect(db_path(DB_NAME))
        c = conn.cursor()
        c.execute("DELETE FROM gastos WHERE id=?", (self.id,))
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect(db_path(DB_NAME))
        c = conn.cursor()

        if self.id:
            c.execute("""
                UPDATE gastos
                SET cartao_id=?, tipo=?, valor=?, parcelas=?, data_recorrencia=?,
                    frequencia=?, nome=?, categoria=?
                WHERE id=?
            """, (
                self.cartao_id, self.tipo, self.valor, self.parcelas,
                self.data_recorrencia, self.frequencia, self.nome,
                self.categoria, self.id
            ))
        else:
            c.execute("""
                INSERT INTO gastos
                (cartao_id, tipo, valor, parcelas, data_recorrencia,
                 frequencia, nome, categoria)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.cartao_id, self.tipo, self.valor, self.parcelas,
                self.data_recorrencia, self.frequencia,
                self.nome, self.categoria
            ))
        conn.commit()
        conn.close()
