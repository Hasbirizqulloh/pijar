# 💡 Pijar - Sistem Pembaca Gambar untuk Tunanetra

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/hasbiiii/pijar-app)

Repositori ini berisi kode sumber untuk proyek Capstone "Pijar", sebuah sistem berbasis web yang dirancang untuk membantu mobilitas mandiri penyandang tunanetra dengan menerjemahkan informasi visual dari lingkungan sekitar menjadi narasi suara.

## Deskripsi Singkat

Penyandang tunanetra menghadapi tantangan besar dalam beraktivitas di ruang publik. Ketidakmampuan mengenali rintangan visual seperti lubang, kendaraan parkir, atau perubahan jalur trotoar dapat meningkatkan risiko kecelakaan.

Pijar mengatasi masalah ini dengan memungkinkan pengguna mengunggah gambar lingkungan sekitar. Gambar tersebut diproses oleh **model deteksi objek (CNN/Keras)** untuk mengidentifikasi rintangan, kemudian hasilnya diubah menjadi narasi deskriptif oleh **model bahasa (GPT-2)**. Akhirnya, narasi ini diubah menjadi suara menggunakan teknologi **Text-to-Speech (TTS)**.

## Demo Aplikasi

Anda bisa mencoba aplikasi Pijar secara langsung melalui link Hugging Face Spaces berikut:

**[➡️ Klik di sini untuk mencoba demo aplikasi](https://huggingface.co/spaces/hasbiiii/pijar-app)**

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


## ## Menjalankan Proyek Secara Lokal

Jika Anda ingin menjalankan proyek ini di komputer Anda sendiri, ikuti langkah-langkah berikut:

1.  **Clone Repository**
    Pastikan Anda sudah menginstal Git dan Git LFS.
    ```bash
    # Clone repository dari github
    git clone https://github.com/Hasbirizqulloh/pijar.git
    ```
2. **Unduh Model**    
    Model CNN
   ```bash
    https://drive.google.com/file/d/1CDCki-yNoRNK1OOrHPoM8rKDkBw82cWg/view?usp=sharing
    ```
   Model GPT-2
    ```bash
    https://drive.google.com/drive/folders/1z22baBDyYZIo2ciyiE8ntm0_KXIwuCw1?usp=sharing
    ```

3.  **Masuk ke Direktori Proyek**
    ```bash
    cd inference
    ```

4.  **Install Dependensi**
    Disarankan untuk menggunakan virtual environment.
    ```bash
    # Buat virtual environment 
    python -m venv venv
    source venv/bin/activate  # Di Windows: venv\Scripts\activate

    # Install semua library yang dibutuhkan
    pip install -r requirements.txt
    ```
5. **Struktur Proyek**    
    Buat struktur proyek seperti ini

   ![image](https://github.com/user-attachments/assets/4dc14ea8-d5a5-4aa2-81bf-752adc67b701)
   
6.  **Jalankan Aplikasi**
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
