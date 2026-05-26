import streamlit as st
import pandas as pd
import subprocess
import os
from io import BytesIO

st.set_page_config(page_title="Платформа контроля реестров", layout="wide")

st.title("📊 Платформа контроля реестров")
st.write("Анализ корпоративных реестров")

# -------------------------
# ЗАГРУЗКА ФАЙЛОВ
# -------------------------

st.subheader("📥 Загрузка данных")

contracts_file = st.file_uploader("Контракты", type=["xlsx"])
documents_file = st.file_uploader("Документы", type=["xlsx"])
assets_file = st.file_uploader("Имущество", type=["xlsx"])

os.makedirs("data", exist_ok=True)

if contracts_file:
    with open("data/contracts.xlsx", "wb") as f:
        f.write(contracts_file.getbuffer())

if documents_file:
    with open("data/documents.xlsx", "wb") as f:
        f.write(documents_file.getbuffer())

if assets_file:
    with open("data/assets.xlsx", "wb") as f:
        f.write(assets_file.getbuffer())


# -------------------------
# АНАЛИЗ
# -------------------------

if st.button("🚀 Запустить анализ"):

    st.write("Анализ выполняется...")

    subprocess.run(["python", "run_all.py"])

    st.success("Анализ завершен!")

    st.subheader("📊 Результаты")

    # -------------------------
    # КОНТРАКТЫ
    # -------------------------
    contracts_df = None
    if os.path.exists("output/renewal_contracts.xlsx"):
        contracts_df = pd.read_excel("output/renewal_contracts.xlsx")

        contracts_df["Priority"] = "High"

        st.write("📌 Контракты на перезаключение")
        st.dataframe(contracts_df)

    # -------------------------
    # ДОКУМЕНТЫ
    # -------------------------
    docs_df = None
    if os.path.exists("output/documents_for_update.xlsx"):
        docs_df = pd.read_excel("output/documents_for_update.xlsx")

        docs_df["Priority"] = "Medium"

        st.write("📌 Документы на актуализацию")
        st.dataframe(docs_df)

    # -------------------------
    # ИМУЩЕСТВО
    # -------------------------
    assets_df = None
    if os.path.exists("output/asset_issues.xlsx"):
        assets_df = pd.read_excel("output/asset_issues.xlsx")

        assets_df["Priority"] = "High"

        st.write("📌 Проблемы по имуществу")
        st.dataframe(assets_df)


    # -------------------------
    # EXCEL ОТЧЕТ
    # -------------------------

    st.subheader("📥 Управленческий отчет (Excel)")

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        # Контракты
        if contracts_df is not None:
            contracts_df.to_excel(writer, sheet_name="Contracts_to_work", index=False)

        # Документы
        if docs_df is not None:
            docs_df.to_excel(writer, sheet_name="Documents_to_update", index=False)

        # Имущество
        if assets_df is not None:
            assets_df.to_excel(writer, sheet_name="Assets_issues", index=False)

        writer.close()

    output.seek(0)

    st.download_button(
        label="📊 Скачать Excel отчет",
        data=output,
        file_name="control_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # -------------------------
    # BUSINESS SUMMARY
    # -------------------------

    st.subheader("📌 Executive Summary")

    st.info("""
Система выполнила анализ корпоративных реестров.

Выявлены:
- контракты, требующие перезаключения (High Priority)
- документы на актуализацию (Medium Priority)
- нарушения по имуществу (High Priority)

Рекомендуется:
- провести контроль сроков контрактов
- обновить нормативные документы
- провести контроль документов выдачи имущества
""")