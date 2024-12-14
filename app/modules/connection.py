import os
import psycopg2
import streamlit as st

from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

@st.cache_resource
def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, cursor_factory=RealDictCursor
    )
    return conn