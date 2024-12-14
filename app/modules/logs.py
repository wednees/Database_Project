import bcrypt
import psycopg2
import streamlit as st

from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from modules.connection import get_connection

def check_logs():
 # Просмотр инвентаризации
    st.subheader("Логи изменений")

    if st.button("Просмотреть логи"):
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""SELECT employee_id as ID_измененной_строки, 
                        action as Изменение,
                        timestamp as Время_изменения
                        FROM Logs""")
            inventory = cur.fetchall()
            st.table(inventory)