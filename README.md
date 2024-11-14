# TumbuhKuy: Platform AI Based on Binary Integer Programming dan Natural Language Processing sebagai Penanganan Stunting dan Optimalisasi Gizi di Indonesia​
​
Deskripsi Karya: TumbuhKuy adalah platform berbasis web yang menggunakan Artificial Intelligence (AI) untuk membantu pencegahan stunting dan optimasi gizi anak di Indonesia. Dengan memanfaatkan Natural Language Processing (NLP) dan Binary Integer Programming, platform ini mampu merekomendasikan bahan makanan yang sesuai kebutuhan gizi pengguna, menghasilkan resep makanan yang mudah diikuti, dan memberikan panduan gizi yang sesuai dengan anggaran serta kondisi kesehatan pengguna.

Tujuan Utama: Tujuan utama TumbuhKuy adalah menyediakan solusi praktis dan personal bagi keluarga dalam memenuhi kebutuhan gizi harian anak-anak. Platform ini juga bertujuan untuk mendukung pihak layanan kesehatan dalam melacak perkembangan kesehatan anak melalui data historis yang tersimpan, sehingga intervensi dapat dilakukan dengan lebih tepat waktu.

Permasalahan yang Diselesaikan: TumbuhKuy dirancang untuk mengatasi permasalahan gizi buruk dan stunting yang masih tinggi di Indonesia. Dengan menggabungkan AI berbasis NLP untuk menyajikan resep yang relevan serta Binary Integer Programming untuk optimasi bahan makanan sesuai anggaran, platform ini menawarkan solusi yang mampu menjawab kendala gizi keluarga, baik di wilayah terpencil maupun perkotaan, dengan rekomendasi gizi yang terjangkau dan terstruktur.

## Daftar Isi
- [Fitur](#fitur)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Struktur Repository](#sturktur-repository)

## Fitur

- **Fitur 1**: Analisis Gizi Personal
- **Fitur 2**: Pemberian Rekomendasi Bahan Makanan Optimal dengan Binary Integer Programming
- **Fitur 3**: Pilihan Bahan Makanan Manual dan Penghitungan Kecukupan Gizi​
- **Fitur 4**: Generasi Resep Otomatis Menggunakan Natural Language Processing​
- **Fitur 5**: Pemantauan Kesehatan dan Perkembangan​
- **Fitur 6**: Fitur Tracking Kesehatan oleh Layanan Kesehatan​
- **Fitur 7**: Chatbot AI untuk Edukasi dan Konsultasi Gizi​

## Instalasi

Langkah-langkah untuk menginstal dan menjalankan repository ini.

1. **Clone repository ini**:
    ```bash
    git clone https://github.com/MarcoAlandAdinanda/TumbuhKuy.git
    ```
2. **Masuk ke direktori proyek**:
    ```bash
    cd TumbuhKuy
    ```
3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Penggunaan

Untuk mulai menghubungkan code dengan website command berikut:

```bash
    flask run
```

Untuk mencoba running salah satu scripts dapat dengan command berikut:

```bash
    python scripts/SampleScript.py
```

## Stuktur Repository

- **api**: 
Berisi code untuk mengaktifkan API menggunakan framework flask, sehingga dapat terhubung dengan code frontend.
- **dataset**: 
Kumpulan dataset yang digunakan untuk menjalankan code pada direktori scripts.
- **scripts**: 
Berisi script python yang befungsi dalam sistem pemrosesan TumbuhKuy. Selain script, terdapat jupyter notebook mengenai contoh penggunaan dari masing-masing script.