import streamlit as st
import pandas as pd
import subprocess
import os
from io import BytesIO

# -------------------------
# CONFIG
# -------------------------

st.set_page_config(
    page_title="Платформа контроля реестров",
    layout="wide"
)

# -------------------------
# HEADER
# -------------------------

st.title("📊 Платформа контроля реестров")
st.caption("Пилотная версия системы анализа корпоративных реестров")

st.write("""
Система выполняет:
- анализ сроков контрактов
- контроль актуальности документов
- проверку реестра имущества
- формирование управленческой отчетности
""")

# -------------------------
# DIRECTORIES
# -------------------------

os.makedirs("output", exist_ok=True)

# -------------------------
# DATA LOAD (DEMO ONLY)
# -------------------------

st.subheader("📥 Загрузка данных")

try:
    contracts_df = pd.read_excel("data/contracts.xlsx")
    documents_df = pd.read_excel("data/documents.xlsx")
    assets_df = pd.read_excel("data/assets.xlsx")

    st.success("📊 Загружены демонстрационные данные из GitHub")

except Exception:
    st.error("❌ Не найдены demo-файлы в папке data/")
    contracts_df = None
    documents_df = None
    assets_df = None

# -------------------------
# DATA PREVIEW
# -------------------------

st.subheader("👀 Предпросмотр данных")

if contracts_df is not None:
    st.write("### Контракты")
    st.dataframe(contracts_df)

if documents_df is not None:
    st.write("### Документы")
    st.dataframe(documents_df)

if assets_df is not None:
    st.write("### Имущество")
    st.dataframe(assets_df)

# -------------------------
# ANALYSIS
# -------------------------

st.subheader("🚀 Анализ")

if st.button("Запустить анализ"):

    st.write("📊 Используются demo-данные из GitHub")

    with st.spinner("Выполняется анализ данных..."):
        subprocess.run(["python", "run_all.py"])

    st.success("✅ Анализ завершен!")

    st.subheader("📊 Результаты анализа")

    # -------------------------
    # CONTRACTS
    # -------------------------

    contracts_result = None

    if os.path.exists("output/renewal_contracts.xlsx"):
        contracts_result = pd.read_excel("output/renewal_contracts.xlsx")
        contracts_result["Priority"] = "High"

        st.write("### 📌 Контракты на перезаключение")
        st.dataframe(contracts_result)

    # -------------------------
    # DOCUMENTS
    # -------------------------

    docs_result = None

    if os.path.exists("output/documents_for_update.xlsx"):
        docs_result = pd.read_excel("output/documents_for_update.xlsx")
        docs_result["Priority"] = "Medium"

        st.write("### 📌 Документы на актуализацию")
        st.dataframe(docs_result)

    # -------------------------
    # ASSETS
    # -------------------------

    assets_result = None

    if os.path.exists("output/asset_issues.xlsx"):
        assets_result = pd.read_excel("output/asset_issues.xlsx")
        assets_result["Priority"] = "High"

        st.write("### 📌 Проблемы по имуществу")
        st.dataframe(assets_result)

    # -------------------------
    # EXCEL REPORT
    # -------------------------

    st.subheader("📥 Управленческий отчет")

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        if contracts_result is not None:
            contracts_result.to_excel(writer, sheet_name="Contracts", index=False)

        if docs_result is not None:
            docs_result.to_excel(writer, sheet_name="Documents", index=False)

        if assets_result is not None:
            assets_result.to_excel(writer, sheet_name="Assets", index=False)

    output.seek(0)

    st.download_button(
        label="📊 Скачать Excel отчет",
        data=output,
        file_name="control_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# -------------------------
# EXECUTIVE SUMMARY
# -------------------------

st.subheader("📌 Executive Summary")

st.info("""
Система выполняет автоматический анализ корпоративных реестров.

Выявляются:
- контракты, требующие перезаключения
- документы на актуализацию
- нарушения по имуществу

Рекомендуется:
- контроль сроков контрактов
- обновление документов
- проверка учета имущества
""")