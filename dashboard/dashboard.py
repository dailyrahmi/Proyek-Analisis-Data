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
all_data_day = None
try:
    all_data_day = pd.read_csv('data/day.csv')
    st.success("Dataset bike sharing day berhasil dimuat!")
except FileNotFoundError:
    st.error("Error memuat dataset bike sharing day: File tidak ditemukan. Pastikan file 'day.csv' berada di dalam folder 'Bike Sharing Dataset'.")
except Exception as e:
    st.error(f"Error memuat dataset bike sharing day: {e}")

# Memuat dataset kedua (bike sharing hour)
all_data_hour = None
try:
    all_data_hour = pd.read_csv('data/hour.csv')
    st.success("Dataset bike sharing hour berhasil dimuat!")
except FileNotFoundError:
    st.error("Error memuat dataset bike sharing hour: File tidak ditemukan. Pastikan file 'hour.csv' berada di dalam folder 'Bike Sharing Dataset'.")
except Exception as e:
    st.error(f"Error memuat dataset bike sharing hour: {e}")

# Sidebar untuk navigasi
st.sidebar.header("Navigasi Data Bike Sharing")
menu = st.sidebar.radio("Pilih bagian:", ["Tampilkan Data", "Visualisasi Bike Sharing Day", "Visualisasi Bike Sharing Hour", "Analisis RFM", "Tentang Aplikasi"])

# Menampilkan data berdasarkan pilihan pada sidebar
if menu == "Tampilkan Data":
    # Menampilkan dataset bike sharing day
    st.subheader("Dataset Bike Sharing Day")
    if all_data_day is not None:
        st.write("Kolom yang tersedia:", all_data_day.columns.tolist())
        if st.checkbox("Tampilkan 5 Data Teratas - Day"):
            st.dataframe(all_data_day.head())
    else:
        st.error("Dataset bike sharing day tidak tersedia!")

    # Menampilkan dataset bike sharing hour
    st.subheader("Dataset Bike Sharing Hour")
    if all_data_hour is not None:
        st.write("Kolom yang tersedia:", all_data_hour.columns.tolist())
        if st.checkbox("Tampilkan 5 Data Teratas - Hour"):
            st.dataframe(all_data_hour.head())
    else:
        st.error("Dataset bike sharing hour tidak tersedia!")

# Visualisasi untuk dataset bike sharing day
if menu == "Visualisasi Bike Sharing Day" and all_data_day is not None:
    st.subheader("Visualisasi Data Bike Sharing Day")
    
    # Visualisasi jumlah peminjaman berdasarkan hari dalam minggu
    if 'weekday' in all_data_day.columns:
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        sns.barplot(x='weekday', y='cnt', data=all_data_day, palette="viridis")
        plt.title("Jumlah Peminjaman Sepeda Berdasarkan Hari dalam Minggu", fontsize=16)
        plt.xlabel("Hari dalam Minggu", fontsize=14)
        plt.ylabel("Jumlah Peminjaman", fontsize=14)
        plt.xticks(rotation=45)
        st.pyplot(plt)
        st.markdown("""Dari visualisasi ini, kita dapat melihat tren penggunaan sepeda berdasarkan hari. 
        Jumlah peminjaman sepeda cenderung lebih tinggi pada akhir pekan, yang menunjukkan peningkatan aktivitas rekreasi pada hari tersebut.""")
    else:
        st.error("Kolom 'weekday' tidak ditemukan pada dataset bike sharing day!")

    # Visualisasi distribusi penggunaan berdasarkan musim
    if 'season' in all_data_day.columns:
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        sns.countplot(x='season', data=all_data_day, palette="coolwarm")
        plt.title("Distribusi Penggunaan Sepeda Berdasarkan Musim", fontsize=16)
        plt.xlabel("Musim", fontsize=14)
        plt.ylabel("Jumlah Peminjaman", fontsize=14)
        st.pyplot(plt)
        st.markdown("""Visualisasi ini menunjukkan distribusi penggunaan sepeda berdasarkan musim. 
        Penggunaan sepeda cenderung lebih tinggi pada musim panas, sementara pada musim dingin menurun.""")
    else:
        st.error("Kolom 'season' tidak ditemukan pada dataset bike sharing day!")

# Visualisasi untuk dataset bike sharing hour
if menu == "Visualisasi Bike Sharing Hour" and all_data_hour is not None:
    st.subheader("Visualisasi Data Bike Sharing Hour")
    st.write("Kolom yang tersedia pada dataset kedua:", all_data_hour.columns.tolist())
    column_name = st.selectbox("Pilih kolom untuk visualisasi:", options=all_data_hour.columns, index=all_data_hour.columns.get_loc("hr"))  # Pilih kolom 'hr' secara default
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.countplot(data=all_data_hour, x=column_name, palette="viridis")
    plt.title(f"Distribusi Penggunaan Sepeda Berdasarkan {column_name.capitalize()}", fontsize=16)
    plt.xlabel(column_name.capitalize(), fontsize=14)
    plt.ylabel("Jumlah Penggunaan", fontsize=14)
    st.pyplot(plt)
    st.markdown(f"""Visualisasi ini menunjukkan distribusi penggunaan sepeda berdasarkan {column_name}. 
    Anda dapat melihat pola penggunaan sepeda pada jam-jam tertentu. 
    Misalnya, penggunaan sepeda cenderung meningkat pada jam-jam sibuk, 
    yang menunjukkan bahwa sepeda sering digunakan untuk perjalanan kerja dan kegiatan lainnya.""")

# Menambahkan analisis RFM jika dataset berhasil dimuat
if menu == "Analisis RFM":
    st.subheader("Analisis RFM")
    st.markdown("""Analisis RFM (Recency, Frequency, Monetary) bertujuan untuk mengelompokkan pelanggan berdasarkan perilaku peminjaman mereka.
    - **Recency:** Menghitung jumlah hari sejak terakhir kali pelanggan melakukan peminjaman.
    - **Frequency:** Menghitung jumlah total peminjaman yang dilakukan oleh pelanggan dalam periode tertentu.
    - **Monetary:** Menghitung total pengeluaran pelanggan dalam periode tersebut.""")

    # RFM analysis code (gunakan sample data untuk testing jika dataset tidak tersedia)
    if all_data_day is not None:
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
        st.write("Segmentasi Pelanggan Berdasarkan Skor RFM:")
        st.dataframe(rfm_df[['customer_id', 'RFM_Segment']])

# Menampilkan data berdasarkan pilihan pada sidebar
if menu == "Analisis RFM":
    st.subheader("Analisis RFM")
    st.markdown("""Analisis RFM (Recency, Frequency, Monetary) bertujuan untuk mengelompokkan pelanggan berdasarkan perilaku peminjaman mereka.""")

    # Menghitung metrik RFM
    if all_data_day is not None:
        all_data_day['date_day'] = pd.to_datetime(all_data_day['date_day'])  # Pastikan 'date_day' dalam format datetime
        tanggal_referensi = all_data_day['date_day'].max()
        all_data_day['Rentang_Hari'] = (tanggal_referensi - all_data_day['date_day']).dt.days

        # Menghitung Frequency
        frekuensi_penggunaan = all_data_day.groupby('date_day')['total_count'].sum().reset_index()
        frekuensi_penggunaan.columns = ['date_day', 'Frekuensi']

        # Menghitung Monetary
        moneter_pengguna = all_data_day.groupby('date_day')['registered'].sum().reset_index()
        moneter_pengguna.columns = ['date_day', 'Nilai_Moneter']

        # Menggabungkan ketiga metrik RFM menjadi satu DataFrame
        rfm_df = all_data_day[['date_day', 'Rentang_Hari']].merge(frekuensi_penggunaan, on='date_day', how='left').merge(moneter_pengguna, on='date_day', how='left')

        # Visualisasi Hari Terbaik Berdasarkan Metrik RFM
        fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

        # Menentukan warna untuk grafik batang
        warna = ["#72BCD4"] * 5  # Warna yang digunakan untuk semua batang

        # Membuat plot untuk Recency
        sns.barplot(y="Rentang_Hari", x="date_day", data=rfm_df.sort_values(by="Rentang_Hari").head(5), palette=warna, ax=ax[0])
        ax[0].set_ylabel(None)
        ax[0].set_xlabel(None)
        ax[0].set_title("Recency (dalam hari)", loc="center", fontsize=18)
        ax[0].tick_params(axis='x', labelsize=15)

        # Membuat plot untuk Frequency
        sns.barplot(y="Frekuensi", x="date_day", data=rfm_df.sort_values(by="Frekuensi", ascending=False).head(5), palette=warna, ax=ax[1])
        ax[1].set_ylabel(None)
        ax[1].set_xlabel(None)
        ax[1].set_title("Frekuensi Peminjaman", loc="center", fontsize=18)
        ax[1].tick_params(axis='x', labelsize=15)

        # Membuat plot untuk Monetary
        sns.barplot(y="Nilai_Moneter", x="date_day", data=rfm_df.sort_values(by="Nilai_Moneter", ascending=False).head(5), palette=warna, ax=ax[2])
        ax[2].set_ylabel(None)
        ax[2].set_xlabel(None)
        ax[2].set_title("Nilai Moneter", loc="center", fontsize=18)
        ax[2].tick_params(axis='x', labelsize=15)

        # Menambahkan judul utama untuk keseluruhan grafik
        plt.suptitle("Analisis Hari Terbaik Berdasarkan Metrik RFM (tanggal)", fontsize=20)

        # Menampilkan grafik di Streamlit
        st.pyplot(fig)

        # Menambahkan penjelasan tentang analisis RFM
        st.markdown("""Visualisasi ini menunjukkan analisis RFM berdasarkan hari. 
        - **Recency:** Menunjukkan berapa hari yang telah berlalu sejak peminjaman terakhir.
        - **Frekuensi:** Jumlah total peminjaman yang dilakukan.
        - **Nilai Moneter:** Total nilai dari peminjaman yang dilakukan oleh pengguna pada hari tertentu.""")

# Tentang aplikasi
if menu == "Tentang Aplikasi":
    st.subheader("Tentang Aplikasi")
    st.markdown("""Aplikasi ini dirancang untuk memberikan analisis mendalam tentang penggunaan sepeda berdasarkan dataset bike sharing. 
    Melalui analisis ini, pengguna dapat memahami pola peminjaman sepeda dan faktor-faktor yang mempengaruhi keputusan peminjaman.
    - Dataset yang digunakan: `day.csv` dan `hour.csv`
    - Menggunakan Streamlit untuk antarmuka interaktif.
    - Kembangkan analisis dan visualisasi sesuai kebutuhan.""")

# Menambahkan footer
st.markdown("---")
st.markdown("<footer style='text-align: center;'><small>© 2024 Dashboard Analisis Data Bike Sharing. Semua hak dilindungi.</small></footer>", unsafe_allow_html=True)
