import io
import streamlit as st
from openai import OpenAI
from PIL import Image

# Konfigurasi Halaman Web
st.set_page_config(page_title="AI Generator Ilustrasi Edukasi", page_icon="🎨", layout="centered")

st.title("🎨 AI Generator Ilustrasi & Kartun Edukasi SD/MI")
st.caption("Buat gambar ilustrasi soal, kartun karakter, atau media pembelajaran secara instan.")

# Sidebar untuk API Key OpenAI
with st.sidebar:
    st.header("⚙️ Konfigurasi API")
    default_key = st.secrets.get("OPENAI_API_KEY", "")
    api_key = st.text_input("OpenAI API Key", value=default_key, type="password")
    
    st.markdown("---")
    st.markdown("### 💡 Tips Prompt yang Baik:")
    st.markdown("- Gunakan gaya **'cute flat cartoon style for kids education'** agar cocok untuk anak SD/MI.")
    st.markdown("- Jelaskan objek secara spesifik (warna baju, ekspresi, aktivitas).")

# Form Input Pengguna
prompt_user = st.text_area(
    "Deskripsikan gambar ilustrasi yang ingin dibuat:", 
    placeholder="Contoh: Ilustrasi kartun anak perempuan mengenakan seragam sekolah sedang menyapu lantai kelas dengan ceria, gaya buku anak SD"
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
        st.error("Silakan masukkan OpenAI API Key Anda terlebih dahulu pada panel samping.")
    elif not prompt_user:
        st.warning("Mohon deskripsikan gambar yang ingin Anda buat.")
    else:
        try:
            # Inisialisasi klien OpenAI
            client = OpenAI(api_key=api_key)
            
            # Menyusun prompt lengkap
            full_prompt = f"{prompt_user}, style: {gaya_gambar}, high quality, bright colors, educational children illustration, clean background"
            
            with st.spinner("AI sedang melukis ilustrasi Anda... Mohon tunggu beberapa detik..."):
                
                # Memanggil DALL-E 3 API untuk generate gambar
                response = client.images.generate(
                    model="dall-e-2",
                    prompt=full_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                image_url = response.data[0].url
                
                # Menampilkan hasil gambar
                st.success("✨ Ilustrasi Berhasil Dibuat!")
                st.image(image_url, caption=f"Hasil: {prompt_user}", use_container_width=True)
                
                st.info("💡 Anda dapat langsung klik kanan pada gambar di atas lalu pilih 'Simpan Gambar Sebagai...' (Save Image As) untuk mengunduhnya.")
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan saat membuat gambar: {str(err)}")
