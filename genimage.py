import io
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# Konfigurasi Halaman Web
st.set_page_config(page_title="AI Generator Ilustrasi Edukasi", page_icon="🎨", layout="centered")

st.title("🎨 AI Generator Ilustrasi & Kartun Edukasi SD/MI")
st.caption("Buat gambar ilustrasi soal, kartun karakter, atau media pembelajaran menggunakan Gemini / Imagen API.")

# Sidebar untuk API Key
with st.sidebar:
    st.header("⚙️ Konfigurasi API")
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input("Gemini API Key", value=default_key, type="password", help="Masukkan API Key Google AI Studio Anda")
    
    st.markdown("---")
    st.markdown("### 💡 Tips Prompt:")
    st.markdown("- Gunakan deskripsi yang spesifik dan jelas.")
    st.markdown("- Contoh: *'Cute flat cartoon illustration of a school girl sweeping the floor'*")

# Form Input Pengguna
prompt_user = st.text_area(
    "Deskripsikan gambar ilustrasi yang ingin dibuat:", 
    placeholder="Contoh: Ilustrasi kartun anak perempuan mengenakan seragam sekolah sedang menyapu lantai kelas dengan ceria"
)

gaya_gambar = st.selectbox(
    "Pilih Gaya Visual", 
    [
        "Kartun Edukasi Anak (Flat Cartoon)", 
        "Ilustrasi Buku Cerita (Storybook Style)", 
        "Gaya Garis Hitam Putih (Black & White Line Art / Mewarnai)"
    ]
)

# Tombol Eksekusi
if st.button("🚀 Buat Ilustrasi Sekarang", type="primary", use_container_width=True):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key Anda terlebih dahulu pada panel samping.")
    elif not prompt_user:
        st.warning("Mohon deskripsikan gambar yang ingin Anda buat.")
    else:
        try:
            # Inisialisasi klien Google GenAI resmi (Versi terbaru)
            client = genai.Client(api_key=api_key)
            
            # Menyusun prompt lengkap
            full_prompt = f"{prompt_user}, style: {gaya_gambar}, high quality, bright colors, educational children illustration, clean background"
            
            with st.spinner("AI sedang melukis ilustrasi Anda... Mohon tunggu beberapa detik..."):
                
                # Memanggil model Imagen untuk generate gambar
                result = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=full_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        output_mime_type="image/jpeg",
                        aspect_ratio="1:1",
                    )
                )
                
                # Mengambil byte gambar dari respons
                for generated_image in result.generated_images:
                    image_bytes = generated_image.image.image_bytes
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    st.success("✨ Ilustrasi Berhasil Dibuat!")
                    st.image(image, caption=f"Hasil: {prompt_user}", use_container_width=True)
                    
                    st.download_button(
                        label="📥 Download Gambar (JPG)",
                        data=image_bytes,
                        file_name="ilustrasi_edukasi.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan saat membuat gambar: {str(err)}")
