import io
import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
import urllib.parse

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="AI Generator Kartun Edukasi", page_icon="🎨", layout="centered")

st.title("🎨 Generator Ilustrasi Kartun Edukasi AI")
st.caption("Memanfaatkan Gemini Flash-Lite untuk konsep & render ilustrasi bersih tanpa watermark.")

# Sidebar untuk Konfigurasi API Key
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Gemini API Key", 
        value=default_key, 
        type="password", 
        help="Masukkan API Key Google Gemini Anda"
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
            # 1. Menggunakan Gemini Flash-Lite untuk menyempurnakan prompt sesuai rujukan
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.5-flash-lite")
            
            style_reference = (
                "Consistent style matching an educational children's book illustration: "
                "clean 2D flat cartoon vector style, friendly characters with clear outlines, "
                "bright and cheerful colors, soft lighting, clean background, simple details, "
                "suitable for elementary school education."
            )
            
            prompt_system = f"Terjemahkan dan perkaya deskripsi berikut ke dalam bahasa Inggris yang sangat detail untuk konsep gambar ilustrasi:\n'{prompt_user}'\nDengan gaya rujukan: {style_reference}. Berikan HANYA teks prompt bahasa Inggris."
            
            with st.spinner("Gemini Flash-Lite sedang merancang konsep gambar..."):
                response_gemini = model.generate_content(prompt_system)
                refined_prompt = response_gemini.text.strip()
            
            # 2. Render gambar tanpa watermark (nologo=true)
            with st.spinner("AI sedang melukis gambar bersih... Mohon tunggu sebentar..."):
                encoded_prompt = urllib.parse.quote(refined_prompt)
                
                # Parameter nologo=true ditambahkan untuk menghilangkan watermark
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                
                response = requests.get(image_url)
                
                if response.status_code == 200:
                    image_bytes = response.content
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
                else:
                    st.error("Gagal mengunduh gambar dari server.")
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan saat memproses: {str(err)}")
