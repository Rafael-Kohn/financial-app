import sqlite3
from config import DB_NAME
from .paths import db_path

FULL_DB_PATH = db_path(DB_NAME)


# ---------------------------------------------------------
# MODELOS (OBJETOS DAS TABELAS)
# ---------------------------------------------------------
class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome


class Cartao:
    def __init__(self, id, banco, responsavel, apelido, ultimos_digitos):
        self.id = id
        self.banco = banco
        self.responsavel = responsavel
        self.apelido = apelido
        self.ultimos_digitos = ultimos_digitos


class Gasto:
    def __init__(self, id, cartao_id, tipo, valor, parcelas,
                 data_recorrencia, frequencia, nome, categoria):
        self.id = id
        self.cartao_id = cartao_id
        self.tipo = tipo
        self.valor = valor
        self.parcelas = parcelas
        self.data_recorrencia = data_recorrencia
        self.frequencia = frequencia
        self.nome = nome
        self.categoria = categoria


# ---------------------------------------------------------
# BANCO
# ---------------------------------------------------------
def connect():
    conn = sqlite3.connect(FULL_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS cartoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banco TEXT,
            responsavel TEXT,
            apelido TEXT,
            ultimos_digitos TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cartao_id INTEGER,
            tipo TEXT,
            valor REAL,
            parcelas INTEGER,
            data_recorrencia TEXT,
            frequencia TEXT,
            nome TEXT,
            categoria TEXT,
            FOREIGN KEY(cartao_id) REFERENCES cartoes(id)
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# FUNÇÕES AUXILIARES PARA CONVERTER PARA OBJETOS
# ---------------------------------------------------------

def _to_categoria(row): return Categoria(row["id"], row["nome"])
def _to_cartao(row): return Cartao(row["id"], row["banco"], row["responsavel"], row["apelido"], row["ultimos_digitos"])
def _to_gasto(row): return Gasto(row["id"], row["cartao_id"], row["tipo"], row["valor"],
                                 row["parcelas"], row["data_recorrencia"], row["frequencia"],
                                 row["nome"], row["categoria"])


# ---------------------------------------------------------
# CRUD – CATEGORIAS
# ---------------------------------------------------------
def create_categoria(nome):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()


def read_categorias():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categorias ORDER BY nome")
    rows = cur.fetchall()
    conn.close()
    return [_to_categoria(r) for r in rows]


def update_categoria(id, nome):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE categorias SET nome=? WHERE id=?", (nome, id))
    conn.commit()
    conn.close()


def delete_categoria(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM categorias WHERE id=?", (id,))
    conn.commit()
    conn.close()


# ---------------------------------------------------------
# CRUD – CARTÕES
# ---------------------------------------------------------
def create_cartao(banco, responsavel, apelido, ultimos_digitos):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cartoes (banco, responsavel, apelido, ultimos_digitos)
        VALUES (?, ?, ?, ?)
    """, (banco, responsavel, apelido, ultimos_digitos))
    conn.commit()
    conn.close()


def read_cartoes():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cartoes ORDER BY apelido")
    rows = cur.fetchall()
    conn.close()
    return [_to_cartao(r) for r in rows]


def update_cartao(id, banco, responsavel, apelido, ultimos_digitos):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE cartoes
        SET banco=?, responsavel=?, apelido=?, ultimos_digitos=?
        WHERE id=?
    """, (banco, responsavel, apelido, ultimos_digitos, id))
    conn.commit()
    conn.close()


def delete_cartao(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM cartoes WHERE id=?", (id,))
    conn.commit()
    conn.close()


# ---------------------------------------------------------
# CRUD – GASTOS
# ---------------------------------------------------------
def create_gasto(cartao_id, tipo, valor, parcelas,
                 data_recorrencia, frequencia, nome, categoria):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO gastos
        (cartao_id, tipo, valor, parcelas, data_recorrencia, frequencia, nome, categoria)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (cartao_id, tipo, valor, parcelas, data_recorrencia, frequencia, nome, categoria))
    conn.commit()
    conn.close()


def read_gastos():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM gastos ORDER BY data_recorrencia")
    rows = cur.fetchall()
    conn.close()
    return [_to_gasto(r) for r in rows]


def update_gasto(id, cartao_id, tipo, valor, parcelas,
                 data_recorrencia, frequencia, nome, categoria):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE gastos
        SET cartao_id=?, tipo=?, valor=?, parcelas=?, data_recorrencia=?, frequencia=?, nome=?, categoria=?
        WHERE id=?
    """, (cartao_id, tipo, valor, parcelas, data_recorrencia, frequencia, nome, categoria, id))
    conn.commit()
    conn.close()


def delete_gasto(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM gastos WHERE id=?", (id,))
    conn.commit()
    conn.close()
