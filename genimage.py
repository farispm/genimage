import io
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Konfigurasi Halaman Web
st.set_page_config(page_title="AI Generator Ilustrasi Edukasi", page_icon="🎨", layout="centered")

st.title("🎨 AI Generator Ilustrasi & Kartun Edukasi SD/MI")
st.caption("Buat gambar ilustrasi soal, kartun karakter, atau media pembelajaran secara instan.")

# Sidebar untuk API Key
with st.sidebar:
    st.header("⚙️ Konfigurasi API")
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input("Gemini / Imagen API Key", value=default_key, type="password")
    
    st.markdown("---")
    st.markdown("### 💡 Tips Prompt yang Baik:")
    st.markdown("- Gunakan gaya **'cute flat cartoon style for kids education'** agar cocok untuk anak SD/MI.")
    st.markdown("- Jelaskan objek secara spesifik (warna baju, ekspresi, aktivitas).")

# Form Input Pengguna
prompt_user = st.text_area(
    "Deskripsikan gambar ilustrasi yang ingin dibuat:", 
    placeholder="Contoh: Ilustrasi kartun anak perempuan mengenakan seragam merah putih sedang menyapu lantai kelas dengan ceria, gaya buku anak SD"
)

gaya_gambar = st.selectbox(
    "Pilih Gaya Visual", 
    [
        "Kartun Edukasi Anak (Flat Cartoon)", 
        "Ilustrasi Buku Cerita (Storybook Style)", 
        "Gaya Garis Hitam Putih (Black & White Line Art / Mewarnai)", 
        "Infografis / Diagram Sains Sederhana"
    ]
)

# Tombol Eksekusi
if st.button("🚀 Buat Ilustrasi Sekarang", type="primary", use_container_width=True):
    if not api_key:
        st.error("Silakan masukkan API Key Anda terlebih dahulu pada panel samping.")
    elif not prompt_user:
        st.warning("Mohon deskripsikan gambar yang ingin Anda buat.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Menyesuaikan prompt dengan gaya yang dipilih
            full_prompt = f"{prompt_user}, {gaya_gambar}, high quality, bright colors, educational children illustration, clean background"
            
            with st.spinner("AI sedang melukis ilustrasi Anda... Mohon tunggu beberapa detik..."):
                
                # CATATAN: Menggunakan model Imagen / GenAI yang mendukung image generation sesuai SDK terbaru
                # Contoh pemanggilan API Imagen Google:
                response = genai.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=full_prompt,
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                    aspect_ratio="1:1"
                )
                
                # Ambil data byte gambar dari hasil respons API
                for generated_image in response.generated_images:
                    image_bytes = generated_image.image.image_bytes
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    st.success("✨ Ilustrasi Berhasil Dibuat!")
                    st.image(image, caption=f"Hasil: {prompt_user}", use_container_width=True)
                    
                    # Tombol Download Hasil Gambar
                    st.download_button(
                        label="📥 Download Gambar (JPG)",
                        data=image_bytes,
                        file_name="ilustrasi_edukasi.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan saat membuat gambar: {str(err)}")
            st.info("Pastikan API Key yang Anda gunakan sudah mendukung akses layanan Imagen / Image Generation.")