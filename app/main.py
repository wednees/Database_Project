import os
import bcrypt
import psycopg2
import streamlit as st

from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from modules.connection import get_connection
from modules.logs import check_logs
from modules.inventory import check_stock, update_stock
from modules.backups import backup_controller
from modules.employees import view_employees, add_employee, delete_employee
from modules.products import view_shorter_products, view_full_products_info, add_product, delete_product, view_suppliers, view_categories


def authenticate_user(username, password):
    """Проверяет учетные данные пользователя"""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, password_hash, role_id FROM Employees WHERE username = %s", (username,))
        user = cur.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return user
    return None

def main():
    st.title("Система учета товаров для винного магазина")

    # Форма авторизации
    st.sidebar.title("Авторизация")
    username = st.sidebar.text_input("Имя пользователя")
    password = st.sidebar.text_input("Пароль", type="password")
    if st.sidebar.button("Войти"):
        user = authenticate_user(username, password)
        if user:
            st.sidebar.success("Успешный вход!")
            st.session_state['user_id'] = user['id']
            st.session_state['role_id'] = user['role_id']
        else:
            st.sidebar.error("Неверные имя пользователя или пароль!")

    # Проверка авторизации
    if 'user_id' in st.session_state:
        role_id = st.session_state['role_id']

        # Роли
        if role_id == 1:  # Администратор
            admin_menu()
        elif role_id == 2:  # Менеджер
            manager_menu()
        elif role_id == 3:  # Кассир
            cashier_menu()
    else:
        st.info("Пожалуйста, авторизуйтесь, чтобы продолжить.")

def admin_menu():
    st.sidebar.title("Меню администратора")
    page = st.sidebar.selectbox("Выберите действие", ["Удалить сотрудника", "Добавить сотрудника", "Управление резервными копиями", "Просмотреть логи"])

    if page == "Удалить сотрудника":
        view_employees()
        delete_employee()
    elif page == "Добавить сотрудника":
        add_employee()
    elif page == "Управление резервными копиями":
        backup_controller()
    elif page == "Просмотреть логи":
        check_logs()


def manager_menu():
    st.sidebar.title("Меню мэнеджера")
    page = st.sidebar.selectbox("Выберите действие", ["Добавить продукт", "Удалить товар", "Просмотр остатков на складе"])

    if page == "Удалить товар":
        view_shorter_products()
        delete_product()
    elif page == "Добавить продукт":
        view_categories()
        view_suppliers()
        add_product()
    elif page == "Просмотр остатков на складе":
        check_stock()

def cashier_menu():
    st.sidebar.title("Меню работника")
    page = st.sidebar.selectbox("Выберите действие", ["Просмотр остатков на складе", "Принять поставку", "Информация о продуктах"])

    if page == "Просмотр остатков на складе":
        check_stock()
    elif page == "Принять поставку":
        view_shorter_products()
        update_stock()
    elif page == "Информация о продуктах":
        view_full_products_info()


if __name__ == "__main__":
    main()
