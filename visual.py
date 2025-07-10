import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import re
import folium # Import Folium

st.header("DATATHON - VISTARA")
st.title("Peta Lokasi Rumah Sakit dan Kecelakaan di Yogyakarta")

# Pastikan file CSV tersedia di direktori yang sama atau berikan path lengkap
df_hospital = pd.read_csv('rumah_sakit_yogyakarta.csv')
df_kecelakaan = pd.read_csv('kecelakaan-with-location-geoencoded.csv')

YOGYA_LAT = -7.7956
YOGYA_LON = 110.3695

# --- Fungsi untuk mengekstrak koordinat atau menggunakan default ---
def extract_coordinates(coord_str):
    if pd.isna(coord_str) or str(coord_str).strip() == "":
        return YOGYA_LAT, YOGYA_LON
    
    match = re.search(r'\(?([-+]?\d+\.?\d*),\s*([-+]?\d+\.?\d*)\)?', str(coord_str))
    if match:
        try:
            lat = float(match.group(1))
            lon = float(match.group(2))
            return lat, lon
        except ValueError:
            return YOGYA_LAT, YOGYA_LON
    return YOGYA_LAT, YOGYA_LON

# --- Proses df_kecelakaan untuk mendapatkan latitude dan longitude ---
df_kecelakaan['created_at'] = pd.to_datetime(df_kecelakaan['created_at'], format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')
df_kecelakaan.dropna(subset=['created_at'], inplace=True)
df_kecelakaan[['latitude', 'longitude']] = df_kecelakaan['coordinates'].apply(lambda x: pd.Series(extract_coordinates(x)))

# --- Tampilan Streamlit dengan tab baru ---
with st.expander("📉 Visualisasi Data"):
    tabs = st.tabs(["Data Rumah Sakit", "Data Kecelakaan", "Data Ambulance", "Peta Gabungan Interaktif"])

    with tabs[0]: # Tab "Data Rumah Sakit" menggunakan Folium
        st.subheader("Lokasi Rumah Sakit (Peta Interaktif)")
        jumlah_rumah_sakit = st.number_input("Jumlah Rumah Sakit yang Ditampilkan:", min_value=1, max_value=len(df_hospital), value=len(df_hospital), key='num_rs_tab0')

        st.dataframe(df_hospital.head(jumlah_rumah_sakit), hide_index=True)

        # Inisialisasi peta Folium untuk Rumah Sakit
        m_hospital = folium.Map(location=[YOGYA_LAT, YOGYA_LON], zoom_start=12)

        # Tambahkan marker untuk Rumah Sakit
        for index, row in df_hospital.head(jumlah_rumah_sakit).iterrows():
            if pd.notna(row['latitude']) and pd.notna(row['longitude']):
                popup_text = f"<b>{row.get('nama_rs', 'Rumah Sakit')}</b><br>" \
                             f"Alamat: {row.get('alamat', 'Tidak diketahui')}"
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=popup_text,
                    icon=folium.Icon(color='blue', icon='hospital', prefix='fa') # Icon Rumah Sakit
                ).add_to(m_hospital)
        
        # Tampilkan peta Folium di Streamlit
        st.components.v1.html(folium.Figure().add_child(m_hospital).render(), height=500)
        st.write("Catatan: Titik **biru** menunjukkan lokasi Rumah Sakit. Klik pada titik untuk melihat detail.")

    with tabs[1]: # Tab "Data Kecelakaan" sekarang menggunakan Folium
        st.subheader("Data Kecelakaan")
        df_kecelakaan['bulan'] = df_kecelakaan['created_at'].dt.strftime('%Y-%m')
        df_hanya_kecelakaan = df_kecelakaan.copy()

        kecelakaan_per_bulan = df_hanya_kecelakaan['bulan'].value_counts().sort_index()
        kecelakaan_df = kecelakaan_per_bulan.reset_index()
        kecelakaan_df.columns = ['Bulan', 'Jumlah Kecelakaan']

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Bulan', y='Jumlah Kecelakaan', data=kecelakaan_df, palette='viridis', ax=ax)
        ax.set_title('Jumlah Kecelakaan per Bulan')
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Jumlah Kecelakaan')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
        
        st.subheader("Peta Lokasi Kecelakaan (Peta Interaktif)")
        # Inisialisasi peta Folium untuk Kecelakaan
        m_kecelakaan = folium.Map(location=[YOGYA_LAT, YOGYA_LON], zoom_start=12)

        # Tambahkan marker untuk Kecelakaan
        for index, row in df_kecelakaan.iterrows():
            if pd.notna(row['latitude']) and pd.notna(row['longitude']):
                popup_text = f"<b>Kecelakaan</b><br>" \
                             f"Waktu: {row['created_at'].strftime('%Y-%m-%d %H:%M')}<br>" \
                             f"Deskripsi: {row.get('text', 'Tidak ada deskripsi')[:100]}..." # Ambil 100 karakter pertama
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=popup_text,
                    icon=folium.Icon(color='red', icon='car', prefix='fa') # Icon Mobil/Kecelakaan
                ).add_to(m_kecelakaan)
        
        # Tampilkan peta Folium di Streamlit
        st.components.v1.html(folium.Figure().add_child(m_kecelakaan).render(), height=500)
        st.write("Catatan: Titik **merah** menunjukkan lokasi Kecelakaan. Klik pada titik untuk melihat detail.")


    with tabs[2]:
        st.subheader("Data Ambulance")
        st.write("Konten untuk Data Ambulance akan ditempatkan di sini.")

    with tabs[3]: # Tab untuk peta gabungan interaktif (tetap menggunakan Folium)
        st.subheader("Peta Gabungan Lokasi Rumah Sakit (Biru) dan Kecelakaan (Merah)")

        # Inisialisasi peta Folium di tengah Yogyakarta
        m_combined = folium.Map(location=[YOGYA_LAT, YOGYA_LON], zoom_start=12)

        # Tambahkan marker untuk Rumah Sakit
        for index, row in df_hospital.iterrows():
            if pd.notna(row['latitude']) and pd.notna(row['longitude']):
                popup_text = f"<b>{row.get('nama_rs', 'Rumah Sakit')}</b><br>" \
                             f"Alamat: {row.get('alamat', 'Tidak diketahui')}"
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=popup_text,
                    icon=folium.Icon(color='blue', icon='hospital', prefix='fa')
                ).add_to(m_combined)
        
        # Tambahkan marker untuk Kecelakaan
        for index, row in df_kecelakaan.iterrows():
            if pd.notna(row['latitude']) and pd.notna(row['longitude']):
                popup_text = f"<b>Kecelakaan</b><br>" \
                             f"Waktu: {row['created_at'].strftime('%Y-%m-%d %H:%M')}<br>" \
                             f"Deskripsi: {row.get('text', 'Tidak ada deskripsi')[:100]}..."
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=popup_text,
                    icon=folium.Icon(color='red', icon='car', prefix='fa')
                ).add_to(m_combined)

        # Tampilkan peta Folium di Streamlit
        st.components.v1.html(folium.Figure().add_child(m_combined).render(), height=500)
        st.write("Catatan: Titik **biru** menunjukkan Rumah Sakit dan titik **merah** menunjukkan lokasi Kecelakaan. Klik pada titik untuk melihat detail lebih lanjut.")