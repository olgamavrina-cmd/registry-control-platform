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
- контроль сроков контрактов
- анализ актуальности документов
- проверку данных по имуществу
""")

# -------------------------
# DATA DIRECTORY
# -------------------------

os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

# -------------------------
# ЗАГРУЗКА ФАЙЛОВ
# -------------------------

st.subheader("📥 Загрузка данных")

# -------------------------
# DEMO FILES FROM GITHUB
# -------------------------

try:
    demo_contracts = pd.read_excel("contracts.xlsx")
    demo_documents = pd.read_excel("documents.xlsx")
    demo_assets = pd.read_excel("assets.xlsx")

    # Копируем demo-файлы в data/
    demo_contracts.to_excel("data/contracts.xlsx", index=False)
    demo_documents.to_excel("data/documents.xlsx", index=False)
    demo_assets.to_excel("data/assets.xlsx", index=False)

    st.success("📊 Загружены демонстрационные данные из GitHub")

except Exception:
    st.warning("⚠️ Демонстрационные файлы не найдены")

# -------------------------
# USER FILE UPLOAD
# -------------------------

st.write("### Загрузите пользовательские файлы (опционально)")

contracts_file = st.file_uploader(
    "Контракты",
    type=["xlsx"]
)

documents_file = st.file_uploader(
    "Документы",
    type=["xlsx"]
)

assets_file = st.file_uploader(
    "Имущество",
    type=["xlsx"]
)

# -------------------------
# SAVE UPLOADED FILES
# -------------------------

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
# DATA PREVIEW
# -------------------------

st.subheader("👀 Предпросмотр данных")

if os.path.exists("data/contracts.xlsx"):
    st.write("### Контракты")
    contracts_preview = pd.read_excel("data/contracts.xlsx")
    st.dataframe(contracts_preview)

if os.path.exists("data/documents.xlsx"):
    st.write("### Документы")
    documents_preview = pd.read_excel("data/documents.xlsx")
    st.dataframe(documents_preview)

if os.path.exists("data/assets.xlsx"):
    st.write("### Имущество")
    assets_preview = pd.read_excel("data/assets.xlsx")
    st.dataframe(assets_preview)

# -------------------------
# ANALYSIS
# -------------------------

st.subheader("🚀 Анализ")

if st.button("Запустить анализ"):

    with st.spinner("Выполняется анализ данных..."):

        subprocess.run(["python", "run_all.py"])

    st.success("✅ Анализ завершен!")

    st.subheader("📊 Результаты анализа")

    # -------------------------
    # CONTRACTS RESULTS
    # -------------------------

    contracts_df = None

    if os.path.exists("output/renewal_contracts.xlsx"):

        contracts_df = pd.read_excel(
            "output/renewal_contracts.xlsx"
        )

        contracts_df["Priority"] = "High"

        st.write("### 📌 Контракты на перезаключение")
        st.dataframe(contracts_df)

    # -------------------------
    # DOCUMENTS RESULTS
    # -------------------------

    docs_df = None

    if os.path.exists("output/documents_for_update.xlsx"):

        docs_df = pd.read_excel(
            "output/documents_for_update.xlsx"
        )

        docs_df["Priority"] = "Medium"

        st.write("### 📌 Документы на актуализацию")
        st.dataframe(docs_df)

    # -------------------------
    # ASSETS RESULTS
    # -------------------------

    assets_df = None

    if os.path.exists("output/asset_issues.xlsx"):

        assets_df = pd.read_excel(
            "output/asset_issues.xlsx"
        )

        assets_df["Priority"] = "High"

        st.write("### 📌 Проблемы по имуществу")
        st.dataframe(assets_df)

    # -------------------------
    # EXCEL REPORT
    # -------------------------

    st.subheader("📥 Управленческий отчет")

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        if contracts_df is not None:
            contracts_df.to_excel(
                writer,
                sheet_name="Contracts_to_work",
                index=False
            )

        if docs_df is not None:
            docs_df.to_excel(
                writer,
                sheet_name="Documents_to_update",
                index=False
            )

        if assets_df is not None:
            assets_df.to_excel(
                writer,
                sheet_name="Assets_issues",
                index=False
            )

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