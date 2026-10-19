import io
import streamlit as st
import requests
from PIL import Image
import urllib.parse

# Konfigurasi Halaman Web
st.set_page_config(page_title="AI Generator Ilustrasi Edukasi", page_icon="🎨", layout="centered")

st.title("🎨 AI Generator Ilustrasi & Kartun Edukasi SD/MI")
st.caption("Aplikasi mandiri untuk membuat gambar ilustrasi soal, kartun karakter, atau media pembelajaran.")

# Sidebar Informasi
with st.sidebar:
    st.header("⚙️ Informasi Aplikasi")
    st.markdown("Aplikasi ini menggunakan teknologi AI generator gambar terbuka yang cepat dan praktis untuk kebutuhan media pembelajaran guru.")
    st.markdown("---")
    st.markdown("### 💡 Tips Deskripsi (Prompt):")
    st.markdown("- Gunakan deskripsi yang spesifik, misal: *'Ilustrasi kartun anak perempuan mengenakan seragam merah putih sedang menyapu lantai kelas, gaya buku anak'*. ")
    st.markdown("- Anda juga bisa menuliskan dalam bahasa Inggris agar hasilnya lebih maksimal.")

# Form Input Pengguna
prompt_user = st.text_area(
    "Deskripsikan gambar ilustrasi yang ingin dibuat:", 
    placeholder="Contoh: Ilustrasi kartun anak perempuan mengenakan seragam sekolah sedang menyapu lantai kelas dengan ceria"
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
    if not prompt_user:
        st.warning("Mohon deskripsikan gambar yang ingin Anda buat terlebih dahulu.")
    else:
        try:
            with st.spinner("AI sedang melukis ilustrasi Anda... Mohon tunggu beberapa detik..."):
                
                # Menggabungkan deskripsi pengguna dan pilihan gaya
                full_prompt = f"{prompt_user}, style: {gaya_gambar}, high quality, bright colors, clean background, suitable for elementary school education"
                
                # Mengubah spasi dan karakter khusus agar aman dibaca di URL
                encoded_prompt = urllib.parse.quote(full_prompt)
                
                # URL Endpoint AI Image Generation (Gratis & Tanpa API Key berbayar)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                
                # Mengunduh gambar dari server
                response = requests.get(image_url)
                
                if response.status_code == 200:
                    image_bytes = response.content
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    st.success("✨ Ilustrasi Berhasil Dibuat!")
                    st.image(image, caption=f"Hasil: {prompt_user}", use_container_width=True)
                    
                    # Tombol Download Gambar
                    st.download_button(
                        label="📥 Download Gambar (JPG)",
                        data=image_bytes,
                        file_name="ilustrasi_edukasi.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                else:
                    st.error("Gagal terhubung ke server pembuat gambar. Silakan coba lagi.")
                    
        except Exception as err:
            st.error(f"Terjadi kesalahan pada sistem: {str(err)}")
