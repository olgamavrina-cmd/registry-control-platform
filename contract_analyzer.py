import pandas as pd
from datetime import datetime, timedelta

# Загружаем Excel
df = pd.read_excel("data/contracts.xlsx")

# Текущая дата
today = datetime.today()

# Дата +30 дней
next_month = today + timedelta(days=30)

# Контракты в архив
archive_df = df[df["Cooperation Status"] == "Terminated"]

# Преобразуем дату
df["Contract End Date"] = pd.to_datetime(df["Contract End Date"])

# Контракты на перезаключение
renewal_df = df[
    (df["Contract End Date"] >= today) &
    (df["Contract End Date"] <= next_month)
]

# Сохраняем результаты
archive_df.to_excel("output/archive_contracts.xlsx", index=False)
renewal_df.to_excel("output/renewal_contracts.xlsx", index=False)

print("Анализ контрактов завершен")