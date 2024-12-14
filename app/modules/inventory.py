import os
import bcrypt
import psycopg2
import streamlit as st

from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from modules.connection import get_connection



def check_stock():
 # Просмотр инвентаризации
    st.subheader("Остатки продуктов")

    if st.button("Просмотреть остатки"):
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""SELECT name as Название,
                        stock_level as Остаток, 
                        last_checked as Дата_последнего_обновлния
                        FROM Inventory LEFT JOIN Products ON Products.id = product_id""")
            inventory = cur.fetchall()
            st.table(inventory)


def update_stock():
    # Обновление запасов
    st.subheader("Принять поставку")

    with st.form("update_stock_form"):
        st.write("Обновить остаток товара")
        product_id = st.text_input("ID товара")
        stock_level = st.number_input("Количество", min_value=0)
        submit = st.form_submit_button("Обновить")
        
        if submit:

            if not product_id.strip().isdigit():
                st.error("ID товара должно быть числом.")
                return

            try:
                conn = get_connection()
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE Inventory SET stock_level = %s, last_checked = NOW() WHERE product_id = %s",
                        (stock_level, product_id)
                    )
                    conn.commit()
                    st.success("Запас обновлен!")
            except psycopg2.IntegrityError:
                st.error("Ошибка: ID товара не существует.")
            except psycopg2.DatabaseError as e:
                st.error(f"Ошибка базы данных: {e}")
            except Exception as e:
                st.error(f"Неизвестная ошибка: {e}")
