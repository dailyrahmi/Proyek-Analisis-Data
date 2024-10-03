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
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Dashboard Analisis Data Bike Sharing🚴</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Analisis data bike sharing untuk memahami pola penggunaan sepeda berdasarkan hari dan jam.</p>", unsafe_allow_html=True)
st.write("---")

# Menambahkan gambar di sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/GhefiraZahraNurFadhilah/ProyekAnalisisDataDicoding/main/assets/bike.jpg")

# Memuat dataset pertama (bike sharing day)
df_bike = None
with st.spinner("Memuat dataset..."):
    try:
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
        df_another = pd.read_csv(r'Bike Sharing Dataset/hour.csv')
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
        st.error("Centang checkbox diatas untuk melihat Dataset bike sharing hour yang tersedia!")

# Menampilkan informasi metrik
if df_bike is not None:
    total_rentals = df_bike['cnt'].sum()
    total_registered = df_bike['registered'].sum()
    total_casual = df_bike['casual'].sum()

    st.write("---")
    st.subheader("Informasi Metrik")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Penyewaan Sepeda", value=f"{total_rentals:,}")
    col2.metric(label="Pengguna Registered", value=f"{total_registered:,}")
    col3.metric(label="Pengguna Casual", value=f"{total_casual:,}")
    st.write("---")

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
