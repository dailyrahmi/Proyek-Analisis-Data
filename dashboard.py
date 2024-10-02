import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

# Mengatur judul aplikasi dan tema
st.set_page_config(
    page_title="Dashboard Analisis Data Bike Sharing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menambahkan judul utama dan deskripsi aplikasi
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Dashboard Analisis Data Bike Sharing</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Analisis data bike sharing untuk memahami pola penggunaan sepeda berdasarkan hari dan jam.</p>", unsafe_allow_html=True)
st.write("---")

# Memuat dataset pertama (bike sharing day)
df_bike = None
with st.spinner("Memuat dataset..."):
    try:
        # Gunakan path relatif untuk memuat dataset (pastikan file berada di folder yang sama dengan `dashboard.py`)
        df_bike = pd.read_csv(r'Bike Sharing Dataset/day.csv')
        st.success("Dataset bike sharing day berhasil dimuat!")
    except FileNotFoundError:
        st.error("Error memuat dataset bike sharing day: File tidak ditemukan. Pastikan file 'day.csv' berada di dalam folder 'datasets'.")
    except Exception as e:
        st.error(f"Error memuat dataset bike sharing day: {e}")

# Memuat dataset kedua (bike sharing hour)
df_another = None
with st.spinner("Memuat dataset..."):
    try:
        # Gunakan path relatif untuk memuat dataset (pastikan file berada di folder yang sama dengan `dashboard.py`)
        df_another = pd.read_csv(r'Bike Sharing Dataset/day.csv')
        st.success("Dataset bike sharing hour berhasil dimuat!")
    except FileNotFoundError:
        st.error("Error memuat dataset bike sharing hour: File tidak ditemukan. Pastikan file 'hour.csv' berada di dalam folder 'datasets'.")
    except Exception as e:
        st.error(f"Error memuat dataset bike sharing hour: {e}")

# Sidebar untuk navigasi
st.sidebar.header("Navigasi Data Bike Sharing")
menu = st.sidebar.radio("Pilih bagian:", ["Tampilkan Data", "Visualisasi Bike Sharing Day", "Visualisasi Bike Sharing Hour", "Analisis RFM", "Tentang Aplikasi"])

# Menampilkan data berdasarkan pilihan pada sidebar
if menu == "Tampilkan Data":
    st.subheader("Dataset Bike Sharing Day")
    if df_bike is not None and st.checkbox("Tampilkan 5 Data Teratas - Day"):
        st.dataframe(df_bike.head())
    else:
        st.error("Centang checkbox diatas untuk melihat Dataset bike sharing day yang tersedia!")

    st.subheader("Dataset Bike Sharing Hour")
    if df_another is not None and st.checkbox("Tampilkan 5 Data Teratas - Hour"):
        st.dataframe(df_another.head())
    else:
        st.error("Centang checkbox diatas untuk melihat Dataset bike sharing day yang tersedia!")

# Visualisasi untuk dataset bike sharing day
if menu == "Visualisasi Bike Sharing Day" and df_bike is not None:
    st.subheader("Visualisasi Data Bike Sharing Day")
    if 'season' in df_bike.columns:
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        sns.countplot(data=df_bike, x='season', palette="coolwarm")
        plt.title("Distribusi Penggunaan Sepeda Berdasarkan Musim", fontsize=16)
        plt.xlabel("Musim", fontsize=14)
        plt.ylabel("Jumlah Penggunaan", fontsize=14)
        st.pyplot(plt)
        st.markdown(""" 
        Dari visualisasi ini, terlihat bahwa penggunaan sepeda tertinggi terjadi pada musim panas. 
        Hal ini mungkin disebabkan oleh cuaca yang lebih baik dan lebih banyak kegiatan luar ruangan. 
        Sementara itu, penggunaan sepeda menurun pada musim dingin, yang menunjukkan bahwa kondisi cuaca 
        memainkan peran penting dalam keputusan peminjaman sepeda.
        """)
    else:
        st.error("Kolom 'season' tidak ditemukan pada dataset bike sharing day!")

# Visualisasi untuk dataset bike sharing hour
if menu == "Visualisasi Bike Sharing Hour" and df_another is not None:
    st.subheader("Visualisasi Data Bike Sharing Hour")
    st.write("Kolom yang tersedia pada dataset kedua:", df_another.columns.tolist())
    column_name = st.selectbox("Pilih kolom untuk visualisasi:", options=df_another.columns, index=df_another.columns.get_loc("hr"))  # Pilih kolom 'hr' secara default
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.countplot(data=df_another, x=column_name, palette="viridis")
    plt.title(f"Distribusi Penggunaan Sepeda Berdasarkan {column_name.capitalize()}", fontsize=16)
    plt.xlabel(column_name.capitalize(), fontsize=14)
    plt.ylabel("Jumlah Penggunaan", fontsize=14)
    st.pyplot(plt)
    st.markdown(f"""
    Visualisasi ini menunjukkan distribusi penggunaan sepeda berdasarkan {column_name}. 
    Anda dapat melihat pola penggunaan sepeda pada jam-jam tertentu. 
    Misalnya, penggunaan sepeda cenderung meningkat pada jam-jam sibuk, 
    yang menunjukkan bahwa sepeda sering digunakan untuk perjalanan kerja dan kegiatan lainnya.
    """)

# Menambahkan analisis RFM jika dataset berhasil dimuat
if menu == "Analisis RFM":
    st.subheader("Analisis RFM")
    st.markdown("""
    Analisis RFM (Recency, Frequency, Monetary) bertujuan untuk mengelompokkan pelanggan berdasarkan perilaku peminjaman mereka.

    - **Recency:** Menghitung jumlah hari sejak terakhir kali pelanggan melakukan peminjaman.
    - **Frequency:** Menghitung jumlah total peminjaman yang dilakukan oleh pelanggan dalam periode tertentu.
    - **Monetary:** Menghitung total pengeluaran pelanggan dalam periode tersebut.
    """)

    # RFM analysis code (gunakan sample data untuk testing jika dataset tidak tersedia)
    if df_bike is not None:
        # Contoh data yang bisa digantikan dengan dataset Anda
        data = {
            'customer_id': [1, 2, 1, 3, 2, 1, 3, 3],
            'transaction_date': [
                '2024-01-01', '2024-01-05', '2024-02-01', 
                '2024-02-15', '2024-03-01', '2024-03-10', 
                '2024-03-20', '2024-03-25'
            ],
            'amount': [10, 20, 15, 10, 25, 30, 5, 20]
        }

        # Membuat DataFrame dari data di atas
        df = pd.DataFrame(data)

        # Mengubah 'transaction_date' menjadi tipe datetime
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])

        # Menentukan tanggal analisis
        analysis_date = dt.datetime.now()

        # Menghitung metrik RFM
        rfm_df = df.groupby('customer_id').agg({
            'transaction_date': lambda x: (analysis_date - x.max()).days,  # Recency
            'amount': ['count', 'sum']  # Frequency dan Monetary
        }).reset_index()

        # Mengubah nama kolom
        rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']

        # Menampilkan DataFrame RFM
        st.write("Dataframe RFM:")
        st.dataframe(rfm_df)

        # Contoh segmentasi pelanggan berdasarkan nilai RFM
        def assign_rfm_scores(df):
            df['R_score'] = pd.cut(df['recency'], bins=4, labels=False)
            df['F_score'] = pd.cut(df['frequency'], bins=4, labels=False)
            df['M_score'] = pd.cut(df['monetary'], bins=4, labels=False)
            return df

        # Memberikan skor RFM
        rfm_df = assign_rfm_scores(rfm_df)

        # Membuat Segmen RFM
        rfm_df['RFM_Segment'] = rfm_df['R_score'].astype(str) + rfm_df['F_score'].astype(str) + rfm_df['M_score'].astype(str)

        # Menampilkan segmen RFM
        st.write("RFM Segments:")
        st.dataframe(rfm_df[['customer_id', 'recency', 'frequency', 'monetary', 'RFM_Segment']])
    else:
        st.error("Dataset tidak tersedia untuk analisis RFM!")

# Menampilkan informasi tentang aplikasi
if menu == "Tentang Aplikasi":
    st.subheader("Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini merupakan dashboard analisis data penggunaan sepeda berdasarkan dataset bike sharing.
    Tujuannya adalah untuk membantu memahami pola penggunaan sepeda berdasarkan waktu (hari dan jam).
    
    **Fitur Utama:**
    - Menampilkan data bike sharing day dan hour.
    - Visualisasi distribusi penggunaan sepeda berdasarkan musim, jam, dan kategori lainnya.
    - Tampilan interaktif dan mudah digunakan.

    Dibuat menggunakan `Streamlit`, `Pandas`, `Seaborn`, dan `Matplotlib`.
    """)

# Menambahkan footer dengan informasi tambahan
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>© 2024 Dashboard Analisis Data Bike Sharing. Dibuat untuk proyek analisis data.</p>", unsafe_allow_html=True)
