-- Создаем таблицу для категорий товаров
CREATE TABLE Categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Создаем таблицу для поставщиков
CREATE TABLE Suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info TEXT
);

-- Создаем таблицу для товаров
CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type_id INT NOT NULL REFERENCES Categories(id),
    supplier_id INT REFERENCES Suppliers(id),
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

-- Создаем таблицу для поставок
CREATE TABLE Shipments (
    id SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL REFERENCES Suppliers(id),
    product_id INT NOT NULL REFERENCES Products(id),
    shipment_date TIMESTAMP NOT NULL,
    quantity INT NOT NULL
);

-- Создаем таблицу для инвентаря
CREATE TABLE Inventory (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES Products(id),
    stock_level INT NOT NULL,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создаем таблицу для ролей
CREATE TABLE Roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Создаем таблицу для сотрудников
CREATE TABLE Employees (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL REFERENCES Roles(id)
);

-- Создаем таблицу для логов
CREATE TABLE Logs (
    id SERIAL PRIMARY KEY,
    employee_id INT,
    action VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
