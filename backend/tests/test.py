import csv
import random

# Списки для генерации
first_names = [
    "Алексей", "Михаил", "Иван", "Никита", "Дмитрий",
    "Сергей", "Егор", "Артем", "Максим", "Олег",
    "Александр", "Антон", "Ярослав", "Богдан", "Владимир"
]

last_initials = ["А.", "Б.", "В.", "Г.", "Д.", "Е.", "Ж.", "З.", "И.", "К."]

regions = [
    "город Москва", "Санкт-Петербург", "Московская область", "Татарстан",
    "Свердловская область", "Чеченская Республика", "Краснодарский край",
    "Хабаровский край", "Ярославская область", "Челябинская область",
    "Удмуртская Республика", "Республика Мордовия", "Вологодская область"
]

statuses = ["Победитель", "Призер", ""]


def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_initials)}"


def generate_olymp_csv(n):
    with open("olymp.csv", mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Имя", "Регион", "Балл", "Статус"])

        for _ in range(n):
            name = generate_name()
            region = random.choice(regions)
            score = random.randint(300, 500)
            status = random.choices(statuses, weights=[0.1, 0.3, 0.6])[0]  # Победитель реже
            writer.writerow([name, region, score, status])


# Пример вызова
generate_olymp_csv(100)  # создаст 100 строк в olymp.csv

import pandas as pd