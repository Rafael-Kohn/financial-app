# services/excel_service.py
import pandas as pd
from ..utils.database import connect
from config import EXPORT_FILE

def export_to_excel(filename=None):
    if filename is None:
        filename = EXPORT_FILE
    conn = connect()
    try:
        df = pd.read_sql_query("SELECT * FROM gastos", conn)
        df.to_excel(filename, index=False)
    finally:
        conn.close()
    return filename
