import gradio as gr
from PIL import Image
import numpy as np
from tensorflow import keras
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
from gtts import gTTS
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# === Load model deteksi objek ===
model_path_detection = "cnn_object_detection_v4.keras"  
model_detection = keras.models.load_model(model_path_detection)

# === Mapping kelas ===
class_mapping = {0 :'Ojol', 1:'Pedestrian Crossing', 2: 'car', 3: 'motorcycle', 4: 'bus', 5: 'pedestrian', 6: 'no_object'}

class_labels = list(class_mapping.values())

IMAGE_SIZE = 224
MAX_OBJECTS = 4


def load_and_preprocess_image(image_pil):
    img = np.array(image_pil)
    img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
    img = img / 255.0
    return img, img  # Return dua kali: resized & original (untuk visualisasi)


def predict_and_visualize(image_pil, model, class_labels, image_size=224, CONFIDENCE_THRESHOLD=0.01):
    img_resized, img_original = load_and_preprocess_image(image_pil)
    img_input = np.expand_dims(img_resized, axis=0)

    pred_bbox, pred_class = model.predict(img_input)
    pred_bbox = pred_bbox[0]
    pred_class = pred_class[0]

    pred_class_labels = np.argmax(pred_class, axis=-1)
    confidence_scores = np.max(pred_class, axis=-1)

    valid_bboxes = []
    valid_class_indices = []
    valid_confidences = []

    def bbox_area(bbox):
        xmin, ymin, xmax, ymax = bbox
        return max(0, xmax - xmin) * max(0, ymax - ymin)

    MIN_AREA_THRESHOLD = 0.015

    for bbox, cls_idx, conf in zip(pred_bbox, pred_class_labels, confidence_scores):
        area = bbox_area(bbox)
        if np.sum(bbox) > 0 and conf >= CONFIDENCE_THRESHOLD and area >= MIN_AREA_THRESHOLD:
            valid_bboxes.append(bbox)
            valid_class_indices.append(int(cls_idx))
            valid_confidences.append(conf)

    predicted_class_names = [class_mapping[i] for i in valid_class_indices]

    # Visualisasi
    fig = plt.figure(figsize=(img_original.shape[1] / 100, img_original.shape[0] / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img_original)

    for bbox, class_name, conf in zip(valid_bboxes, predicted_class_names, valid_confidences):
        xmin, ymin, xmax, ymax = bbox * image_size
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   edgecolor='red', facecolor='none', linewidth=2))
        ax.text(xmin, ymin - 5, f"{class_name} ({conf:.2f})", color='white', fontsize=10,
                bbox=dict(facecolor='red', alpha=0.7, boxstyle='round,pad=0.2'))

    ax.axis('off')
    canvas = FigureCanvas(fig)
    canvas.draw()
    image_array = np.frombuffer(canvas.buffer_rgba(), dtype='uint8')
    image_array = image_array.reshape(canvas.get_width_height()[::-1] + (4,))
    plt.close(fig)

    image_pil = Image.fromarray(image_array).convert("RGB")
    return image_pil, predicted_class_names



# === Load GPT-2 untuk narasi ===
model_text_path = "Gpt-2" 
tokenizer = GPT2Tokenizer.from_pretrained(model_text_path)
model_text = GPT2LMHeadModel.from_pretrained(model_text_path)


def generate_text(
    model,
    tokenizer,
    prompt,
    max_length=150,
    do_sample=True,
    temperature=1.0,
    top_k=50,
    top_p=0.95,
    num_return_sequences=1,
    repetition_penalty=1.0,
    eos_token_id=None
):
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

    outputs = generator(
        prompt,
        max_length=max_length,
        do_sample=do_sample,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        num_return_sequences=num_return_sequences,
        repetition_penalty=repetition_penalty,
        eos_token_id=eos_token_id,
    )

    return [out["generated_text"] for out in outputs]


    # === Fungsi Gradio utama yang telah dimodifikasi dengan TTS ===
def process_image(image):
    # Bagian ini tetap sama
    vis_image, hasil_kelas = predict_and_visualize(image, model_detection, class_labels)

    print("Kelas-kelas hasil deteksi:", hasil_kelas)

    # --- MODIFIKASI PADA KASUS 'TIDAK ADA DETEKSI' ---
    # Jika tidak ada objek, kita tetap harus mengembalikan 3 nilai agar Gradio tidak error.
    # Nilai ketiga (untuk audio) kita isi dengan None.
    if not hasil_kelas:
        narasi_kosong = "Tidak ada objek yang terdeteksi dengan jelas pada gambar ini."
        # --- BAGIAN BARU UNTUK TTS (KASUS KOSONG) ---
        audio_filepath = None
        try:
            tts = gTTS(text=narasi_kosong, lang='id')
            audio_filepath = "narasi_output.mp3"
            tts.save(audio_filepath)
        except Exception as e:
            print(f"Gagal membuat audio untuk narasi kosong: {e}")
        # -----------------------------------------------
        return vis_image, narasi_kosong, audio_filepath

    # Bagian ini tetap sama
    kelas_str = ', '.join(hasil_kelas)
    prompt = (
        f"{kelas_str}"
    )
    narasi = generate_text(
        model=model_text,
        tokenizer=tokenizer,
        prompt=prompt,
        max_length=50, # Saran: Naikkan max_length agar narasi tidak terpotong
        temperature=0.4,
        top_k=30,
        top_p=0.92,
        num_return_sequences=1,
        repetition_penalty=1.5,
        eos_token_id=tokenizer.eos_token_id
    )

    # Ambil teks narasi hasil generate
    narasi_final = narasi[0]

    # --- BAGIAN BARU UNTUK TTS (KASUS SUKSES) ---
    audio_filepath = None # Default value
    try:
        # Buat objek gTTS dari teks narasi yang sudah digenerate
        tts = gTTS(text=narasi_final, lang='id', slow=False)

        # Simpan file audio
        audio_filepath = "narasi_output.mp3"
        tts.save(audio_filepath)
    except Exception as e:
        print(f"Terjadi error saat membuat file audio TTS: {e}")
    # --- AKHIR BAGIAN BARU ---

    # --- MODIFIKASI PADA RETURN VALUE ---
    # Sekarang kita kembalikan 3 nilai: gambar, teks, dan path file audio
    return vis_image, narasi_final, audio_filepath

# Asumsi: Anda sudah memiliki fungsi 'process_image' dan 'gTTS' dari sebelumnya

# (Letakkan fungsi process_image Anda di sini)
# def process_image(image):
#     ...
#     return vis_image, narasi_final, audio_filepath

# === Desain UI Baru dengan Gradio Blocks ===

# Pilih tema yang Anda suka. 'Soft' terlihat modern dan bersih.
theme = gr.themes.Soft(
    primary_hue="neutral",
    secondary_hue="neutral",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    # Kustomisasi tambahan jika diperlukan
    button_primary_background_fill="#007aff",
    button_primary_background_fill_hover="#0056b3",
)


with gr.Blocks(theme=theme, title="Pijar") as demo:
    # Judul dengan Markdown untuk styling dan logo
    gr.Markdown(
        """
        # 💡 Pijar - Sistem Pembaca Gambar
        Unggah gambar kondisi trotoar atau jalan di sekitarmu. Sistem akan mendeteksi rintangan dan memberikan deskripsi dalam bentuk teks dan suara.
        """
    )

    # Membuat tata letak utama dengan dua kolom
    with gr.Row():
        # Kolom Kiri untuk Input
        with gr.Column(scale=1):
            input_image = gr.Image(type="pil", label="Unggah Gambar Anda")
            
            submit_btn = gr.Button("Analisis Gambar", variant="primary")

        # Kolom Kanan untuk Output
        with gr.Column(scale=1):
            output_image = gr.Image(label="Hasil Deteksi")
            narasi_box = gr.Textbox(label="Narasi Deskriptif", lines=4)
            audio_output = gr.Audio(label="Suara Narasi", autoplay=True)

    # Menghubungkan tombol 'submit' dengan fungsi process_image
    submit_btn.click(
        fn=process_image,
        inputs=input_image,
        outputs=[output_image, narasi_box, audio_output]
    )

# Jalankan interface
demo.launch()