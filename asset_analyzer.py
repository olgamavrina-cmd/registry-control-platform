import pandas as pd

df = pd.read_excel("data/assets.xlsx")

# 1. Уволенные сотрудники (всегда проблема)
fired_df = df[df["Status"] == "Fired"]

# 2. КРИТИЧНЫЕ категории БЕЗ расписки
critical_no_receipt_df = df[
    (df["Asset Type"].isin(["Laptop", "Test Device"])) &
    (df["Receipt"] == "No")
]

# ОБЪЕДИНЯЕМ ТОЛЬКО РЕАЛЬНЫЕ НАРУШЕНИЯ
issues_df = pd.concat([
    fired_df,
    critical_no_receipt_df
]).drop_duplicates()

# финальная защита — только строки с проблемами
issues_df = issues_df[
    (issues_df["Status"] == "Fired") |
    (
        issues_df["Asset Type"].isin(["Laptop", "Test Device"]) &
        (issues_df["Receipt"] == "No")
    )
]

# сохраняем результат
issues_df.to_excel("output/asset_issues.xlsx", index=False)

print("Анализ имущества завершен")