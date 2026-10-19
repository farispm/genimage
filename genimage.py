import streamlit as st
import requests
from PIL import Image
import io
import urllib.parse

# Konfigurasi Halaman Web
st.set_page_config(page_title="AI Generator Ilustrasi Edukasi", page_icon="🎨", layout="centered")

st.title("🎨 AI Generator Ilustrasi & Kartun Edukasi SD/MI")
st.caption("Buat gambar ilustrasi soal, kartun karakter, atau media pembelajaran secara instan (Gratis).")

# Sidebar
with st.sidebar:
    st.header("⚙️ Informasi")
    st.markdown("Aplikasi ini menggunakan layanan AI publik sehingga **tidak memerlukan API Key** berbayar.")

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
    if not prompt_user:
        st.warning("Mohon deskripsikan gambar yang ingin Anda buat.")
    else:
        try:
            with st.spinner("AI sedang melukis ilustrasi Anda... Mohon tunggu beberapa detik..."):
                
                # Menggabungkan prompt dan gaya
                full_prompt = f"{prompt_user}, style: {gaya_gambar}, high quality, bright colors, educational children illustration"
                
                # Encode prompt untuk URL
                encoded_prompt = urllib.parse.quote(full_prompt)
                
                # URL Endpoint Pollinations.ai (Gratis & Tanpa Key)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                
                # Mengunduh gambar
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_bytes = response.content
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
                else:
                    st.error("Gagal mengunduh gambar dari server AI.")
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan saat membuat gambar: {str(err)}")
