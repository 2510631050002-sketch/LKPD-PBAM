
import streamlit as st
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Petualangan Luas Lingkaran",
    page_icon="🔵",
    layout="wide"
)

# =========================
# DESAIN TAMPILAN
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #FFF9F0;
}
.main-title {
    text-align: center;
    color: #FF758F;
    font-size: 38px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #64748B;
    font-size: 17px;
}
.lesson-card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 18px;
    border: 2px solid #FFD6A5;
    margin-bottom: 12px;
}
div.stButton > button {
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA SOAL
# =========================
soal_pg = [
    {
        "soal": "Apa yang dimaksud dengan luas lingkaran?",
        "opsi": [
            "Panjang garis tepi lingkaran",
            "Daerah yang berada di dalam lingkaran",
            "Jarak dari pusat ke tepi",
            "Garis yang melewati pusat"
        ],
        "jawaban": 1
    },
    {
        "soal": "Apa rumus luas lingkaran?",
        "opsi": ["2 × π × r", "π × r", "π × r × r", "π + r"],
        "jawaban": 2
    },
    {
        "soal": "Jika jari-jari lingkaran 7 cm, berapa diameternya?",
        "opsi": ["7 cm", "14 cm", "21 cm", "28 cm"],
        "jawaban": 1
    },
    {
        "soal": "Jika diameter lingkaran 20 cm, berapa jari-jarinya?",
        "opsi": ["5 cm", "10 cm", "20 cm", "40 cm"],
        "jawaban": 1
    },
    {
        "soal": "Nilai π yang sering digunakan jika jari-jari kelipatan 7 adalah ...",
        "opsi": ["2,14", "3,14", "22/7", "7/22"],
        "jawaban": 2
    },
    {
        "soal": "Sebuah lingkaran memiliki jari-jari 7 cm. Luasnya adalah ...",
        "opsi": ["44 cm²", "77 cm²", "154 cm²", "308 cm²"],
        "jawaban": 2
    },
    {
        "soal": "Luas lingkaran dengan jari-jari 10 cm adalah ... (π = 3,14)",
        "opsi": ["31,4 cm²", "62,8 cm²", "100 cm²", "314 cm²"],
        "jawaban": 3
    },
    {
        "soal": "Sebuah lingkaran memiliki diameter 14 cm. Luasnya adalah ...",
        "opsi": ["44 cm²", "154 cm²", "196 cm²", "308 cm²"],
        "jawaban": 1
    },
    {
        "soal": "Jika jari-jari lingkaran menjadi 2 kali semula, luasnya menjadi ...",
        "opsi": [
            "2 kali semula",
            "3 kali semula",
            "4 kali semula",
            "Tetap sama"
        ],
        "jawaban": 2
    },
    {
        "soal": "Sebuah taman berbentuk lingkaran memiliki jari-jari 14 m. Berapa luasnya?",
        "opsi": [
            "154 m²",
            "308 m²",
            "616 m²",
            "1.232 m²"
        ],
        "jawaban": 2
    }
]

# Lima soal tambahan berupa jawaban angka
soal_isian = [
    {
        "soal": "Jari-jari lingkaran 14 cm. Hitung luasnya! (π = 22/7)",
        "jawaban": 616,
        "satuan": "cm²"
    },
    {
        "soal": "Diameter lingkaran 28 cm. Berapa jari-jarinya?",
        "jawaban": 14,
        "satuan": "cm"
    },
    {
        "soal": "Jari-jari lingkaran 5 cm. Hitung luasnya! (π = 3,14)",
        "jawaban": 78.5,
        "satuan": "cm²"
    },
    {
        "soal": "Luas lingkaran 154 cm². Jika π = 22/7, berapa jari-jarinya?",
        "jawaban": 7,
        "satuan": "cm"
    },
    {
        "soal": "Jari-jari roda berbentuk lingkaran 21 cm. Berapa luasnya? (π = 22/7)",
        "jawaban": 1386,
        "satuan": "cm²"
    }
]

# =========================
# SESSION STATE
# =========================
if "halaman" not in st.session_state:
    st.session_state.halaman = "Beranda"

if "nama" not in st.session_state:
    st.session_state.nama = ""

if "hasil" not in st.session_state:
    st.session_state.hasil = None

# =========================
# SIDEBAR / NAVIGASI
# =========================
st.sidebar.title("🌈 Menu Belajar")
st.sidebar.caption("Petualangan Luas Lingkaran")

menu = st.sidebar.radio(
    "Pilih halaman:",
    [
        "Beranda",
        "Materi",
        "Visualisasi",
        "Latihan",
        "Hasil Belajar"
    ],
    key="menu_navigasi"
)

st.session_state.halaman = menu

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 Tips: Pelajari materi dahulu, "
    "lalu kerjakan latihan dengan teliti!"
)

# =========================
# BERANDA
# =========================
if menu == "Beranda":
    st.markdown(
        '<div class="main-title">🔵 Petualangan Luas Lingkaran</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Belajar matematika jadi seru '
        'bersama si Lingkaran!</div>',
        unsafe_allow_html=True
    )

    st.write("")
    kiri, kanan = st.columns([1, 1])

    with kiri:
        st.markdown("""
        <div class="lesson-card">
        <h3>🎒 Halo, Teman Matematika!</h3>
        Yuk, kita belajar menghitung luas lingkaran
        melalui materi, gambar, dan permainan soal.
        </div>
        """, unsafe_allow_html=True)

        nama = st.text_input(
            "Siapa namamu?",
            value=st.session_state.nama,
            placeholder="Tulis namamu di sini..."
        )
        st.session_state.nama = nama

        st.success("Ayo belajar sambil bermain! 🌟")

    with kanan:
        st.markdown("### 🎯 Misi Belajar")
        st.markdown("""
        - 📖 Memahami pengertian luas lingkaran.
        - 📐 Mengenal jari-jari dan diameter.
        - 🔵 Melihat bentuk lingkaran.
        - ✏️ Menyelesaikan 10 soal pilihan ganda.
        - 🧩 Mencoba 5 soal tambahan.
        """)

    st.markdown("---")
    st.markdown("### 🚀 Siap memulai petualangan?")
    st.write("Pilih menu **Materi** untuk mulai belajar.")
    st.button(
        "📚 Mulai Belajar",
        on_click=lambda: st.session_state.update(
            menu_navigasi="Materi",
            halaman="Materi"
        ),
        use_container_width=True
    )

# =========================
# MATERI
# =========================
elif menu == "Materi":
    st.title("📚 Mengenal Luas Lingkaran")

    st.markdown("""
    <div class="lesson-card">
    <h3>🔵 Apa itu lingkaran?</h3>
    Lingkaran adalah bangun datar yang memiliki satu titik pusat
    dan garis tepi yang setiap titiknya berjarak sama dari pusat.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📏 Bagian-bagian lingkaran")
    st.markdown("""
    - **Titik pusat:** titik yang berada di tengah lingkaran.
    - **Jari-jari (r):** jarak dari titik pusat ke tepi lingkaran.
    - **Diameter (d):** garis yang melewati titik pusat
      dan menghubungkan dua titik pada tepi lingkaran.
    """)

    st.subheader("🧮 Rumus luas lingkaran")
    st.latex(r"L = \pi \times r \times r")
    st.write("Keterangan:")
    st.write("- L = luas lingkaran")
    st.write("- π = 3,14 atau 22/7")
    st.write("- r = jari-jari lingkaran")

    st.info("Ingat: diameter = 2 × jari-jari.")

    st.subheader("✏️ Contoh soal")
    st.write(
        "Sebuah lingkaran mempunyai jari-jari 7 cm. "
        "Berapa luasnya?"
    )

    with st.expander("Lihat langkah penyelesaian"):
        st.write("Diketahui: r = 7 cm dan π = 22/7")
        st.latex(r"L = \pi \times r \times r")
        st.latex(r"L = \frac{22}{7} \times 7 \times 7")
        st.latex(r"L = 154\text{ cm}^2")
        st.success("Jadi, luas lingkaran adalah 154 cm².")

# =========================
# VISUALISASI LINGKARAN
# =========================
elif menu == "Visualisasi":
    st.title("🎨 Ayo Bermain dengan Lingkaran!")
    st.write(
        "Geser jari-jari dan lihat bagaimana ukuran "
        "lingkaran berubah."
    )

    radius = st.slider(
        "Pilih jari-jari lingkaran (cm)",
        min_value=1,
        max_value=20,
        value=7
    )

    fig, ax = plt.subplots(figsize=(5, 5))
    lingkaran = Circle(
        (0, 0),
        radius,
        facecolor="#FFB3C6",
        edgecolor="#FF4D6D",
        linewidth=3,
        alpha=0.8
    )

    ax.add_patch(lingkaran)
    ax.plot(0, 0, "o", color="#264653")
    ax.plot([0, radius], [0, 0], color="#264653", linewidth=3)

    ax.text(
        radius / 2,
        0.5,
        f"r = {radius} cm",
        ha="center",
        fontsize=12
    )

    ax.set_xlim(-radius - 2, radius + 2)
    ax.set_ylim(-radius - 2, radius + 2)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    ax.set_title("Lingkaran dan Jari-jari")

    st.pyplot(fig)
    plt.close(fig)

    luas = math.pi * radius**2

    kolom1, kolom2 = st.columns(2)
    kolom1.metric("Jari-jari", f"{radius} cm")
    kolom2.metric("Luas (π = 3,14)", f"{luas:.2f} cm²")

    st.caption(
        "Semakin besar jari-jari, semakin besar pula luas lingkaran."
    )

# =========================
# LATIHAN
# =========================
elif menu == "Latihan":
    st.title("✏️ Kuis Petualangan")
    st.write("Jawab semua soal, ya! Semangat! 🌟")

    tab1, tab2 = st.tabs([
        "🔵 10 Pilihan Ganda",
        "🧩 5 Soal Tambahan"
    ])

    with tab1:
        with st.form("form_pg"):
            jawaban_pg = {}

            for i, soal in enumerate(soal_pg):
                st.markdown(f"**Soal {i+1}. {soal['soal']}**")

                jawaban_pg[i] = st.radio(
                    "Pilih jawaban:",
                    options=list(range(len(soal["opsi"]))),
                    format_func=lambda x, s=soal: s["opsi"][x],
                    key=f"pg_{i}",
                    index=None
                )
                st.markdown("---")

            kirim_pg = st.form_submit_button(
                "Periksa Pilihan Ganda",
                use_container_width=True
            )

        if kirim_pg:
            benar = 0
            kosong = 0

            for i, soal in enumerate(soal_pg):
                pilihan = jawaban_pg[i]
                if pilihan is None:
                    kosong += 1
                elif pilihan == soal["jawaban"]:
                    benar += 1

            nilai_pg = benar * 10

            st.session_state.hasil_pg = {
                "benar": benar,
                "kosong": kosong,
                "nilai": nilai_pg,
                "jawaban": jawaban_pg
            }

            st.success(
                f"Pilihan ganda selesai! "
                f"Jawaban benar: {benar}/10. "
                f"Nilai: {nilai_pg}/100."
            )

            for i, soal in enumerate(soal_pg):
                pilihan = jawaban_pg[i]
                teks_benar = soal["opsi"][soal["jawaban"]]

                if pilihan == soal["jawaban"]:
                    st.write(f"✅ Soal {i+1}: Benar!")
                else:
                    st.write(
                        f"❌ Soal {i+1}: Jawaban benar adalah "
                        f"**{teks_benar}**."
                    )

    with tab2:
        st.info(
            "Masukkan jawaban berupa angka saja. "
            "Contoh: 154. Gunakan titik untuk desimal, "
            "misalnya 78.5."
        )

        with st.form("form_isian"):
            jawaban_isian = {}

            for i, soal in enumerate(soal_isian):
                st.markdown(f"**Soal {i+1}. {soal['soal']}**")
                jawaban_isian[i] = st.text_input(
                    f"Jawaban ({soal['satuan']})",
                    key=f"isian_{i}"
                )

            kirim_isian = st.form_submit_button(
                "Periksa Soal Tambahan",
                use_container_width=True
            )

        if kirim_isian:
            benar = 0
            detail = []

            for i, soal in enumerate(soal_isian):
                teks = jawaban_isian[i].strip().replace(",", ".")

                try:
                    nilai = float(teks)
                    betul = math.isclose(
                        nilai,
                        soal["jawaban"],
                        rel_tol=0,
                        abs_tol=0.02
                    )
                except ValueError:
                    betul = False

                if betul:
                    benar += 1

                detail.append({
                    "nomor": i + 1,
                    "betul": betul,
                    "jawaban_benar": soal["jawaban"],
                    "satuan": soal["satuan"]
                })

            st.session_state.hasil_isian = {
                "benar": benar,
                "nilai": benar * 20,
                "detail": detail
            }

            st.success(
                f"Soal tambahan selesai! "
                f"Jawaban benar: {benar}/5. "
                f"Nilai: {benar * 20}/100."
            )

            for item in detail:
                if item["betul"]:
                    st.write(f"✅ Soal {item['nomor']}: Benar!")
                else:
                    st.write(
                        f"❌ Soal {item['nomor']}: "
                        f"Jawaban benar adalah "
                        f"{item['jawaban_benar']} "
                        f"{item['satuan']}."
                    )

# =========================
# HASIL DAN PROGRES BELAJAR
# =========================
elif menu == "Hasil Belajar":
    st.title("🏆 Hasil Belajarku")

    hasil_pg = st.session_state.get("hasil_pg")
    hasil_isian = st.session_state.get("hasil_isian")

    if not hasil_pg and not hasil_isian:
        st.info(
            "Kamu belum mengerjakan latihan. "
            "Yuk, buka menu Latihan terlebih dahulu!"
        )
    else:
        skor_pg = hasil_pg["nilai"] if hasil_pg else None
        skor_isian = hasil_isian["nilai"] if hasil_isian else None

        if skor_pg is not None:
            st.subheader("🔵 Hasil Pilihan Ganda")
            st.metric(
                "Nilai pilihan ganda",
                f"{skor_pg}/100"
            )
            st.progress(skor_pg / 100)

        if skor_isian is not None:
            st.subheader("🧩 Hasil Soal Tambahan")
            st.metric(
                "Nilai soal tambahan",
                f"{skor_isian}/100"
            )
            st.progress(skor_isian / 100)

        if skor_pg is not None and skor_isian is not None:
            nilai_akhir = round((skor_pg + skor_isian) / 2)

            st.markdown("---")
            st.subheader("🌟 Nilai Akhir")
            st.metric("Rata-rata nilai", f"{nilai_akhir}/100")
            st.progress(nilai_akhir / 100)

            if nilai_akhir >= 80:
                st.balloons()
                st.success(
                    "Hebat! Kamu sudah memahami luas lingkaran. 🎉"
                )
            elif nilai_akhir >= 60:
                st.info(
                    "Bagus! Pelajari kembali materi yang belum dikuasai."
                )
            else:
                st.warning(
                    "Jangan menyerah! Baca materi lagi dan coba latihan."
                )

        elif skor_pg is not None:
            st.info(
                "Pilihan ganda sudah selesai. "
                "Kerjakan soal tambahan untuk melihat nilai akhir."
            )
        else:
            st.info(
                "Soal tambahan sudah selesai. "
                "Kerjakan pilihan ganda untuk melihat nilai akhir."
            )

    st.markdown("---")
    st.caption(
        "Catatan: hasil belajar tersimpan selama sesi aplikasi aktif. "
        "Jika aplikasi dimulai ulang, hasil dapat terhapus."
    )
