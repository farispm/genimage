import io
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="AI Generator Kartun Edukasi", page_icon="🎨", layout="centered")

st.title("🎨 Generator Ilustrasi Kartun Edukasi AI")
st.caption("Buat gambar ilustrasi dengan gaya konsisten menggunakan model 3.5 Flash Lite.")

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
if st.button("🚀 Buat Gambar Sesuai Gaya Rujukan", type="primary", use_container_width=True):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key Anda terlebih dahulu pada panel samping.")
    elif not prompt_user:
        st.warning("Mohon deskripsikan gambar yang ingin Anda buat.")
    else:
        try:
            # Inisialisasi Klien Google GenAI resmi
            client = genai.Client(api_key=api_key)
            
            # Memasukkan panduan gaya rujukan secara otomatis ke dalam prompt
            style_reference = (
                "Consistent style matching an educational children's book illustration: "
                "clean 2D flat cartoon vector style, friendly characters with clear outlines, "
                "bright and cheerful colors, soft lighting, clean background, simple details, "
                "suitable for elementary school education."
            )
            
            full_prompt = f"{prompt_user}. Style details: {style_reference}"
            
            with st.spinner("AI sedang melukis gambar menggunakan model 3.5 Flash Lite... Mohon tunggu sebentar..."):
                
                # Memanggil model 3.5 flash lite untuk generate gambar
                result = client.models.generate_images(
                    model='gemini-3.5-flash-lite',
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
                    
                    st.success("✨ Ilustrasi Berhasil Dibuat!")
                    st.image(image, caption=f"Hasil: {prompt_user}", use_container_width=True)
                    
                    # Tombol Unduh Gambar
                    st.download_button(
                        label="📥 Download Gambar (JPG)",
                        data=image_bytes,
                        file_name="ilustrasi_gaya_rujukan.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan saat membuat gambar: {str(err)}")
