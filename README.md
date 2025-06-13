# 💡 Pijar - Sistem Pembaca Gambar untuk Tunanetra

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/[NAMA-ANDA]/[NAMA-SPACE-ANDA])

Repositori ini berisi kode sumber untuk proyek Capstone "Pijar", sebuah sistem berbasis web yang dirancang untuk membantu mobilitas mandiri penyandang tunanetra dengan menerjemahkan informasi visual dari lingkungan sekitar menjadi narasi suara.

## Deskripsi Singkat

Penyandang tunanetra menghadapi tantangan besar dalam beraktivitas di ruang publik. Ketidakmampuan mengenali rintangan visual seperti lubang, kendaraan parkir, atau perubahan jalur trotoar dapat meningkatkan risiko kecelakaan.

Pijar mengatasi masalah ini dengan memungkinkan pengguna mengunggah gambar lingkungan sekitar. Gambar tersebut diproses oleh **model deteksi objek (CNN/Keras)** untuk mengidentifikasi rintangan, kemudian hasilnya diubah menjadi narasi deskriptif oleh **model bahasa (GPT-2)**. Akhirnya, narasi ini diubah menjadi suara menggunakan teknologi **Text-to-Speech (TTS)**.

## Demo Aplikasi

Anda bisa mencoba aplikasi Pijar secara langsung melalui link Hugging Face Spaces berikut:

**[➡️ Klik di sini untuk mencoba demo aplikasi](https://huggingface.co/spaces/[NAMA-ANDA]/[NAMA-SPACE-ANDA])**

*(Harap ganti `[NAMA-ANDA]` dan `[NAMA-SPACE-ANDA]` dengan URL Space Anda yang sebenarnya)*

## Fitur Utama

-   **Deteksi Objek**: Mengidentifikasi berbagai objek rintangan yang umum ditemukan di jalan atau trotoar.
-   **Generasi Narasi Dinamis**: Membuat deskripsi dalam bahasa natural berdasarkan objek yang terdeteksi menggunakan GPT-2.
-   **Konversi Teks ke Suara (TTS)**: Menyediakan output audio dalam Bahasa Indonesia agar mudah diakses.
-   **Antarmuka Web Interaktif**: UI yang sederhana dan mudah digunakan dibangun dengan Gradio.

## Teknologi yang Digunakan

-   **Bahasa**: Python 3
-   **Frameworks & Libraries**:
    -   `Gradio`: Untuk membangun antarmuka web.
    -   `TensorFlow` & `Keras`: Untuk memuat dan menjalankan model deteksi objek (`.keras`).
    -   `Transformers`: Untuk memuat dan menjalankan model bahasa GPT-2.
    -   `gTTS`: Untuk fungsionalitas Text-to-Speech.
    -   `Pillow` & `OpenCV`: Untuk pemrosesan gambar.
-   **Platform Deployment**: Hugging Face Spaces
-   **Manajemen File Besar**: Git LFS

## Struktur Proyek

## ## Menjalankan Proyek Secara Lokal

Jika Anda ingin menjalankan proyek ini di komputer Anda sendiri, ikuti langkah-langkah berikut:

1.  **Clone Repository**
    Pastikan Anda sudah menginstal Git dan Git LFS.
    ```bash
    # Clone repository dari Hugging Face Spaces
    git clone [https://huggingface.co/spaces/](https://huggingface.co/spaces/)[NAMA-ANDA]/[NAMA-SPACE-ANDA]
    ```

2.  **Masuk ke Direktori Proyek**
    ```bash
    cd [NAMA-SPACE-ANDA]
    ```

3.  **Unduh File Model (Git LFS)**
    Perintah ini akan mengunduh file-file besar seperti `.keras` dan `.bin` yang dilacak oleh LFS.
    ```bash
    git lfs pull
    ```

4.  **Install Dependensi**
    Disarankan untuk menggunakan virtual environment.
    ```bash
    # Buat virtual environment (opsional tapi direkomendasikan)
    python -m venv venv
    source venv/bin/activate  # Di Windows: venv\Scripts\activate

    # Install semua library yang dibutuhkan
    pip install -r requirements.txt
    ```

5.  **Jalankan Aplikasi**
    ```bash
    python app.py
    ```
    Aplikasi akan berjalan dan memberikan URL lokal (biasanya `http://127.0.0.1:7860`) yang bisa Anda buka di browser.

## Cara Menggunakan Aplikasi

1.  Buka link demo aplikasi.
2.  Unggah gambar lingkungan (trotoar, jalan, dll.) melalui area "Unggah Gambar Anda".
3.  Klik tombol **"Analisis Gambar"**.
4.  Tunggu beberapa saat hingga proses selesai.
5.  Hasil deteksi visual, narasi deskriptif, dan suara narasi akan muncul di kolom sebelah kanan.

---
