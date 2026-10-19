import io
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Gemini Direct Image Generator", page_icon="🎨", layout="centered")

st.title("🎨 Generator Ilustrasi Langsung dari Gemini AI")
st.caption("Membuat gambar secara resmi menggunakan model Image Generation dari Google Gemini.")

# Sidebar untuk Konfigurasi API Key
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Gemini API Key", 
        value=default_key, 
        type="password", 
        help="Masukkan API Key Google AI Studio Anda"
    )
    st.markdown("---")
    st.markdown("### 💡 Panduan Gaya Rujukan:")
    st.markdown("- Ilustrasi datar 2D yang bersih (*clean 2D flat cartoon*).")
    st.markdown("- Watak kanak-kanak sekolah dengan ekspresi ceria.")
    st.markdown("- Warna cerah, latar belakang alam/sekolah yang rapi.")

# Form Input Pengguna
prompt_user = st.text_area(
    "Deskripsikan adegan gambar yang ingin dibuat:", 
    placeholder="Contoh: Anak laki-laki mengenakan peci dan seragam sekolah sedang menyapu halaman rumah"
)

# Tombol Eksekusi Pembuatan Gambar
if st.button("🚀 Buat Gambar Langsung dari Gemini", type="primary", use_container_width=True):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key Anda terlebih dahulu pada panel samping.")
    elif not prompt_user:
        st.warning("Mohon deskripsikan gambar yang ingin Anda buat.")
    else:
        try:
            # Inisialisasi klien Google GenAI resmi
            client = genai.Client(api_key=api_key)
            
            style_reference = (
                "Consistent style matching an educational children's book illustration: "
                "clean 2D flat cartoon vector style, friendly characters with clear outlines, "
                "bright and cheerful colors, soft lighting, clean background, simple details, "
                "suitable for elementary school education."
            )
            
            full_prompt = f"{prompt_user}. Style details: {style_reference}"
            
            with st.spinner("Gemini sedang melukis gambar secara langsung... Mohon tunggu sebentar..."):
                
                # Memanggil model pembuat gambar resmi Google (Imagen / GenAI Image Model)
                response = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=full_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        output_mime_type="image/jpeg",
                        aspect_ratio="1:1",
                    )
                )
                
                # Mengambil byte gambar dari respons resmi Gemini
                for generated_image in response.generated_images:
                    image_bytes = generated_image.image.image_bytes
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    st.success("✨ Ilustrasi Berhasil Dibuat Langsung oleh Gemini!")
                    st.image(image, caption=f"Hasil: {prompt_user}", use_container_width=True)
                    
                    # Tombol Unduh Gambar
                    st.download_button(
                        label="📥 Download Gambar (JPG)",
                        data=image_bytes,
                        file_name="ilustrasi_gemini.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan pada sistem Gemini: {str(err)}")
            st.info("Pastikan API Key Anda memiliki kuota atau izin akses untuk layanan pembuat gambar (Imagen/GenAI Image).")
