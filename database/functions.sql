-- Функция для записи действий в таблицу Logs
DROP FUNCTION IF EXISTS public.log_action();
CREATE OR REPLACE FUNCTION log_action()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Logs (employee_id, action)
    VALUES (
        COALESCE(NEW.id, OLD.id), -- Используем ID новой записи или старой записи
        TG_OP || ' on ' || TG_TABLE_NAME
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Триггер для автоматического вызова функции log_action при изменениях в таблице Employees
CREATE TRIGGER log_employee_action
AFTER INSERT OR DELETE OR UPDATE ON Employees
FOR EACH ROW
EXECUTE PROCEDURE log_action();

CREATE TRIGGER log_product_action
AFTER INSERT OR DELETE OR UPDATE ON Products
FOR EACH ROW
EXECUTE PROCEDURE log_action();

CREATE TRIGGER log_inventory_action
AFTER INSERT OR DELETE OR UPDATE ON Inventory
FOR EACH ROW
EXECUTE PROCEDURE log_action();
