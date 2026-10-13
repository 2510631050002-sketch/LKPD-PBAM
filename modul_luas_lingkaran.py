import math
import io
import wave
import struct
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ============================================================
# MODUL INTERAKTIF LUAS LINGKARAN - KELAS VI SD/MI
# Jalankan: streamlit run modul_luas_lingkaran.py
# ============================================================

st.set_page_config(
    page_title="Petualangan Luas Lingkaran | Kelas VI",
    page_icon="⭕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- TEMA / DESAIN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.stApp { background: #F7FAF5; color: #24352A; }
[data-testid="stHeader"] { background: #F7FAF5; }
.hero {
    background: linear-gradient(120deg, #DDEFE0, #FFF1C9);
    padding: 1.5rem 1.8rem; border-radius: 24px;
    border: 1px solid #D0E3D1; margin-bottom: 1rem;
}
.hero h1 { color: #214D35 !important; }
.hero p { color: #355B43 !important; font-size: 1.05rem; }
.info-card {
    background: white; color: #24352A; padding: 1rem;
    border-radius: 18px; border: 1px solid #E0E9DF;
    min-height: 110px; margin-bottom: .5rem;
}
.formula {
    background: #E5F1E5; color: #214D35 !important;
    padding: 1rem; border-radius: 15px; text-align: center;
    font-size: 1.35rem; font-weight: 800; margin: .6rem 0;
}
div.stButton > button {
    border-radius: 13px; font-weight: 800;
    border: 1px solid #B8D2BA; min-height: 2.8rem;
}
[data-testid="stMetric"] {
    background: white; padding: .8rem; border-radius: 14px;
    border: 1px solid #E0E9DF;
}
.small-note { color: #4A5D4D; font-size: .9rem; }
</style>
""", unsafe_allow_html=True)

# ---------- KONFIGURASI MENU ----------
MENU = [
    ("🎯", "Capaian Pembelajaran"),
    ("🧭", "Petunjuk Penggunaan"),
    ("🌻", "Pengantar Materi"),
    ("🧠", "Materi Inti"),
    ("✏️", "Latihan Soal"),
    ("💭", "Refleksi"),
]

# ---------- PENYIMPANAN DATA SEMENTARA ----------
defaults = {
    "screen": "Cover",
    "completed": set(),
    "student_name": "",
    "answers": {},
    "quiz_submitted": False,
    "quiz_score": 0,
    "quiz_results": [],
    "reflection": {},
    "reset_quiz_widgets": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def go(screen):
    """Mengganti layar aplikasi."""
    st.session_state.screen = screen
    st.rerun()

def mark_complete(section):
    """Menandai bagian yang sudah dipelajari."""
    st.session_state.completed.add(section)

def hero(title, subtitle):
    """Menampilkan banner judul halaman."""
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

def nav_buttons():
    """Tombol Home membawa siswa kembali ke menu pilihan."""
    st.divider()
    left, right = st.columns([1, 1])
    with left:
        if st.button("🏠 Home / Menu Pilihan", use_container_width=True, key="home_bottom"):
            go("Menu")
    with right:
        if st.button("🏡 Kembali ke Cover", use_container_width=True, key="cover_bottom"):
            go("Cover")

def draw_circle(radius=7, show_diameter=True, object_name=None):
    """Menggambar lingkaran dan memberi label jari-jari/diameter."""
    fig, ax = plt.subplots(figsize=(5, 3.5))
    circle = Circle((0, 0), radius, facecolor="#DDEFE0",
                    edgecolor="#2F7047", linewidth=2.5, alpha=.95)
    ax.add_patch(circle)
    ax.plot([0, radius], [0, 0], color="#D18B2C", linewidth=2.7)
    ax.scatter([0, radius], [0, 0], color=["#2F7047", "#D18B2C"], zorder=3)
    ax.text(radius / 2, .35, f"r = {radius:g}", ha="center",
            color="#80531A", fontsize=11, weight="bold")
    if show_diameter:
        ax.plot([-radius, radius], [0, 0], color="#547BBA",
                linewidth=1.8, linestyle="--")
        ax.text(0, -.65, f"d = {2*radius:g}", ha="center",
                color="#34588A", fontsize=10, weight="bold")
    ax.set_xlim(-radius - 1.5, radius + 1.5)
    ax.set_ylim(-radius - 1.5, radius + 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_alpha(0)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

def fmt_num(value):
    if abs(value - round(value)) < 1e-8:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")

def make_tone(correct=True):
    """Membuat bunyi pendek sederhana; siswa perlu menekan play karena kebijakan browser."""
    sample_rate = 22050
    duration = 0.24
    frequency = 880 if correct else 220
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for i in range(int(sample_rate * duration)):
            fade = min(1, i / 300, (sample_rate * duration - i) / 500)
            sample = int(11000 * max(0, fade) * math.sin(2 * math.pi * frequency * i / sample_rate))
            wav.writeframesraw(struct.pack("<h", sample))
    return buf.getvalue()

# ---------- BANK SOAL ----------
# Jawaban pilihan ganda disimpan sebagai indeks mulai dari 0.
QUESTIONS = [
    {
        "id": "q1", "type": "number", "topic": "jari-jari",
        "question": "Sebuah piring berbentuk lingkaran memiliki jari-jari 7 cm. Berapa luas permukaannya (cm²)?",
        "answer": 154, "unit": "cm²",
        "explanation": "Diketahui r = 7 cm. Karena 7 kelipatan 7, gunakan π = 22/7. L = 22/7 × 7 × 7 = 154 cm².",
    },
    {
        "id": "q2", "type": "single", "topic": "rumus",
        "question": "Rumus yang tepat untuk menghitung luas lingkaran adalah …",
        "options": ["L = π × r", "L = 2 × π × r", "L = π × r × r", "L = π × d"],
        "answer": 2, "explanation": "Luas lingkaran dihitung dengan L = π × r², yaitu π dikali jari-jari dikali jari-jari.",
    },
    {
        "id": "q3", "type": "multi", "topic": "pi",
        "question": "Pilih SEMUA pernyataan yang benar tentang pemilihan nilai π.",
        "options": [
            "π = 22/7 dapat digunakan jika jari-jari atau diameter merupakan kelipatan 7.",
            "π = 3,14 dapat digunakan untuk ukuran yang bukan kelipatan 7.",
            "Luas lingkaran selalu sama dengan 2 × π × r.",
            "Jika diameter diketahui, jari-jari diperoleh dengan membagi diameter dengan 2.",
        ],
        "answer": [0, 1, 3],
        "explanation": "Pernyataan 1, 2, dan 4 benar. Pernyataan 3 adalah rumus keliling, bukan rumus luas. Dalam perhitungan sekolah, π = 22/7 praktis untuk ukuran kelipatan 7 dan π = 3,14 untuk ukuran lainnya.",
    },
    {
        "id": "q4", "type": "number", "topic": "diameter",
        "question": "Sebuah pizza memiliki diameter 20 cm. Berapa luas pizza (cm²)?",
        "answer": 314, "unit": "cm²",
        "explanation": "Diketahui d = 20 cm. Jari-jari r = 20 ÷ 2 = 10 cm. Gunakan π = 3,14. L = 3,14 × 10 × 10 = 314 cm².",
        "visual": True,
    },
    {
        "id": "q5", "type": "single", "topic": "diameter",
        "question": "Tutup taman berbentuk lingkaran memiliki diameter 28 m. Berapakah jari-jarinya?",
        "options": ["7 m", "14 m", "28 m", "56 m"],
        "answer": 1,
        "explanation": "Jari-jari adalah setengah diameter. Jadi r = 28 ÷ 2 = 14 m.",
        "visual": True,
    },
    {
        "id": "q6", "type": "number", "topic": "kontekstual",
        "question": "Sebuah taman bundar memiliki jari-jari 14 m. Berapa luas taman tersebut (m²)?",
        "answer": 616, "unit": "m²",
        "explanation": "Diketahui r = 14 m. Gunakan π = 22/7. L = 22/7 × 14 × 14 = 616 m².",
        "visual": True,
    },
]

# ---------- COVER ----------
screen = st.session_state.screen

if screen == "Cover":
    st.markdown("<div style='text-align:center;font-size:4rem'>⭕ 🌼 📐</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="hero" style="text-align:center;padding:2.5rem 1.5rem">
      <p style="font-weight:800;letter-spacing:2px">MODUL PEMBELAJARAN INTERAKTIF • KELAS VI SD/MI</p>
      <h1 style="font-size:2.6rem">Petualangan Luas Lingkaran</h1>
      <p>Amati bentuknya, temukan rumusnya, lalu pecahkan tantangannya!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.markdown('<div class="info-card">⭕<br><b>Kenali bentuk</b><br>Jari-jari dan diameter</div>', unsafe_allow_html=True)
    col2.markdown('<div class="info-card">🧮<br><b>Belajar menghitung</b><br>Rumus luas lingkaran</div>', unsafe_allow_html=True)
    col3.markdown('<div class="info-card">🏆<br><b>Taklukkan tantangan</b><br>Latihan dan refleksi</div>', unsafe_allow_html=True)
    st.session_state.student_name = st.text_input(
        "Nama siswa (opsional)", value=st.session_state.student_name,
        placeholder="Tulis namamu sebelum mulai"
    )
    if st.button("🚀 Mulai Petualangan", type="primary", use_container_width=True):
        go("Menu")

# ---------- MENU UTAMA ----------
elif screen == "Menu":
    hero("🏠 Menu Pilihan", "Pilih bagian yang ingin kamu pelajari. Kamu bisa kembali ke menu ini kapan saja.")
    if st.session_state.student_name.strip():
        st.write(f"Halo, **{st.session_state.student_name.strip()}**! Siap belajar hari ini? 🌻")
    completed = len(st.session_state.completed)
    st.metric("Progres belajar", f"{completed}/6 bagian selesai")
    st.progress(completed / 6)
    cards = st.columns(3)
    for i, (emoji, title) in enumerate(MENU):
        with cards[i % 3]:
            status = "✅ Selesai" if title in st.session_state.completed else "Mulai belajar"
            st.markdown(
                f'<div class="info-card"><div style="font-size:2rem">{emoji}</div>'
                f'<b>{title}</b><br><span class="small-note">{status}</span></div>',
                unsafe_allow_html=True,
            )
            if st.button(f"Buka {title}", key=f"menu_{i}", use_container_width=True):
                go(title)
    st.divider()
    if st.session_state.quiz_submitted:
        st.metric("Skor latihan terakhir", f"{st.session_state.quiz_score}/100")
    if st.button("🏡 Kembali ke Cover", use_container_width=True):
        go("Cover")

# ---------- CAPAIAN PEMBELAJARAN ----------
elif screen == "Capaian Pembelajaran":
    hero("🎯 Capaian Pembelajaran", "Tujuan yang akan kamu capai setelah belajar.")
    st.markdown("### Setelah menyelesaikan modul ini, kamu diharapkan mampu:")
    goals = [
        "Mengenali jari-jari dan diameter lingkaran.",
        "Menjelaskan hubungan diameter dan jari-jari.",
        "Memilih nilai π yang sesuai untuk perhitungan.",
        "Menghitung luas lingkaran jika diketahui jari-jari atau diameter.",
        "Menyelesaikan masalah luas lingkaran dalam kehidupan sehari-hari.",
        "Menjelaskan langkah penyelesaian dengan bahasamu sendiri.",
    ]
    for goal in goals:
        st.markdown(f"- {goal}")
    st.info("Catatan untuk guru: rumusan di atas merupakan tujuan pembelajaran modul. Cocokkan dengan CP dan ATP resmi yang digunakan sekolah.")
    if st.button("✅ Saya sudah membaca tujuan", type="primary"):
        mark_complete(screen)
        st.success("Bagian capaian pembelajaran ditandai selesai.")
    nav_buttons()

# ---------- PETUNJUK PENGGUNAAN ----------
elif screen == "Petunjuk Penggunaan":
    hero("🧭 Petunjuk Penggunaan", "Ikuti langkah berikut agar petualangan belajarmu lebih mudah.")
    steps = [
        ("1", "Buka menu pilihan dan pilih bagian yang ingin dipelajari."),
        ("2", "Baca materi, amati gambar, dan coba alat hitung interaktif."),
        ("3", "Kerjakan latihan dengan teliti. Beberapa soal memiliki lebih dari satu jawaban benar."),
        ("4", "Periksa hasil dan baca pembahasan meskipun jawabanmu benar."),
        ("5", "Isi refleksi untuk mengetahui bagian yang sudah kamu kuasai."),
        ("6", "Gunakan tombol Home / Menu Pilihan untuk kembali ke daftar bagian."),
    ]
    for n, desc in steps:
        st.markdown(f'<div class="info-card"><b>{n}. {desc}</b></div>', unsafe_allow_html=True)
    st.warning("Untuk soal pilihan ganda kompleks, pilih semua jawaban yang benar. Untuk soal esai, tulis diketahui, ditanya, langkah hitung, dan kesimpulan.")
    if st.button("✅ Petunjuk sudah dipahami", type="primary"):
        mark_complete(screen)
        st.success("Bagian petunjuk ditandai selesai.")
    nav_buttons()

# ---------- PENGANTAR MATERI ----------
elif screen == "Pengantar Materi":
    hero("🌻 Pengantar Materi", "Lingkaran ada di banyak tempat di sekitar kita!")
    a, b = st.columns([1, 1])
    with a:
        st.markdown("### Pernah melihat benda-benda ini?")
        st.markdown("- 🍕 Pizza")
        st.markdown("- 🕒 Jam dinding")
        st.markdown("- 🍽️ Piring")
        st.markdown("- 🌳 Taman bundar")
        st.write("Luas adalah ukuran besar daerah yang berada di dalam batas lingkaran. Kita akan belajar menghitung seberapa luas permukaan benda-benda tersebut.")
    with b:
        draw_circle(7, True)
        st.caption("Gambar lingkaran: garis dari pusat ke tepi adalah jari-jari (r), sedangkan garis yang melewati pusat dari tepi ke tepi adalah diameter (d).")
    st.markdown('<div class="formula">d = 2 × r &nbsp;&nbsp; | &nbsp;&nbsp; r = d ÷ 2</div>', unsafe_allow_html=True)
    st.markdown("### Pertanyaan pemantik")
    st.write("Jika sebuah pizza diketahui diameternya 20 cm, apakah kita bisa langsung memasukkan 20 ke rumus luas? Mengapa?")
    answer = st.text_area("Tulis pendapatmu (opsional)", key="pengantar_pemantik")
    if st.button("✅ Saya selesai membaca pengantar", type="primary"):
        mark_complete(screen)
        st.success("Bagian pengantar ditandai selesai.")
    nav_buttons()

# ---------- MATERI INTI ----------
elif screen == "Materi Inti":
    hero("🧠 Materi Inti: Luas Lingkaran", "Pahami rumus, amati visualisasi, lalu coba ubah ukuran lingkaran.")
    st.markdown("### 1. Rumus luas lingkaran")
    st.markdown('<div class="formula">L = π × r × r = π × r²</div>', unsafe_allow_html=True)
    st.markdown("""
    - **L** = luas lingkaran
    - **π (pi)** = 22/7 atau 3,14
    - **r** = jari-jari lingkaran
    - **r²** = r × r
    """)
    st.markdown("### 2. Memilih nilai π")
    st.markdown("""
    - Gunakan **π = 22/7** jika jari-jari atau diameter yang diketahui merupakan kelipatan 7, karena perhitungannya lebih mudah.
    - Gunakan **π = 3,14** untuk ukuran yang tidak cocok menggunakan 22/7.
    - Jika diameter diketahui, hitung **r = d ÷ 2** terlebih dahulu.
    """)
    st.warning("Ingat: L = π × r² adalah rumus luas. Rumus 2 × π × r digunakan untuk menghitung keliling.")
    st.markdown("### 3. Visualisasi interaktif")
    radius = st.slider("Geser untuk mengubah jari-jari (cm)", 1, 20, 7, key="materi_radius")
    pi_choice = st.radio("Pilih nilai π", ["22/7", "3,14"], horizontal=True, key="materi_pi")
    pi_value = 22 / 7 if pi_choice == "22/7" else 3.14
    area = pi_value * radius ** 2
    left, right = st.columns(2)
    with left:
        draw_circle(radius, True)
    with right:
        st.markdown("### Hitung bersama")
        st.write(f"Jari-jari: **{radius} cm**")
        st.write(f"L = π × r × r")
        st.write(f"L = {pi_choice} × {radius} × {radius}")
        st.success(f"Luas = {fmt_num(area)} cm²")
    st.markdown("### 4. Contoh soal kontekstual")
    with st.expander("🍽️ Contoh A — Piring bundar"):
        st.write("Piring memiliki jari-jari 7 cm. Tentukan luas permukaannya.")
        st.write("Diketahui: r = 7 cm. Ditanya: L.")
        st.latex(r"L = \frac{22}{7}\times 7\times 7 = 154\text{ cm}^2")
    with st.expander("🍕 Contoh B — Pizza"):
        st.write("Pizza berdiameter 20 cm. Tentukan luasnya.")
        st.write("Diketahui: d = 20 cm. Ditanya: L. Cari jari-jari: r = 20 ÷ 2 = 10 cm.")
        st.latex(r"L = 3{,}14\times 10\times 10 = 314\text{ cm}^2")
    with st.expander("🌳 Contoh C — Taman bundar"):
        st.write("Taman memiliki jari-jari 14 m. Karena 14 kelipatan 7, gunakan π = 22/7.")
        st.latex(r"L = \frac{22}{7}\times 14\times 14 = 616\text{ m}^2")
    st.markdown("### 5. Video belajar")
    st.write("Tambahkan tautan video YouTube yang sudah dipilih guru. Ganti tautan contoh berikut dengan video yang sesuai.")
    youtube_url = st.text_input("Tautan YouTube", value="https://www.youtube.com/results?search_query=luas+lingkaran+kelas+6+SD")
    if youtube_url.startswith("https://"):
        st.link_button("▶️ Buka video pembelajaran", youtube_url)
    st.caption("Video akan terbuka di YouTube. Pastikan tautan sudah diperiksa guru sebelum digunakan.")
    if st.button("✅ Materi sudah dipelajari", type="primary"):
        mark_complete(screen)
        st.success("Bagian materi inti ditandai selesai.")
    nav_buttons()

# ---------- LATIHAN SOAL ----------
elif screen == "Latihan Soal":
    # Reset nilai widget dilakukan sebelum widget dibuat agar tidak bentrok dengan Streamlit.
    if st.session_state.get("reset_quiz_widgets", False):
        for q in QUESTIONS:
            st.session_state.pop(f"input_{q['id']}", None)
        for key in ["essay_known", "essay_asked", "essay_pi", "essay_operation", "essay_work", "essay_conclusion"]:
            st.session_state.pop(key, None)
        st.session_state.reset_quiz_widgets = False
    hero("✏️ Latihan Soal", "Ada soal hitungan, pilihan ganda, pilihan ganda kompleks, dan soal esai kontekstual.")
    st.info("Untuk soal hitungan, tulis angka saja. Untuk pilihan ganda kompleks, pilih semua jawaban yang benar. Skor otomatis menghitung 6 soal objektif; esai dinilai dengan panduan langkah.")
    with st.form("quiz_form"):
        st.markdown("### Bagian A — Pilihan dan hitungan")
        user_answers = {}
        for i, q in enumerate(QUESTIONS, start=1):
            st.markdown(f"**{i}. {q['question']}**")
            if q.get("visual"):
                draw_circle(10 if q["id"] == "q4" else 14, True)
            if q["type"] == "number":
                user_answers[q["id"]] = st.number_input(
                    f"Jawaban ({q.get('unit', 'angka')})",
                    min_value=0.0, max_value=100000000.0, step=1.0,
                    key=f"input_{q['id']}"
                )
            elif q["type"] == "single":
                user_answers[q["id"]] = st.radio(
                    "Pilih satu jawaban:", q["options"],
                    index=None, key=f"input_{q['id']}"
                )
            elif q["type"] == "multi":
                user_answers[q["id"]] = st.multiselect(
                    "Pilih semua jawaban yang benar:", q["options"],
                    key=f"input_{q['id']}"
                )
            st.divider()

        st.markdown("### Bagian B — Esai kontekstual")
        st.markdown("**7.** Sebuah taman berbentuk lingkaran memiliki diameter 28 meter. Pengelola ingin menanami seluruh permukaan taman dengan rumput. Berapa luas daerah yang akan ditanami rumput?")
        st.caption("Petunjuk: tuliskan informasi yang diketahui, apa yang ditanyakan, rumus/operasi yang digunakan, langkah perhitungan, dan kesimpulan.")
        essay_known = st.text_area("a. Diketahui", key="essay_known", placeholder="Contoh: diameter taman = ...")
        essay_asked = st.text_input("b. Ditanya", key="essay_asked", placeholder="Apa yang harus dicari?")
        essay_pi = st.radio("c. Nilai π yang kamu pilih", ["22/7", "3,14"], horizontal=True, key="essay_pi")
        essay_operation = st.selectbox(
            "d. Operasi/langkah pertama yang digunakan",
            ["Pakai diameter langsung ke rumus luas", "Bagi diameter dengan 2 untuk mencari jari-jari", "Kalikan diameter dengan 2"],
            key="essay_operation"
        )
        essay_work = st.text_area("e. Langkah perhitungan", key="essay_work", placeholder="Tuliskan rumus dan perhitunganmu...")
        essay_conclusion = st.text_area("f. Kesimpulan", key="essay_conclusion", placeholder="Jadi, luas taman adalah ...")
        submitted = st.form_submit_button("🔎 Periksa Jawaban", type="primary")

    if submitted:
        results = []
        correct_count = 0
        for q in QUESTIONS:
            given = user_answers.get(q["id"])
            if q["type"] == "number":
                correct = math.isclose(float(given or 0), float(q["answer"]), abs_tol=0.01)
            elif q["type"] == "single":
                correct = given == q["options"][q["answer"]]
            else:
                correct = set(given or []) == {q["options"][idx] for idx in q["answer"]}
            results.append({"question": q, "given": given, "correct": correct})
            if correct:
                correct_count += 1
        score = round(correct_count / len(QUESTIONS) * 100)
        st.session_state.quiz_score = score
        st.session_state.quiz_results = results
        st.session_state.quiz_submitted = True
        st.session_state.answers = user_answers
        mark_complete("Latihan Soal")

        # Penilaian esai bersifat panduan otomatis sederhana, bukan penilaian bahasa secara penuh.
        essay_checks = {
            "Diketahui mencantumkan diameter 28": "28" in essay_known and ("diameter" in essay_known.lower() or "d" in essay_known.lower()),
            "Operasi pertama mencari jari-jari": essay_operation == "Bagi diameter dengan 2 untuk mencari jari-jari",
            "Memilih π = 22/7": essay_pi == "22/7",
            "Langkah perhitungan memuat hasil 616": "616" in essay_work.replace(".", ""),
            "Kesimpulan menyebut hasil 616": "616" in essay_conclusion,
        }
        st.session_state.essay_checks = essay_checks

    if st.session_state.quiz_submitted:
        st.markdown("## 📊 Hasil latihan")
        score = st.session_state.quiz_score
        m1, m2 = st.columns(2)
        m1.metric("Skor soal objektif", f"{score}/100")
        m2.metric("Jawaban benar", f"{sum(x['correct'] for x in st.session_state.quiz_results)}/{len(QUESTIONS)}")
        st.progress(score / 100)
        if score >= 80:
            st.success("🎉 Hebat! Kamu sudah menguasai banyak bagian materi.")
        elif score >= 60:
            st.info("🌱 Bagus, terus berlatih. Baca pembahasan untuk bagian yang masih keliru.")
        else:
            st.warning("💪 Jangan menyerah! Pelajari kembali materi inti, lalu coba lagi.")

        st.markdown("### Pembahasan setiap soal")
        for item in st.session_state.quiz_results:
            q = item["question"]
            with st.expander(("✅ Benar — " if item["correct"] else "❌ Belum tepat — ") + q["question"]):
                if item["correct"]:
                    st.success("Jawabanmu benar!")
                    st.audio(make_tone(True), format="audio/wav")
                else:
                    st.error("Jawabanmu belum tepat. Tidak apa-apa, pelajari langkah berikut.")
                    st.audio(make_tone(False), format="audio/wav")
                st.write(q["explanation"])
                if not item["correct"]:
                    st.markdown("**Rekomendasi belajar:** buka menu **Materi Inti**, lalu pelajari bagian rumus, pemilihan π, dan perubahan diameter menjadi jari-jari.")
                    st.link_button("📚 Cari video penjelasan luas lingkaran", "https://www.youtube.com/results?search_query=luas+lingkaran+kelas+6+SD")
        st.markdown("### Rubrik pemeriksaan esai")
        st.caption("Pemeriksaan esai di bawah ini hanya mengecek beberapa kata/angka penting. Guru tetap perlu menilai penalaran dan penulisan siswa.")
        for criterion, passed in st.session_state.get("essay_checks", {}).items():
            st.write(("✅ " if passed else "🔎 ") + criterion)
        if st.button("🔁 Ulangi latihan", type="primary"):
            st.session_state.quiz_submitted = False
            st.session_state.answers = {}
            st.session_state.quiz_results = []
            st.session_state.reset_quiz_widgets = True
            st.rerun()
    nav_buttons()

# ---------- REFLEKSI ----------
elif screen == "Refleksi":
    hero("💭 Refleksi Belajar", "Pikirkan apa yang sudah kamu pahami dan bagian yang masih menantang.")
    with st.form("reflection_form"):
        understanding = st.radio(
            "1. Seberapa paham kamu tentang luas lingkaran?",
            ["😊 Sudah paham", "🙂 Cukup paham", "🤔 Masih perlu latihan"],
            index=None,
        )
        hard_part = st.selectbox(
            "2. Bagian mana yang paling menantang?",
            ["Memahami jari-jari dan diameter", "Memilih nilai π", "Menggunakan rumus luas",
             "Mengubah diameter menjadi jari-jari", "Menyelesaikan soal cerita",
             "Memilih lebih dari satu jawaban", "Menulis langkah esai", "Tidak ada, semuanya cukup mudah"],
            index=None, placeholder="Pilih salah satu",
        )
        useful = st.radio(
            "3. Apakah gambar dan contoh sehari-hari membantumu?",
            ["Sangat membantu", "Cukup membantu", "Belum membantu"], index=None,
        )
        next_step = st.text_area("4. Apa yang ingin kamu pelajari atau latih lagi?")
        reflection_submit = st.form_submit_button("💾 Simpan Refleksi", type="primary")
    if reflection_submit:
        st.session_state.reflection = {
            "understanding": understanding,
            "hard_part": hard_part,
            "useful": useful,
            "next_step": next_step,
        }
        mark_complete("Refleksi")
        st.success("Refleksi tersimpan selama sesi aplikasi ini. Terima kasih sudah belajar! 🌼")
    if st.session_state.reflection:
        st.markdown("### Ringkasan refleksimu")
        st.write(f"**Pemahaman:** {st.session_state.reflection.get('understanding') or 'Belum diisi'}")
        st.write(f"**Bagian menantang:** {st.session_state.reflection.get('hard_part') or 'Belum diisi'}")
        st.write(f"**Manfaat gambar:** {st.session_state.reflection.get('useful') or 'Belum diisi'}")
        if st.session_state.reflection.get("next_step"):
            st.write(f"**Rencana berikutnya:** {st.session_state.reflection['next_step']}")
    if st.button("✅ Tandai refleksi selesai", type="primary"):
        mark_complete("Refleksi")
        st.success("Refleksi ditandai selesai.")
    nav_buttons()

# ---------- FOOTER ----------
st.divider()
st.caption("Modul pembelajaran interaktif • Luas Lingkaran • Kelas VI SD/MI")
st.caption("Data progres, jawaban, dan refleksi disimpan sementara selama sesi aplikasi berjalan.")
