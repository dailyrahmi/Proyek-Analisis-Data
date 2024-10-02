import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
with st.spinner("Memuat dataset..."):
    try:
        df_bike = pd.read_csv(r'C:\Users\Asus\Documents\DICODING\Bike Sharing Dataset\day.csv')
        st.success("Dataset bike sharing day berhasil dimuat!")
    except Exception as e:
        st.error(f"Error memuat dataset bike sharing day: {e}")

# Memuat dataset kedua (bike sharing hour)
with st.spinner("Memuat dataset..."):
    try:
        df_another = pd.read_csv(r'C:\Users\Asus\Documents\DICODING\Bike Sharing Dataset\hour.csv')
        st.success("Dataset bike sharing hour berhasil dimuat!")
    except Exception as e:
        st.error(f"Error memuat dataset bike sharing hour: {e}")

# Sidebar untuk navigasi
st.sidebar.header("Navigasi")
menu = st.sidebar.radio("Pilih bagian:", ["Tampilkan Data", "Visualisasi Bike Sharing Day", "Visualisasi Bike Sharing Hour", "Analisis RFM", "Tentang Aplikasi"])

# Menampilkan data berdasarkan pilihan pada sidebar
if menu == "Tampilkan Data":
    st.subheader("Dataset Bike Sharing Day")
    if st.checkbox("Tampilkan 5 Data Teratas - Day"):
        st.dataframe(df_bike.head())
    st.subheader("Dataset Bike Sharing Hour")
    if st.checkbox("Tampilkan 5 Data Teratas - Hour"):
        st.dataframe(df_another.head())

# Visualisasi untuk dataset bike sharing day
if menu == "Visualisasi Bike Sharing Day":
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
        **Insight:**
        Penggunaan sepeda cenderung lebih tinggi pada musim tertentu, seperti musim panas, yang dapat dijadikan dasar strategi penambahan sepeda di musim tersebut.
        """)
    else:
        st.error("Kolom 'season' tidak ditemukan pada dataset bike sharing day!")

# Visualisasi untuk dataset bike sharing hour
if menu == "Visualisasi Bike Sharing Hour":
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

    st.markdown("""
    **Insight:**
    Tren peminjaman sepeda menunjukkan bahwa jam sibuk pagi dan sore (sekitar pukul 7-9 dan 17-19) merupakan waktu terbaik untuk menambah armada sepeda.
    """)

# Menambahkan analisis tambahan (contoh: RFM Analysis)
if menu == "Analisis RFM":
    st.subheader("Analisis RFM (Recency, Frequency, Monetary)")
    st.markdown("""
    Analisis RFM dilakukan untuk mengelompokkan pelanggan berdasarkan perilaku peminjaman mereka. 
    Ini membantu memahami karakteristik pengguna, apakah mereka sering menggunakan sepeda (frequency), 
    kapan terakhir kali menggunakan sepeda (recency), dan seberapa sering mereka meminjam sepeda.
    """)
    # Contoh implementasi analisis RFM sederhana
    df_another['recency'] = df_another['dteday'].apply(lambda x: pd.to_datetime('today') - pd.to_datetime(x))
    df_another['frequency'] = df_another.groupby('instant')['instant'].transform('count')
    df_another['monetary'] = df_another['cnt']

    # Menampilkan tabel hasil analisis
    st.write("Tabel Hasil Analisis RFM:")
    st.dataframe(df_another[['recency', 'frequency', 'monetary']].head())

    st.markdown("""
    **Insight:**
    Pengguna yang sering meminjam sepeda dapat dianggap sebagai pengguna setia dan dapat diberi penawaran khusus untuk meningkatkan loyalitas.
    """)

# Menampilkan informasi tentang aplikasi
if menu == "Tentang Aplikasi":
    st.subheader("Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini merupakan dashboard analisis data penggunaan sepeda berdasarkan dataset bike sharing.
    Tujuannya adalah untuk membantu memahami pola penggunaan sepeda berdasarkan waktu (hari dan jam).

    **Fitur Utama:**
    - Menampilkan data bike sharing day dan hour.
    - Visualisasi distribusi penggunaan sepeda berdasarkan musim, jam, dan kategori lainnya.
    - Analisis RFM sederhana untuk mengelompokkan pengguna berdasarkan perilaku peminjaman.
    - Tampilan interaktif dan mudah digunakan.

    Dibuat menggunakan `Streamlit`, `Pandas`, `Seaborn`, dan `Matplotlib`.
    """)

# Menambahkan footer dengan informasi tambahan
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>© 2024 Dashboard Analisis Data Bike Sharing. Dibuat untuk proyek analisis data.</p>", unsafe_allow_html=True)
