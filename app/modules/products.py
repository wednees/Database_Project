import os
import bcrypt
import psycopg2
import streamlit as st

from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from modules.connection import get_connection

    
def view_shorter_products():
    st.subheader("Продукты")

    # Просмотр товаров
    if st.button("Просмотреть товары"):
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id as ID, name as Название FROM Products")
            products = cur.fetchall()
            st.table(products)

def view_full_products_info():
    st.subheader("Продукты")

    # Просмотр товаров
    if st.button("Просмотреть товары"):
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""SELECT Products.name as Название, 
                        Categories.name as Категория,
                        description as Описание,
                        price as Цена
                        FROM Products LEFT JOIN Categories ON Categories.id = type_id""")
            products = cur.fetchall()
            st.table(products)



def add_product():
    st.subheader("Добавление нового товара")

    # Добавление товара
    with st.form("add_product_form"):
        st.write("Добавить новый товар")
        name = st.text_input("Название товара", max_chars=100)
        type_id = st.text_input("ID категории")
        supplier_id = st.text_input("ID поставщика")
        description = st.text_area("Описание", max_chars=500)
        price = st.number_input("Цена", min_value=0.01, step=0.01)
        submit = st.form_submit_button("Добавить")
        
        if submit:
            # Проверка на заполнение всех обязательных полей
            if not name.strip():
                st.error("Название товара обязательно для заполнения.")
                return
            if not type_id.strip().isdigit():
                st.error("ID категории должно быть числом.")
                return
            if not supplier_id.strip().isdigit():
                st.error("ID поставщика должно быть числом.")
                return

            # Подключение к базе данных
            try:
                conn = get_connection()
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO Products (name, type_id, supplier_id, description, price) VALUES (%s, %s, %s, %s, %s)",
                        (name, int(type_id), int(supplier_id), description, price)
                    )
                    conn.commit()
                    st.success("Товар добавлен!")
            except psycopg2.IntegrityError:
                st.error("Ошибка: ID категории или ID поставщика не существует.")
            except psycopg2.DatabaseError as e:
                st.error(f"Ошибка базы данных: {e}")
            except Exception as e:
                st.error(f"Неизвестная ошибка: {e}")



def delete_product_func(product_id):
    """Удаляет товар из базы данных по его ID."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Проверка, существует ли товар с данным ID
            cur.execute("SELECT * FROM Products WHERE id = %s", (product_id,))
            product = cur.fetchone()
            if not product:
                st.error("Товар с указанным ID не найден.")
                return

            # Удаление товара
            cur.execute("DELETE FROM Products WHERE id = %s", (product_id,))
            conn.commit()
            st.success(f"Товар с ID {product_id} успешно удален.")
    except psycopg2.Error as e:
        st.error(f"Ошибка при удалении товара: {e}")

def delete_product():
    """Интерфейс Streamlit для удаления товара."""
    st.subheader("Удаление товара")

    # Поле ввода для ID товара
    product_id = st.text_input("Введите ID товара для удаления")

    if st.button("Удалить товар"):
        if product_id.isdigit():
            delete_product_func(int(product_id))
        else:
            st.error("ID товара должен быть числом.")



def view_suppliers():
    st.subheader("Поставщики")

    if st.button("Просмтореть поставщиков"):
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id as ID, name as Название, contact_info as Контакты FROM Suppliers")
            products = cur.fetchall()
            st.table(products)



def view_categories():
    st.subheader("Категории")

    if st.button("Просмотреть категории"):
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id as ID, name as Категория FROM Categories")
            products = cur.fetchall()
            st.table(products)