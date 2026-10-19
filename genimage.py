import io
import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
import urllib.parse

# Konfigurasi Halaman Web
st.set_page_config(page_title="AI Generator Ilustrasi Edukasi", page_icon="🎨", layout="centered")

st.title("🎨 AI Generator Ilustrasi & Kartun Edukasi SD/MI")
st.caption("Didukung oleh Google Gemini (Model Flash) & AI Image Engine")

# Sidebar untuk Konfigurasi API Key
with st.sidebar:
    st.header("⚙️ Konfigurasi API")
    default_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Gemini API Key", 
        value=default_key, 
        type="password", 
        help="Masukkan API Key Google AI Studio Anda"
    )
    st.markdown("---")
    st.markdown("Aplikasi ini memanfaatkan kecepatan **Gemini Flash** untuk mengoptimalkan deskripsi gambar Anda agar ramah anak dan sesuai konteks sekolah.")

# Form Input Pengguna
prompt_user = st.text_area(
    "Deskripsikan gambar ilustrasi yang ingin dibuat:", 
    placeholder="Contoh: Rani sedang menyapu lantai kelas bersama teman-temannya"
)

gaya_gambar = st.selectbox(
    "Pilih Gaya Visual", 
    [
        "Kartun Edukasi Anak (Flat Cartoon Style)", 
        "Ilustrasi Buku Cerita (Storybook Children Illustration)", 
        "Gaya Garis Hitam Putih / Lembar Mewarnai (Black & White Line Art)", 
        "Infografis atau Diagram Sederhana (Simple Educational Infographic)"
    ]
)

# Tombol Eksekusi
if st.button("🚀 Buat Ilustrasi Sekarang", type="primary", use_container_width=True):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key Anda terlebih dahulu pada panel samping.")
    elif not prompt_user:
        st.warning("Mohon deskripsikan gambar yang ingin Anda buat terlebih dahulu.")
    else:
        try:
            # 1. Konfigurasi dan Gunakan Gemini Model Flash untuk Menyempurnakan Prompt
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            system_instruction = (
                "Anda adalah asisten AI pendidikan. Tugas Anda adalah menerjemahkan dan memperkaya deskripsi "
                "dari guru SD/MI menjadi prompt visual berbahasa Inggris yang sangat detail, spesifik, cerah, "
                "ramah anak, dan bergaya kartun edukasi yang bersih."
            )
            
            prompt_penyempurna = f"{system_instruction}\n\nDeskripsi guru: '{prompt_user}'\nGaya visual: '{gaya_gambar}'\n\nBerikan HANYA teks prompt bahasa Inggris yang siap pakai untuk pembuat gambar tanpa teks pengantar tambahan."
            
            with st.spinner("Gemini Flash sedang merancang konsep gambar..."):
                ai_response = model.generate_content(prompt_penyempurna)
                refined_prompt = ai_response.text.strip()
            
            # 2. Generate Gambar Berdasarkan Prompt yang Telah Diperkaya Gemini
            with st.spinner("AI sedang melukis ilustrasi berdasarkan konsep Gemini..."):
                encoded_prompt = urllib.parse.quote(refined_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                
                response = requests.get(image_url)
                
                if response.status_code == 200:
                    image_bytes = response.content
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    st.success("✨ Ilustrasi Berhasil Dibuat!")
                    st.image(image, caption=f"Konsep AI: {refined_prompt}", use_container_width=True)
                    
                    st.download_button(
                        label="📥 Download Gambar (JPG)",
                        data=image_bytes,
                        file_name="ilustrasi_edukasi.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                else:
                    st.error("Gagal mengunduh gambar dari server.")
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan pada sistem: {str(err)}")
