import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import datetime

def download_excel(df, filename):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return buffer.getvalue()

# Загрузка файла
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Чтение файла в датафрейм
    df = pd.read_excel(uploaded_file)

    # Преобразования над датафреймом


    df = df[['Содержимое', 'Tag']].fillna(value="-")

    filtered_df = df[df['Содержимое'].str.contains(r'((\d\d)|([O0О][ABАВ]))-?[ВСДОКCOKB]{1,2}\d\d\d', regex=True)]

    filtered_df2 = df[df['Tag'].str.contains(r'((\d\d)|([O0О][ABАВ]))-?[ВСДОКCOKB]{1,2}\d\d\d', regex=True)]

    combined_df = pd.concat([filtered_df["Содержимое"], filtered_df2["Tag"]])

    combined_df = combined_df.reset_index(drop=True)

    df1 = pd.DataFrame(combined_df, columns=['ЗРА'])

    replacement_dict = {'B': 'В', 'C': 'С', 'O': 'О', 'K': 'К'}
    df1['ЗРА'] = df1['ЗРА'].replace(replacement_dict, regex=True)

    df1 = df1.replace(r'\\pxqc;', '', regex=True)

    df1 = df1.replace(r'^[0OО][AА]', '0А', regex=True)

    df1 = df1.replace(r'^[0OО][BВ]', '0В', regex=True)

    df2 = df1['ЗРА'].str.extract(r'(?P<Вид_ЗРА>[ВСДОКCOKB]{1,2})(?P<Номер>\d{3,4})')

    df2['Подсистема'] = df1['ЗРА'].str[:2]

    df2 = df2[['Подсистема', 'Вид_ЗРА', 'Номер']]

    df2 = pd.concat([df1, df2], axis=1)

    # Получить сегодняшнюю дату в формате DD_MM_YYYY
    today_date = datetime.today().strftime('%d_%m_%Y')

    # Формируйте название файла, используя сегодняшнюю дату
    file_name = f'ЗРА из dwg {today_date}.xlsx'

    #df2.to_excel(file_name, index=False)

    # Сохранение датафрейма в новый файл Excel

    st.write(f"Файл {file_name} успешно сохранен!")



    excel_bytes = download_excel(df2, 'data.xlsx')

    st.download_button(
        label="Скачать Excel-файл",
        data=excel_bytes,
        file_name=file_name,
        mime="application/vnd.ms-excel",)



