import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur style untuk seaborn
sns.set(style='dark')

# Memuat dataset
def load_data():
    df_day = pd.read_csv('data/data_day.csv')
    df_hour = pd.read_csv('data/data_hour.csv')
    return df_day, df_hour

df_day, df_hour = load_data()

# Menyiapkan kolom 'date_day' untuk pengolahan data berdasarkan tanggal
def prepare_date_column(df):
    if 'date_day' in df.columns:
        df['date_day'] = pd.to_datetime(df['date_day'])
    elif {'year', 'month', 'day'}.issubset(df.columns):
        df['date_day'] = pd.to_datetime(df[['year', 'month', 'day']])
    else:
        st.error("Tidak ditemukan kolom 'date_day', atau kolom lain yang memungkinkan pembentukan tanggal.")
    return df

df_day = prepare_date_column(df_day)

# Menambahkan kolom 'user_id' jika tidak ada
if 'user_id' not in df_day.columns:
    df_day['user_id'] = range(1, len(df_day) + 1)

with st.sidebar:
    st.image("https://raw.githubusercontent.com/dailyrahmi/Proyek-Analisis-Data/main/assets/bike2.png")

# Sidebar untuk pemilihan periode waktu
st.sidebar.title('🗓️ Pilih Periode Waktu')
start_date = st.sidebar.date_input("Pilih Tanggal Mulai", pd.to_datetime('2011-01-01'))
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", pd.to_datetime('2012-12-31'))

# Menyaring dataset berdasarkan periode waktu yang dipilih
def filter_data_by_date(df, start_date, end_date):
    filtered_df = df[(df['date_day'] >= pd.to_datetime(start_date)) & (df['date_day'] <= pd.to_datetime(end_date))]
    return filtered_df

filtered_day_df = filter_data_by_date(df_day, start_date, end_date)

# Membuat judul utama halaman
st.title('Bike Sharing Analysis 🚴')

# Mengambil informasi terkait penyewaan sepeda berdasarkan tanggal yang dipilih
def get_rent_info(df):
    total_rentals = df['total_count'].sum()
    total_registered = df['registered'].sum()
    total_casual = df['casual'].sum()
    return total_rentals, total_registered, total_casual

total_rentals, total_registered, total_casual = get_rent_info(filtered_day_df)

# Menyusun tampilan metrik penyewaan sepeda dalam 3 kolom
col1, col2, col3 = st.columns(3)

# Menampilkan informasi metrik untuk total penyewaan, pengguna registered, dan casual
col1.metric(label="Total Penyewaan Sepeda", value=f"{total_rentals:,}")
col2.metric(label="Pengguna Registered", value=f"{total_registered:,}")
col3.metric(label="Pengguna Casual", value=f"{total_casual:,}")


# Membuat header untuk visualisasi penggunaan sepeda per jam
st.header('Distribusi Penggunaan Sepeda per Jam')

# Membuat visualisasi distribusi penyewaan sepeda berdasarkan jam
def plot_usage_by_hour(hour_df):
    plt.figure(figsize=(12, 6))
    sns.barplot(x='hr', y='total_count', data=hour_df, palette='coolwarm', ci=None)
    plt.title('Distribusi Jumlah Pengguna Sepeda per Jam', fontsize=16)
    plt.xlabel('Jam (dalam 24 jam)', fontsize=14)
    plt.ylabel('Jumlah Pengguna (per jam)', fontsize=14)
    plt.ylim(0, 500)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(plt)

plot_usage_by_hour(df_hour)

st.header('Perbandingan Pengguna Casual vs Registered')
def plot_user_type_comparison(df):
    total_users = df.groupby(by='year').agg({'registered': 'sum', 'casual': 'sum'}).reset_index()
    total_users = pd.melt(total_users, id_vars='year', value_vars=['registered', 'casual'], var_name='User Type', value_name='Count')

    plt.figure(figsize=(10, 6))
    sns.barplot(x='year', y='Count', hue='User Type', data=total_users, palette='pastel')
    plt.title('Total Pengguna Registered dan Casual per Tahun', fontsize=16)
    plt.xlabel('Tahun', fontsize=14)
    plt.ylabel('Jumlah Pengguna', fontsize=14)
    plt.legend(title='Tipe Pengguna')
    plt.grid(axis='y')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.tight_layout()
    st.pyplot(plt)

plot_user_type_comparison(df_day)

st.header('Trend Penyewaan Sepeda')
def plot_monthly_rentals(df):
    monthly_rentals = df.groupby(['year', 'month'])['total_count'].sum().reset_index()
    monthly_rentals['month'] = pd.Categorical(monthly_rentals['month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
    plt.figure(figsize=(10, 6))
    custom_palette = ['#ffd7d7', '#1f77b4']
    sns.lineplot(x='month', y='total_count', hue='year', data=monthly_rentals, marker='o', palette=custom_palette)
    plt.title('Jumlah Total Sepeda yang Disewakan Berdasarkan Bulan dan Tahun', fontsize=16)
    plt.xlabel('Bulan', fontsize=14)
    plt.ylabel('Jumlah Penyewaan', fontsize=14)
    plt.grid(True)
    plt.legend(title='Tahun', loc='upper right')
    plt.tight_layout()
    st.pyplot(plt)

plot_monthly_rentals(df_day)

st.header('Penyewaan Sepeda Berdasarkan Musim')
def plot_season_rentals(df):
    season_counts = df.groupby('season')['total_count'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    palette_colors = ['#ff6666', '#ff9999', '#ff9999', '#ff9999']
    bars = sns.barplot(x=season_counts.index, y=season_counts.values, palette=palette_colors, ax=ax)
    highest_season = season_counts.idxmax()
    for i, bar in enumerate(bars.patches):
        if season_counts.index[i] == highest_season:
            bar.set_facecolor('#ff4c4c')
    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
    ax.set_xlabel('Musim', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=14)
    y_ticks = ax.get_yticks().astype(int)
    ax.set_yticklabels([f'{int(y):,}' for y in y_ticks])
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

plot_season_rentals(df_day)

# Menambahkan catatan copyright di akhir halaman
st.caption('Copyright (c) RAHMI 2024')
