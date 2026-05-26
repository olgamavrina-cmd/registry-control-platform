import subprocess

print("Запуск анализа реестров...\n")

# 1. Контракты
print("Анализ контрактов...")
subprocess.run(["python", "contract_analyzer.py"])

# 2. Документы
print("Анализ документов...")
subprocess.run(["python", "document_analyzer.py"])

# 3. Имущество
print("Анализ имущества...")
subprocess.run(["python", "asset_analyzer.py"])

print("\nВсе реестры обработаны успешно!")
print("Результаты сохранены в папке output/")