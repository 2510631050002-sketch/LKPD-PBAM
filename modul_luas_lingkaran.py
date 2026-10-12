import math
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ============================================================
# MODUL PEMBELAJARAN LUAS LINGKARAN - KELAS VI SD/MI
# Jalankan: streamlit run modul_luas_lingkaran.py
# ============================================================

st.set_page_config(
    page_title="Modul Luas Lingkaran | Kelas VI",
    page_icon="⭕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Tema ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background: #F7FAF5; }
    .hero {
        background: linear-gradient(120deg, #DDEFE0 0%, #F5F4D8 100%);
        padding: 1.6rem 1.8rem; border-radius: 22px;
        border: 1px solid #D0E3D1; margin-bottom: 1rem;
    }
    .hero h1 { color: #214D35; margin-bottom: .3rem; }
    .hero p { color: #355B43; font-size: 1.05rem; margin-bottom: 0; }
    .info-card {
        background: white; padding: 1rem 1.1rem; border-radius: 16px;
        border: 1px solid #E0E9DF; margin: .4rem 0;
    }
    .formula {
        background: #E5F1E5; color: #214D35; padding: 1rem;
        border-radius: 14px; text-align: center; font-size: 1.35rem;
        font-weight: 800; margin: .6rem 0;
    }
    .small-note { color: #5A6D5D; font-size: .92rem; }
    div.stButton > button {
        border-radius: 12px; font-weight: 700; border: 1px solid #B8D2BA;
    }
    [data-testid="stMetric"] {
        background: white; padding: 1rem; border-radius: 14px;
        border: 1px solid #E0E9DF;
    }
</style>
""", unsafe_allow_html=True)

# ---------- State ----------
if "completed_sections" not in st.session_state:
    st.session_state.completed_sections = set()
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "reflection" not in st.session_state:
    st.session_state.reflection = {}
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

SECTIONS = [
    "Capaian Pembelajaran",
    "Petunjuk & Pengantar",
    "Materi Inti",
    "Latihan Soal",
    "Refleksi",
]

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ⭕ Modul Matematika")
    st.caption("Kelas VI SD/MI • Luas Lingkaran")
    st.session_state.student_name = st.text_input(
        "Nama siswa (opsional)", value=st.session_state.student_name,
        placeholder="Tulis namamu di sini"
    )
    page = st.radio("Menu modul", SECTIONS, index=0)
    st.divider()
    done_count = len(st.session_state.completed_sections)
    progress = done_count / len(SECTIONS)
    st.markdown("### 📍 Progres Belajar")
    st.progress(progress)
    st.write(f"{done_count} dari {len(SECTIONS)} bagian selesai")
    if st.session_state.quiz_submitted:
        st.metric("Skor latihan", f"{st.session_state.get('quiz_score', 0)}/100")
    st.caption("Pelajari satu bagian demi satu bagian, ya!")

def mark_complete(section):
    st.session_state.completed_sections.add(section)

def show_hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True
    )

def draw_circle(radius=7, show_diameter=False):
    fig, ax = plt.subplots(figsize=(5, 3.6))
    circle = Circle((0, 0), radius, facecolor="#DDEFE0",
                    edgecolor="#2F7047", linewidth=2.5, alpha=0.95)
    ax.add_patch(circle)
    ax.plot([0, radius], [0, 0], color="#D18B2C", linewidth=2.5)
    ax.scatter([0, radius], [0, 0], color=["#2F7047", "#D18B2C"], zorder=3)
    ax.text(radius / 2, 0.35, f"r = {radius:g}", ha="center",
            color="#80531A", fontsize=11, weight="bold")
    if show_diameter:
        ax.plot([-radius, radius], [0, 0], color="#547BBA",
                linewidth=1.8, linestyle="--")
        ax.text(0, -0.55, f"d = {2*radius:g}", ha="center",
                color="#34588A", fontsize=10, weight="bold")
    ax.set_xlim(-radius - 1.3, radius + 1.3)
    ax.set_ylim(-radius - 1.3, radius + 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_alpha(0)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

def fmt_num(value):
    if abs(value - round(value)) < 1e-8:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")

# ---------- Page 1: Capaian ----------
if page == "Capaian Pembelajaran":
    show_hero("🌟 Ayo Belajar Luas Lingkaran!", "Kenali lingkaran dan temukan luasnya melalui benda-benda di sekitar kita.")
    st.markdown("### 🎯 Capaian dan tujuan pembelajaran")
    st.info(
        "Bagian ini dirumuskan sebagai tujuan belajar untuk modul berdasarkan LKPD yang diberikan. "
        "Sesuaikan kembali dengan dokumen Capaian Pembelajaran resmi yang digunakan sekolah."
    )
    st.markdown("""
    Setelah belajar menggunakan modul ini, siswa diharapkan mampu:
    - mengenali jari-jari dan diameter lingkaran;
    - menjelaskan hubungan diameter dengan jari-jari;
    - menggunakan rumus luas lingkaran untuk menyelesaikan masalah sehari-hari;
    - membandingkan luas dua lingkaran dan memeriksa ketepatan penyelesaian;
    - menjelaskan cara menyelesaikan soal dengan bahasa sendiri.
    """)
    st.markdown("### 🧭 Peta belajar")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="info-card">⭕<br><b>Kenali</b><br>Jari-jari dan diameter</div>', unsafe_allow_html=True)
    c2.markdown('<div class="info-card">🧮<br><b>Hitung</b><br>Luas lingkaran</div>', unsafe_allow_html=True)
    c3.markdown('<div class="info-card">💡<br><b>Gunakan</b><br>Dalam kehidupan sehari-hari</div>', unsafe_allow_html=True)
    if st.button("Saya siap belajar! ➜", type="primary"):
        mark_complete("Capaian Pembelajaran")
        st.success("Bagian capaian pembelajaran selesai. Lanjut ke Petunjuk & Pengantar!")

# ---------- Page 2: Petunjuk dan pengantar ----------
elif page == "Petunjuk & Pengantar":
    show_hero("📘 Petunjuk Penggunaan dan Pengantar", "Ikuti langkah-langkahnya dan jangan takut mencoba!")
    st.markdown("### Cara menggunakan modul")
    st.markdown("""
    1. Baca capaian dan tujuan pembelajaran.
    2. Pelajari materi inti secara berurutan.
    3. Amati gambar lingkaran dan contoh perhitungannya.
    4. Kerjakan latihan soal secara mandiri.
    5. Periksa skor, lalu isi refleksi belajar.
    """)
    st.markdown("### Pernah melihat benda berbentuk lingkaran?")
    a, b = st.columns([1, 1])
    with a:
        st.write("Piring, jam dinding, pizza, tutup tempat sampah, dan meja bundar adalah contoh benda yang permukaannya dapat berbentuk lingkaran.")
        st.write("Jika kita ingin mengetahui luas permukaan yang ditutupi benda tersebut, kita dapat menggunakan **luas lingkaran**.")
    with b:
        draw_circle(7, True)
    st.markdown("### Kenali dua bagian penting")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="info-card"><b>Jari-jari (r)</b><br>Jarak dari titik pusat ke tepi lingkaran.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-card"><b>Diameter (d)</b><br>Garis yang melewati titik pusat dan menghubungkan dua titik pada tepi lingkaran.</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula">d = 2 × r &nbsp;&nbsp; dan &nbsp;&nbsp; r = d ÷ 2</div>', unsafe_allow_html=True)
    if st.button("Petunjuk sudah dibaca ✓", type="primary"):
        mark_complete("Petunjuk & Pengantar")
        st.success("Bagian ini selesai!")

# ---------- Page 3: Materi inti ----------
elif page == "Materi Inti":
    show_hero("🧠 Materi Inti: Luas Lingkaran", "Kita pelajari rumusnya pelan-pelan, lalu coba dengan contoh.")
    st.markdown("### 1. Rumus luas lingkaran")
    st.markdown('<div class="formula">L = π × r × r = π × r²</div>', unsafe_allow_html=True)
    st.write("Keterangan:")
    st.markdown("""
    - **L** = luas lingkaran
    - **π (pi)** = 22/7 atau 3,14
    - **r** = jari-jari lingkaran
    - **r²** = r × r
    """)
    st.warning("Ingat: jika yang diketahui diameter, cari jari-jari terlebih dahulu dengan membagi diameter menjadi 2.")
    st.markdown("### 2. Coba ubah jari-jari")
    radius = st.slider("Geser untuk memilih jari-jari (cm)", min_value=1, max_value=20, value=7)
    use_pi = st.radio("Pilih nilai π", ["22/7", "3,14"], horizontal=True)
    pi_value = 22 / 7 if use_pi == "22/7" else 3.14
    area = pi_value * radius * radius
    left, right = st.columns([1, 1])
    with left:
        draw_circle(radius, True)
    with right:
        st.markdown("#### Hitung bersama")
        st.write(f"Jari-jari = {radius} cm")
        st.write(f"L = π × r × r")
        st.write(f"L = {use_pi} × {radius} × {radius}")
        st.success(f"Luas = {fmt_num(area)} cm²")
    st.markdown("### 3. Contoh soal")
    with st.expander("Contoh A — piring berjari-jari 7 cm"):
        st.write("Diketahui r = 7 cm dan π = 22/7.")
        st.latex(r"L = \frac{22}{7} \times 7 \times 7")
        st.latex(r"L = 154\text{ cm}^2")
    with st.expander("Contoh B — pizza berdiameter 20 cm"):
        st.write("Diketahui d = 20 cm. Maka r = 20 ÷ 2 = 10 cm.")
        st.latex(r"L = 3{,}14 \times 10 \times 10")
        st.latex(r"L = 314\text{ cm}^2")
    with st.expander("Contoh C — membandingkan dua lingkaran"):
        st.write("Lingkaran A memiliki r = 7 cm dan lingkaran B memiliki r = 14 cm.")
        st.write("Luas A = 154 cm², sedangkan luas B = 616 cm². Luas B empat kali luas A.")
    if st.button("Materi sudah dipelajari ✓", type="primary"):
        mark_complete("Materi Inti")
        st.success("Bagus! Kamu sudah menyelesaikan materi inti.")

# ---------- Page 4: Latihan ----------
elif page == "Latihan Soal":
    show_hero("✏️ Latihan Soal", "Baca soal dengan teliti. Masukkan jawaban luas dalam satuan persegi.")
    st.write("Gunakan π = 22/7 untuk jari-jari atau diameter kelipatan 7. Untuk soal lain, gunakan π = 3,14.")
    questions = [
        {
            "id": "q1",
            "question": "1. Sebuah piring memiliki jari-jari 7 cm. Berapa luas permukaannya (cm²)?",
            "answer": 154,
            "explanation": "L = 22/7 × 7 × 7 = 154 cm²."
        },
        {
            "id": "q2",
            "question": "2. Jam dinding berbentuk lingkaran memiliki jari-jari 14 cm. Berapa luasnya (cm²)?",
            "answer": 616,
            "explanation": "L = 22/7 × 14 × 14 = 616 cm²."
        },
        {
            "id": "q3",
            "question": "3. Sebuah pizza memiliki diameter 20 cm. Berapa luasnya (cm²)?",
            "answer": 314,
            "explanation": "r = 20 ÷ 2 = 10 cm. L = 3,14 × 10 × 10 = 314 cm²."
        },
        {
            "id": "q4",
            "question": "4. Tutup tempat sampah berbentuk lingkaran berdiameter 28 cm. Berapa luasnya (cm²)?",
            "answer": 616,
            "explanation": "r = 28 ÷ 2 = 14 cm. L = 22/7 × 14 × 14 = 616 cm²."
        },
        {
            "id": "q5",
            "question": "5. Pelindung kipas berbentuk lingkaran berjari-jari 10 cm. Berapa luasnya (cm²)?",
            "answer": 314,
            "explanation": "L = 3,14 × 10 × 10 = 314 cm²."
        },
        {
            "id": "q6",
            "question": "6. Taman berbentuk lingkaran memiliki jari-jari 14 m. Berapa luas taman (m²)?",
            "answer": 616,
            "explanation": "L = 22/7 × 14 × 14 = 616 m²."
        },
        {
            "id": "q7",
            "question": "7. Sebuah kolam berbentuk lingkaran memiliki diameter 20 m. Berapa luasnya (m²)?",
            "answer": 314,
            "explanation": "r = 20 ÷ 2 = 10 m. L = 3,14 × 10 × 10 = 314 m²."
        },
        {
            "id": "q8",
            "question": "8. Lapangan berbentuk lingkaran berdiameter 28 m. Seorang siswa menghitung L = π × d × d. Apakah cara itu benar? Pilih jawaban yang tepat.",
            "choices": [
                "Benar, karena diameter digunakan langsung dalam rumus luas.",
                "Salah, rumus luas memakai jari-jari, yaitu L = π × r × r.",
                "Salah, luas lingkaran selalu sama dengan keliling."
            ],
            "answer": 1,
            "explanation": "Cara itu salah. Diameter harus dibagi 2 terlebih dahulu untuk memperoleh jari-jari. Jika d = 28 m, r = 14 m dan L = 616 m²."
        },
    ]
    with st.form("quiz_form"):
        for q in questions:
            st.markdown(f"**{q['question']}**")
            if "choices" in q:
                value = st.radio(
                    "Pilih jawaban:", q["choices"], index=None,
                    key=q["id"], label_visibility="collapsed"
                )
                st.session_state.answers[q["id"]] = value
            else:
                value = st.number_input(
                    "Jawaban", min_value=0.0, max_value=1000000.0,
                    value=float(st.session_state.answers.get(q["id"], 0.0)),
                    step=1.0, key=q["id"], label_visibility="collapsed"
                )
                st.session_state.answers[q["id"]] = value
            st.divider()
        submitted = st.form_submit_button("Periksa Jawaban dan Hitung Skor", type="primary")
    if submitted:
        score = 0
        results = []
        for q in questions:
            answer = st.session_state.answers.get(q["id"])
            if "choices" in q:
                correct = answer == q["choices"][q["answer"]]
            else:
                try:
                    correct = math.isclose(float(answer), float(q["answer"]), abs_tol=0.01)
                except (TypeError, ValueError):
                    correct = False
            if correct:
                score += 1
            results.append((q, correct, answer))
        st.session_state.quiz_score = round(score / len(questions) * 100)
        st.session_state.quiz_results = results
        st.session_state.quiz_submitted = True
        mark_complete("Latihan Soal")
    if st.session_state.quiz_submitted:
        st.markdown("### 📊 Hasil latihan")
        score = st.session_state.get("quiz_score", 0)
        st.metric("Skor kamu", f"{score}/100")
        st.progress(score / 100)
        if score >= 80:
            st.success("Hebat! Kamu sudah memahami luas lingkaran dengan baik. 🎉")
        elif score >= 60:
            st.info("Bagus! Baca kembali bagian yang masih membingungkan, lalu coba lagi.")
        else:
            st.warning("Tidak apa-apa, terus berlatih ya! Pelajari lagi contoh soal di Materi Inti.")
        st.markdown("### Pembahasan")
        for q, correct, answer in st.session_state.get("quiz_results", []):
            st.markdown(f"**{q['question']}**")
            st.write("✅ Benar!" if correct else "❌ Belum tepat.")
            st.caption(q["explanation"])
        if st.button("Ulangi latihan"):
            st.session_state.quiz_submitted = False
            st.session_state.answers = {}
            st.rerun()

# ---------- Page 5: Refleksi ----------
elif page == "Refleksi":
    show_hero("💭 Refleksi Belajar", "Yuk, pikirkan pengalaman belajarmu hari ini.")
    st.write("Tidak ada jawaban yang perlu ditakuti. Jawablah dengan jujur agar kamu tahu bagian yang sudah dipahami.")
    with st.form("reflection_form"):
        understanding = st.radio(
            "1. Seberapa paham kamu tentang luas lingkaran?",
            ["😊 Sudah paham", "🙂 Cukup paham", "🤔 Masih perlu latihan"],
            index=None
        )
        hard_part = st.selectbox(
            "2. Bagian mana yang paling menantang?",
            [
                "Memahami jari-jari dan diameter",
                "Memilih nilai π",
                "Menggunakan rumus luas lingkaran",
                "Mengubah diameter menjadi jari-jari",
                "Menyelesaikan soal cerita",
                "Tidak ada, semuanya cukup mudah",
            ],
            index=None,
            placeholder="Pilih salah satu"
        )
        useful = st.radio(
            "3. Apakah contoh benda sehari-hari membantu kamu belajar?",
            ["Sangat membantu", "Cukup membantu", "Belum membantu"],
            index=None
        )
        message = st.text_area(
            "4. Tuliskan hal yang kamu pelajari atau pertanyaanmu:",
            placeholder="Contoh: Saya belajar bahwa diameter adalah dua kali jari-jari..."
        )
        reflection_submit = st.form_submit_button("Simpan Refleksi", type="primary")
    if reflection_submit:
        st.session_state.reflection = {
            "understanding": understanding,
            "hard_part": hard_part,
            "useful": useful,
            "message": message,
        }
        mark_complete("Refleksi")
        st.success("Refleksi tersimpan selama sesi aplikasi ini. Terima kasih sudah belajar! 🌻")
    if st.session_state.reflection:
        st.markdown("### Ringkasan refleksimu")
        st.write(f"**Pemahaman:** {st.session_state.reflection.get('understanding') or 'Belum diisi'}")
        st.write(f"**Bagian menantang:** {st.session_state.reflection.get('hard_part') or 'Belum diisi'}")
        st.write(f"**Manfaat contoh:** {st.session_state.reflection.get('useful') or 'Belum diisi'}")
        if st.session_state.reflection.get("message"):
            st.write(f"**Catatan:** {st.session_state.reflection['message']}")

# ---------- Footer ----------
st.divider()
st.caption("Modul pembelajaran interaktif • Luas Lingkaran • Kelas VI SD/MI")
st.caption("Catatan: progres dan jawaban disimpan selama sesi aplikasi berjalan, bukan sebagai data permanen.")
