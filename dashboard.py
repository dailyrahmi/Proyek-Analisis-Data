import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

# Menambahkan judul utama dan deskripsi aplikasi
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Dashboard Analisis Data Bike Sharing🚴</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Analisis data bike sharing untuk memahami pola penggunaan sepeda berdasarkan hari dan jam.</p>", unsafe_allow_html=True)
st.write("---")

# Memuat dataset pertama (bike sharing day)
df_bike = None
try:
    df_bike = pd.read_csv('Bike Sharing Dataset/day.csv')
    st.success("Dataset bike sharing day berhasil dimuat!")
except FileNotFoundError:
    st.error("Error memuat dataset bike sharing day: File tidak ditemukan. Pastikan file 'day.csv' berada di dalam folder 'Bike Sharing Dataset'.")
except Exception as e:
    st.error(f"Error memuat dataset bike sharing day: {e}")

# Memuat dataset kedua (bike sharing hour)
df_another = None
try:
    df_another = pd.read_csv('Bike Sharing Dataset/hour.csv')
    st.success("Dataset bike sharing hour berhasil dimuat!")
except FileNotFoundError:
    st.error("Error memuat dataset bike sharing hour: File tidak ditemukan. Pastikan file 'hour.csv' berada di dalam folder 'Bike Sharing Dataset'.")
except Exception as e:
    st.error(f"Error memuat dataset bike sharing hour: {e}")

# Sidebar untuk navigasi
with st.sidebar:
    if os.path.exists(image_path):
    st.image(image_path, use_column_width=True)
else:
    st.error("Gambar tidak ditemukan! Periksa path gambar di folder 'assets'.")
    st.header("Navigasi Data Bike Sharing")
    menu = st.radio("Pilih bagian:", ["Tampilkan Data", "Visualisasi Bike Sharing Day", "Visualisasi Bike Sharing Hour", "Analisis RFM", "Tentang Aplikasi"])

# Menampilkan informasi metrik pada halaman utama jika dataset tersedia
if df_bike is not None:
    total_rentals = int(df_bike['cnt'].sum())
    total_registered = int(df_bike['registered'].sum())
    total_casual = int(df_bike['casual'].sum())

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Penyewaan Sepeda", value=f"{total_rentals:,}")
    col2.metric(label="Pengguna Registered", value=f"{total_registered:,}")
    col3.metric(label="Pengguna Casual", value=f"{total_casual:,}")

# Menampilkan data berdasarkan pilihan pada sidebar
if menu == "Tampilkan Data":
    st.subheader("Dataset Bike Sharing Day")
    if df_bike is not None:
        st.write("Kolom yang tersedia:", df_bike.columns.tolist())
        if st.checkbox("Tampilkan 5 Data Teratas - Day"):
            st.dataframe(df_bike.head())

    st.subheader("Dataset Bike Sharing Hour")
    if df_another is not None:
        st.write("Kolom yang tersedia:", df_another.columns.tolist())
        if st.checkbox("Tampilkan 5 Data Teratas - Hour"):
            st.dataframe(df_another.head())

# Visualisasi untuk dataset bike sharing day
if menu == "Visualisasi Bike Sharing Day" and df_bike is not None:
    st.subheader("Visualisasi Data Bike Sharing Day")
    if 'season' in df_bike.columns:
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        sns.countplot(data=df_bike, x='season', palette="coolwarm", hue='season', legend=False)
        plt.title("Distribusi Penggunaan Sepeda Berdasarkan Musim", fontsize=16)
        plt.xlabel("Musim", fontsize=14)
        plt.ylabel("Jumlah Penggunaan", fontsize=14)
        st.pyplot(plt)
    else:
        st.error("Kolom 'season' tidak ditemukan pada dataset bike sharing day!")

# Visualisasi untuk dataset bike sharing hour
if menu == "Visualisasi Bike Sharing Hour" and df_another is not None:
    st.subheader("Visualisasi Data Bike Sharing Hour")
    column_name = st.selectbox("Pilih kolom untuk visualisasi:", options=df_another.columns, index=df_another.columns.get_loc("hr"))
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.countplot(data=df_another, x=column_name, palette="viridis", hue=column_name, legend=False)
    plt.title(f"Distribusi Penggunaan Sepeda Berdasarkan {column_name.capitalize()}", fontsize=16)
    plt.xlabel(column_name.capitalize(), fontsize=14)
    plt.ylabel("Jumlah Penggunaan", fontsize=14)
    st.pyplot(plt)

# Menambahkan analisis RFM jika dataset berhasil dimuat
if menu == "Analisis RFM":
    st.subheader("Analisis RFM")
    st.markdown("""
    Analisis RFM (Recency, Frequency, Monetary) bertujuan untuk mengelompokkan pelanggan berdasarkan perilaku peminjaman mereka.
    """)

    if df_bike is not None:
        # Contoh data untuk analisis RFM
        data = {
            'customer_id': [1, 2, 1, 3, 2, 1, 3, 3],
            'transaction_date': [
                '2024-01-01', '2024-01-05', '2024-02-01', 
                '2024-02-15', '2024-03-01', '2024-03-10', 
                '2024-03-20', '2024-03-25'
            ],
            'amount': [10, 20, 15, 10, 25, 30, 5, 20]
        }
        df = pd.DataFrame(data)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        analysis_date = dt.datetime.now()
        rfm_df = df.groupby('customer_id').agg({
            'transaction_date': lambda x: (analysis_date - x.max()).days,
            'amount': ['count', 'sum']
        }).reset_index()
        rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        st.dataframe(rfm_df)
    else:
        st.error("Dataset tidak tersedia untuk analisis RFM!")
