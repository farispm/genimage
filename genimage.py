import io
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Gemini AI Image Generator", page_icon="🎨", layout="centered")

st.title("🎨 Generator Ilustrasi Edukasi AI")
st.caption("Buat gambar ilustrasi kartun anak sekolah dengan gaya kustom secara instan.")

# Sidebar untuk Konfigurasi API Key
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Gemini API Key", 
        value=default_key, 
        type="password", 
        help="Masukkan Gemini API Key Anda"
    )
    st.markdown("---")
    st.markdown("### 💡 Tips Prompt:")
    st.markdown("- Gunakan deskripsi yang jelas dan spesifik.")
    st.markdown("- Contoh gaya: *'Cute flat cartoon style illustration, bright colors, clean background'*")

# Form Input Pengguna
prompt_user = st.text_area(
    "Deskripsikan gambar yang ingin Anda buat:", 
    placeholder="Contoh: Seorang anak laki-laki mengenakan peci dan seragam sekolah sedang menyapu halaman rumah dengan ceria"
)

gaya_visual = st.selectbox(
    "Pilih Gaya Gambar",
    [
        "Kartun Flat Edukasi Anak (Flat Cartoon)",
        "Gaya Ilustrasi Buku Cerita (Storybook Style)",
        "Gaya Garis Hitam Putih / Lembar Mewarnai (Line Art)"
    ]
)

# Tombol Eksekusi Pembuatan Gambar
if st.button("🚀 Buat Gambar Sekarang", type="primary", use_container_width=True):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key Anda terlebih dahulu pada panel samping.")
    elif not prompt_user:
        st.warning("Mohon deskripsikan gambar yang ingin Anda buat.")
    else:
        try:
            # Inisialisasi Klien Google GenAI resmi
            client = genai.Client(api_key=api_key)
            
            # Menggabungkan deskripsi user dengan gaya pilihan
            full_prompt = f"{prompt_user}, style: {gaya_visual}, high quality, bright colors, educational children illustration, clean background"
            
            with st.spinner("AI sedang melukis gambar Anda... Mohon tunggu sebentar..."):
                
                # Memanggil model Gemini untuk generate gambar
                result = client.models.generate_images(
                    model='gemini-3.1-flash-lite-image',
                    prompt=full_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        output_mime_type="image/jpeg",
                        aspect_ratio="1:1",
                    )
                )
                
                # Menampilkan hasil gambar ke layar
                for generated_image in result.generated_images:
                    image_bytes = generated_image.image.image_bytes
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    st.success("✨ Gambar Berhasil Dibuat!")
                    st.image(image, caption=f"Hasil: {prompt_user}", use_container_width=True)
                    
                    # Tombol Unduh Gambar
                    st.download_button(
                        label="📥 Download Gambar (JPG)",
                        data=image_bytes,
                        file_name="ilustrasi_edukasi.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan saat membuat gambar: {str(err)}")
