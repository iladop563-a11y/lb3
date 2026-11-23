"""Лабораторна робота №3: винятки, модулі, документація, інтроспекція."""
import logging
from tempfile import TemporaryDirectory
from pathlib import Path

from shop import create_product, find_product
from shop.models.exceptions import ShopError, ValidationError, ProductNotFoundError
from shop.models import products
from shop.utils.files import write_text, read_text


def task1() -> None:
    print("\n========== ЗАВДАННЯ 1 ==========")
    print("Сценарій 1: try/except")
    for value in ("100", "не число"):
        try:
            print("Успіх:", int(value))
        except ValueError:
            print("Помилка: введено не число")

    print("\nСценарій 2: try/except/else/finally")
    for divisor in (5, 0):
        try:
            result = 10 / divisor
        except ZeroDivisionError:
            print("Помилка обчислення")
        else:
            print("Результат:", result)
        finally:
            print("Операцію завершено")

    print("\nСценарій 3: декілька виключень")
    for value, divisor in (("8", 2), ("x", 2), ("8", 0)):
        try:
            print("Успіх:", int(value) / divisor)
        except (ValueError, ZeroDivisionError):
            print("Помилка введення або ділення")

    print("\nРобота з файлом")
    with TemporaryDirectory() as folder:
        path = str(Path(folder) / "example.txt")
        write_text(path, "Тестовий запис")
        assert read_text(path) == "Тестовий запис"
        print("Файл успішно створено")


def task2() -> None:
    print("\n========== ЗАВДАННЯ 2 ==========")
    try:
        create_product("", 100)
    except ValidationError as error:
        print("Помилка перевірки:", error)

    try:
        find_product([create_product("Ноутбук", 25000)], "Телефон")
    except ProductNotFoundError as error:
        print("Помилка пошуку:", error)

    try:
        read_text("missing.txt")
    except FileNotFoundError as error:
        print("Помилка файлу:", error)

    try:
        create_product("Ноутбук", -1)
    except ShopError as error:
        print("Базовий клас перехопив:", error)
        logging.warning("Помилка перевірки: %s", error)
        print("Помилку записано в журнал")

    try:
        raise ValidationError("Некоректне поле: quantity")
    except ValidationError as error:
        print("Повторно перехоплено:", error)


def task3() -> None:
    print("\n========== ЗАВДАННЯ 3 ==========")
    product = create_product("Ноутбук", 25000)
    print("Створений товар:", product)
    print("Назва модуля:", products.__name__)
    print("Експорт пакета:", products.__all__)
    print("Імпортовані імена:", ["create_product", "find_product"])
    print("create_product:", callable(create_product))
    print("find_product:", callable(find_product))


def task4() -> None:
    print("\n========== ЗАВДАННЯ 4 ==========")
    print("Назва:", create_product.__name__)
    print("\nДокументація:\n", create_product.__doc__)
    print("Анотації:", create_product.__annotations__)
    print("\nHELP:")
    help(create_product)


def main() -> None:
    logging.basicConfig(filename="shop.log", level=logging.WARNING, encoding="utf-8")
    task1()
    task2()
    task3()
    task4()


if __name__ == "__main__":
    main()
