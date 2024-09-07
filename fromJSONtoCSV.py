import json
import csv

#Можно сказать, что в создании этого кода я тоже принимал какое-то участие

# Откроем JSON-файл и загрузим данные
with open('countries.json', 'r') as json_file:
    data = json.load(json_file)

# Собираем все уникальные показатели
all_indicators = set()

for country_data in data:
    for country, indicators in country_data.items():
        all_indicators.update(indicators.keys())
        # for indicator_set in indicators.:
        #     all_indicators.update(indicator_set.keys())

# Преобразуем множество в список для заголовков CSV
fieldnames = ["Country"] + list(all_indicators)

# Записываем данные в CSV
with open('countries.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Запишем заголовки
    writer.writeheader()
    
    # Обрабатываем данные по каждой стране
    for country_data in data:
        for country, indicators in country_data.items():
            # Для каждой страны собираем строки данных
                row = {"Country": country}
                
                # Добавляем показатели для этой строки
                row.update(indicators)
                
                # Записываем строку в CSV
                writer.writerow(row)

#Ура! csv открыт в ноутбуке!