import pandas as pd
from datetime import datetime, timedelta

# Загружаем данные
df = pd.read_excel("data/documents.xlsx")

# Текущая дата
today = datetime.today()

# +4 месяца (примерно 120 дней)
limit_date = today + timedelta(days=120)

# Преобразуем дату
df["Expiration Date"] = pd.to_datetime(df["Expiration Date"])

# Фильтр документов на актуализацию
update_df = df[df["Expiration Date"] <= limit_date]

# Сохраняем результат
update_df.to_excel("output/documents_for_update.xlsx", index=False)

print("Анализ документов завершен")