import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import pyodbc
from datetime import datetime

#Sehifenin nastroykasi
st.set_page_config(
    page_title='BAZARLAMA ÇEŞİD SAYI',
    page_icon='logo.png',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# BAZARLAMA ÇEŞİD SAYI \n Bu hesabat FAB şirkətlər qrupu üçün hazırlanmışdır."
    }
)

css_header = """
<style>

    [data-testid="stHeader"] {
        display: none;
    }
    
    [data-testid="stElementToolbar"] {
        display: none;
    }
    
</style>
<title>BAZARLAMA ÇEŞİD SAYI</title>
<meta name="description" content="FAB Şirkətlər Qrupu" />
"""

st.markdown(css_header, unsafe_allow_html=True)

# =============================================================================
# try:  
# =============================================================================
#Sehifenin adini tablari duzeldirik
st.header('BAZARLAMA ÇEŞİD SAYI', divider='rainbow', anchor=False)

# Connect to the database
def get_db_connection():
    server = '192.168.1.245'
    database = 'MikroDB_V16_05'
    username = 'MA'
    password = 'mikro'
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    return pyodbc.connect(conn_str)
    
current_month = datetime.now().month
year = st.selectbox("İl seçin:", [2024], index=0)
month_names = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "İyun", 
           "İyul", "Avqust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"]
month_index = st.selectbox("Ay seçin:", month_names, index=current_month - 1)
month = month_names.index(month_index) + 1


# SQL query function
def fetch_data(year, month):
    query = f"""  
SELECT
    SUBSTRING(STK.sth_evrakno_seri, 2, LEN(STK.sth_evrakno_seri) - 1) AS BAZARLAMA_KOD,
	PER.cari_per_adi as BAZARLAMA_AD,
    COUNT(DISTINCT STK.sth_stok_kod) AS CESID_SAYI
FROM
    STOK_HAREKETLERI STK
LEFT JOIN
	CARI_PERSONEL_TANIMLARI PER
	ON SUBSTRING(STK.sth_evrakno_seri, 2, LEN(STK.sth_evrakno_seri) - 1) = PER.cari_per_kod
WHERE
    YEAR(sth_tarih) = {year}
    AND MONTH(sth_tarih) = {month}
    AND sth_tip = 1
    AND sth_cins = 0
    AND sth_normal_iade = 0
    AND sth_evrakno_seri LIKE 'O%'
    AND sth_evrakno_seri NOT LIKE 'OMID%'
GROUP BY
    SUBSTRING(STK.sth_evrakno_seri, 2, LEN(STK.sth_evrakno_seri) - 1),
	PER.cari_per_adi
ORDER BY
    BAZARLAMA_KOD;
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]  # Get column names from cursor
    df = pd.DataFrame.from_records(rows, columns=columns)

    cursor.close()
    conn.close()

    return df

# Execute query and fetch data
df = fetch_data(year, month)
df.index = np.arange(1, len(df)+1)

# Display the DataFrame in Streamlit
if not df.empty:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Ümumi')
    excel_data = output.getvalue()
    st.download_button(
        label=":green[Cədvəli Excel'ə yüklə] :floppy_disk:",
        data=excel_data,
        file_name='BAZARLAMA ÇEŞİD SAYI.xlsx',
    )
    st.table(df)
else:
    st.error("Məlumat tapımadı.")
    
# =============================================================================
# except:
#     st.error('Məlumatlar yenilənmişdir. Zəhmət olmasa sol üstə yerləşən "Məlumatları Yenilə" düyməsinə basın.')
# =============================================================================
    
    
css_page = """
<style>

    th {
       color: black;
       font-weight: bold;
    }
        
    

    [data-testid="stHeader"] {
        display: none;
    }
    
    [class="viewerBadge_link__qRIco"] {
        display: none;
    }
    
    [data-testid="stElementToolbar"] {
        display: none;
    }
    
    button[title="View fullscreen"] {
        visibility: hidden;
    }
    
</style>
<title>FAB MARKALAR</title>
<meta name="description" content="FAB Şirkətlər Qrupu" />
"""

st.markdown(css_page, unsafe_allow_html=True)