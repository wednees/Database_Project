import os
import bcrypt
import psycopg2
import streamlit as st

from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from modules.connection import get_connection

import json
from modules.redis_client import redis_client

def view_employees():
    st.subheader("Сотрудники")

    cache_key = "cache:employees"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        categories = json.loads(cached_data)
        st.table(categories)
        if st.button("Обновить данные"):
            redis_client.delete(cache_key)
            st.rerun()
    else:
        if st.button("Просмотреть всех сотрудников"):
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT username as Имя_пользователя, name as Роль FROM Employees LEFT JOIN Roles ON role_id = Roles.id")
                employees = cur.fetchall()

                redis_client.setex(cache_key, 300, json.dumps(employees))
                st.table(employees)

def add_employee():
    st.subheader("Добавление нового аккаунта сотрудника")

    with st.form("add_employee_form"):
        st.write("Добавить нового сотрудника")
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type="password")
        role_id = st.selectbox("Роль", [1, 2, 3], format_func=lambda x: {1: "Администратор", 2: "Менеджер", 3: "Кассир"}[x])
        submit = st.form_submit_button("Добавить")
        
        if submit:

            if not username.strip():
                st.error("Имя пользователя обязательно для заполнения.")
                return
            if not password.strip():
                st.error("Пароль обязателен для заполнения.")
                return
            
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            try:
                conn = get_connection()
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO Employees (username, password_hash, role_id) VALUES (%s, %s, %s)",
                        (username, password_hash, role_id)
                    )
                    conn.commit()
                    st.success("Сотрудник добавлен!")

                    redis_client.delete("cache:employees")    

            except psycopg2.IntegrityError:
                st.error("Ошибка: Некорректный ввод данных")
            except psycopg2.DatabaseError as e:
                st.error(f"Ошибка базы данных: {e}")
            except Exception as e:
                st.error(f"Неизвестная ошибка: {e}")


def delete_employee_func(username):
    """Удаляет товар из базы данных по его ID."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Проверка, существует ли товар с данным ID
            cur.execute("SELECT * FROM Employees WHERE username = %s", (username,))
            product = cur.fetchone()
            if not product:
                st.error("Аккаунт с указанным именем не найден.")
                return

            # Удаление товара
            cur.execute("DELETE FROM Employees WHERE username = %s", (username,))
            conn.commit()
            st.success(f"Аккуант {username} успешно удален.")
            
            redis_client.delete("cache:employees")    

    except psycopg2.Error as e:
        st.error(f"Ошибка при удалении аккаунта: {e}")

def delete_employee():
    """Интерфейс Streamlit для удаления товара."""
    st.subheader("Удаление пользователя")

    # Поле ввода для ID товара
    username = st.text_input("Введите имя пользователя для удаления")

    if st.button("Удалить пользователя"):
        delete_employee_func(username)