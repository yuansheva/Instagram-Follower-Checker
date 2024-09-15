import streamlit as st
import json

# Fungsi untuk membaca data dari file JSON
def read_json(file):
    return json.load(file)

# Fungsi untuk memproses data followers
def process_followers(data):
    followers = [user_data["value"] for item in data for user_data in item["string_list_data"]]
    return followers

# Fungsi untuk memproses data following
def process_following(data):
    following = [user_data["value"] for item in data["relationships_following"] for user_data in item["string_list_data"]]
    return following

st.title("Instagram Follower Checker")

# Menampilkan pengumuman atau panduan

# Fungsi untuk halaman panduan
def show_guide():
    st.markdown("""
        ## 📢 Panduan Mendapatkan File Follower dan Following

        Selamat datang di aplikasi **Instagram Follower Checker** yang dikembangkan dengan Streamlit! Aplikasi ini memungkinkan Anda untuk menganalisis akun Instagram yang Anda ikuti dan menentukan siapa yang tidak mengikuti Anda kembali. Berikut adalah langkah-langkah untuk menggunakan aplikasi ini:

        ### Langkah 1: Buka Account Center Instagram
        1. **Pilih Your Information and Permissions**:
           - Klik tombol Download your information.
           - klik tombol Download or transfer information.
           
        2. **Pilih Akun yang mau di dilihat**:
           - Klik tombol Some of your information.
           - Scroll kebawah, pilih Followers and Following.

        ### Langkah 2: Download to device
        1. Create files to download, sesuaikan dengan kemauan Anda, disini saya memilih date range nya All time dan Format JSON
        2. Klik tombol Create files

        ### Langkah 3: Create files
        - Menunggu sampai tombol download muncul, semakin banyak datanya semakin lama prosessnya 
        - Setelah muncul tombol download nya, silahkan download

        ### Langkah 3: Ekstraksi Files
        - Setelah berhasil didownload, file harus di ekstrak dari ZIP nya
        - lalu ambil file folowing_1 dan followers

        ### Catatan
        - Aplikasi ini tidak menyimpan data pribadi anda
        - Jangan lupa follow akun instagram **@yuansheva**
    """)

def run_app():
    st.markdown("""
        ## 📢 Pengumuman: Panduan Menggunakan Aplikasi Instagram Follower Checker

        Selamat datang di aplikasi **Instagram Follower Checker** yang dikembangkan dengan Streamlit! Aplikasi ini memungkinkan Anda untuk menganalisis akun Instagram yang Anda ikuti dan menentukan siapa yang tidak mengikuti Anda kembali. **Sebelum menggunakan Aplikasi Instagram Follower Checker, Anda telah menyiapkan requirements dengan file follower_1.json dan following.json. Anda bisa melihat panduan di navigation untuk mendapatkan file tersebut.** Berikut adalah langkah-langkah untuk menggunakan aplikasi ini:

        ### Langkah 1: Unggah File JSON
        1. **Pilih File Followers**:
        - Klik tombol **"Upload Followers JSON file"**.
        - Pilih file JSON yang berisi data followers Anda (`follower_1.json`).
        
        2. **Pilih File Following**:
        - Klik tombol **"Upload Following JSON file"**.
        - Pilih file JSON yang berisi data following Anda (`following.json`).

        ### Langkah 2: Lihat Hasil Analisis
        1. Setelah mengunggah kedua file, aplikasi akan secara otomatis menganalisis data dan menampilkan hasil analisis.
        2. Di bagian hasil, Anda akan melihat daftar akun yang Anda ikuti tetapi tidak mengikuti Anda kembali.
        - **Tombol "Open Profile"**: Klik tombol ini untuk membuka profil Instagram dari setiap akun yang tidak mengikuti Anda kembali di tab baru.

        ### Langkah 3: Periksa Statistik
        - **Total Followers**: Jumlah total followers Anda.
        - **Total Following**: Jumlah total akun yang Anda ikuti.
        - **Jumlah Akun yang Tidak Mengikuti Kembali**: Jumlah akun yang Anda ikuti tetapi tidak mengikuti Anda kembali.

        ### Catatan
        - Aplikasi ini tidak menyimpan data pribadi anda
        - Jangan lupa follow akun instagram **@yuansheva**
    """)

    # Upload file followers dan following
    followers_file = st.file_uploader("Upload Followers JSON file", type="json")
    following_file = st.file_uploader("Upload Following JSON file", type="json")

    if followers_file and following_file:
        try:
            # Membaca data dari file
            followers_data = read_json(followers_file)
            following_data = read_json(following_file)

            # Memproses data
            followers = process_followers(followers_data)
            following = process_following(following_data)

            # Menentukan akun yang tidak mengikuti balik
            not_following_back = set(following) - set(followers)

            # Menampilkan hasil analisis
            st.write("Akun yang Anda ikuti tapi tidak mengikuti Anda kembali:")

            # Menyusun tombol dalam kolom-kolom
            num_columns = 3  # Jumlah kolom yang diinginkan
            cols = st.columns(num_columns)
            for i, username in enumerate(not_following_back):
                url = f"https://www.instagram.com/{username}"
                col = cols[i % num_columns]
                col.markdown(f'<a href="{url}" target="_blank" class="btn">{username}</a>', unsafe_allow_html=True)

            # Menampilkan statistik
            st.write(f"Total followers: {len(followers)}")
            st.write(f"Total following: {len(following)}")
            st.write(f"Jumlah akun yang tidak mengikuti Anda kembali: {len(not_following_back)}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # CSS untuk styling tombol
    st.markdown("""
        <style>
        .btn {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            font-size: 16px;
            font-weight: bold;
            color: white !important; /* Warna teks tombol */
            background-color: #ff6347; /* Warna latar belakang tombol */
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
        }
        .btn:hover {
            background-color: #0056b3; /* Warna latar belakang tombol saat hover */
        }
        </style>
    """, unsafe_allow_html=True)

# Sidebar untuk navigasi
st.sidebar.title("Navigation")
page = st.sidebar.radio("Pilih Halaman", ["Panduan", "Aplikasi"])

# Menampilkan halaman berdasarkan pilihan pengguna
if page == "Panduan":
    show_guide()
elif page == "Aplikasi":
    run_app()
