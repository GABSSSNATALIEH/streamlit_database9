import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler


# Load data dari file Excel
file_excel = 'data_iq.xlsx'  
data = pd.read_excel(file_excel)

# Periksa nama kolom
print("Nama Kolom:", data.columns)

# Bersihkan nama kolom jika ada spasi
data.columns = data.columns.str.strip()

# Isi ulang nilai NaN hanya pada kolom numerik
data.fillna(data.select_dtypes(include=[np.number]).mean(), inplace=True)

# Pastikan kolom 'Skor Mentah' ada dan gunakan nama kolom yang sesuai
if 'Skor Mentah' in data.columns:
    # Menstandarisasi skor mentah
    standarisasi = StandardScaler()
    data['Skor_Mentah_Standar'] = standarisasi.fit_transform(data[['Skor Mentah']])

    # Hitung Nilai IQ
    data['Nilai_IQ'] = (data['Skor_Mentah_Standar'] * 15) + 100

    # Tambahkan kolom keterangan berdasarkan nilai IQ
    def keterangan_iq(iq):
        if iq >= 110:
            return 'Di Atas Rata-Rata'
        elif iq >= 92:
            return 'Rata-Rata'
        elif iq >= 56:
            return 'Di Bawah Rata-Rata'
        else:
            return 'Defisiensi'

    data['Keterangan'] = data['Nilai_IQ'].apply(keterangan_iq)

    # Tentukan Outcome berdasarkan nilai IQ
    data['Outcome'] = data['Nilai_IQ'] >= 100

    # Simpan hasil ke file Excel baru
    output_file = 'hasil_iq.xlsx'
    data.to_excel(output_file, index=False)

    print(f"Proses selesai. Data hasil disimpan ke {output_file}")

    # Simpan model standarisasi ke file pickle
    pickle.dump(standarisasi, open('scaler_iq.sav', 'wb'))
else:
    print("Kolom 'Skor Mentah' tidak ditemukan dalam data. Periksa file Excel Anda.")