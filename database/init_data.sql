-- Добавляем роли
INSERT INTO Roles (name, description) 
VALUES 
    ('Администратор', 'Полный доступ к системе'),
    ('Менеджер', 'Управление товарами и поставками'),
    ('Кассир', 'Просмотр и управление инвентаризацией');

-- Добавляем категории товаров
INSERT INTO Categories (name) 
VALUES 
    ('Красное вино'),
    ('Белое вино'),
    ('Игристое вино'),
    ('Десертное вино');

-- Добавляем поставщиков
INSERT INTO Suppliers (name, contact_info) 
VALUES 
    ('Винный дом Бордо', 'Контакты: example1@example.com, +123456789'),
    ('Итальянские вина', 'Контакты: example2@example.com, +987654321');

-- Добавляем товары
INSERT INTO Products (name, type_id, supplier_id, description, price) 
VALUES 
    ('Шато Марго 2015', 1, 1, 'Красное вино премиум класса', 25000.00),
    ('Совиньон Блан 2020', 2, 1, 'Легкое белое вино', 1500.00),
    ('Просекко', 3, 2, 'Итальянское игристое вино', 2000.00),
    ('Портвейн', 4, 2, 'Десертное вино крепленое', 3000.00);

-- Добавляем данные в инвентаризацию
INSERT INTO Inventory (product_id, stock_level, last_checked) 
VALUES 
    (1, 10, CURRENT_TIMESTAMP),
    (2, 50, CURRENT_TIMESTAMP),
    (3, 30, CURRENT_TIMESTAMP),
    (4, 20, CURRENT_TIMESTAMP);
