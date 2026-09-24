import streamlit as st
import pandas as pd
import random

# Sayfa Yapılandırması
st.set_page_config(page_title="Target Football", page_icon="⚽", layout="centered")

# Hareketli Gradient Arka Plan & Canlı Açık Mavi Tema
st.markdown("""
<style>
    /* Hareketli Arka Plan Gradyan Animasyonu */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #0d1e30, #1e242c) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 12s ease infinite !important;
        color: #f8fafc !important;
    }
    
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main-title {
        font-size: 44px;
        font-weight: 900;
        font-style: italic;
        color: #38bdf8 !important;
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }
    .sub-title {
        text-align: center;
        color: #94a3b8 !important;
        font-size: 16px;
        margin-bottom: 35px;
    }

    /* Giriş Menüsü Açık Mavi Kare Kart Butonlar */
    div.stButton > button[key="btn_market"], div.stButton > button[key="btn_height"] {
        background: linear-gradient(135deg, #38bdf8, #0284c7) !important;
        background-color: #0284c7 !important;
        color: #041017 !important;
        border: none !important;
        border-radius: 20px !important;
        aspect-ratio: 1 / 1 !important;
        height: auto !important;
        width: 100% !important;
        max-width: 210px !important;
        margin: 0 auto 20px auto !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 8px 24px rgba(56, 189, 248, 0.35) !important;
        padding: 16px !important;
    }

    div.stButton > button[key="btn_market"]:hover, div.stButton > button[key="btn_height"]:hover {
        background: linear-gradient(135deg, #7dd3fc, #0ea5e9) !important;
        background-color: #0ea5e9 !important;
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 28px rgba(56, 189, 248, 0.5) !important;
    }

    div.stButton > button[key="btn_market"] p, div.stButton > button[key="btn_height"] p {
        color: #041017 !important;
        font-size: 19px !important;
        font-weight: 800 !important;
        white-space: pre-wrap !important;
        line-height: 1.5 !important;
        text-align: center !important;
    }

    /* En Üstteki Menüye Dön Butonu */
    div.stButton > button[key="btn_top_menu"] {
        background: rgba(36, 43, 53, 0.8) !important;
        color: #94a3b8 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        padding: 6px 14px !important;
        box-shadow: none !important;
        margin-top: 0px !important;
        width: auto !important;
    }
    div.stButton > button[key="btn_top_menu"]:hover {
        background: #334155 !important;
        color: #38bdf8 !important;
        border-color: #38bdf8 !important;
        transform: none !important;
    }

    /* Diğer Standart Butonlar */
    div.stButton > button:not([key="btn_market"]):not([key="btn_height"]):not([key="btn_top_menu"]) {
        width: 100% !important;
        background: linear-gradient(135deg, #38bdf8, #0284c7) !important;
        color: #041017 !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        border: none !important;
        font-size: 17px !important;
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
        margin-top: 10px !important;
    }

    div.stButton > button:not([key="btn_market"]):not([key="btn_height"]):not([key="btn_top_menu"]):hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(56, 189, 248, 0.5) !important;
    }

    /* Kart Panelleri */
    .target-card {
        background: rgba(39, 48, 60, 0.85) !important;
        backdrop-filter: blur(8px);
        border: 2px solid #3b4758 !important;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .target-number {
        font-size: 46px;
        font-weight: 900;
        color: #38bdf8;
        line-height: 1.1;
        margin: 8px 0;
    }
    .score-card {
        background: rgba(39, 48, 60, 0.85) !important;
        backdrop-filter: blur(8px);
        border: 1px solid #3b4758 !important;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        margin-bottom: 12px;
    }
    .score-val {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
        margin: 4px 0;
    }

    /* Input Alanları */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: rgba(39, 48, 60, 0.9) !important;
        border: 1px solid #3b4758 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="input"] input {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Veriyi oku
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_players.csv')

try:
    df = load_data()
except Exception:
    st.error("cleaned_players.csv bulunamadı!")
    st.stop()

# Oyun Hafızası
if "stage" not in st.session_state:
    st.session_state.stage = "menu"
    st.session_state.game_mode = None
    st.session_state.p1_name = "Oyuncu 1"
    st.session_state.p2_name = "Oyuncu 2"
    st.session_state.target = 0
    st.session_state.turn = 1
    st.session_state.p1_picks = []
    st.session_state.p2_picks = []

# 1. EKRAN: GİRİŞ MENÜSÜ
if st.session_state.stage == "menu":
    st.markdown('<div class="main-title">TARGET FOOTBALL</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Oynamak istediğiniz modu seçin:</div>', unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 1.2, 1])

    with center_col:
        if st.button("💰\n\nPiyasa Tahmin", key="btn_market"):
            st.session_state.game_mode = "market"
            st.session_state.stage = "settings"
            st.rerun()

        if st.button("📏\n\nBoy Tahmin", key="btn_height"):
            st.session_state.game_mode = "height"
            st.session_state.stage = "settings"
            st.rerun()

# 2. EKRAN: LOBİ
elif st.session_state.stage == "settings":
    mode_title = "PİYASA DEĞERİ" if st.session_state.game_mode == "market" else "BOY TAHMİNİ"
    st.markdown(f'<div class="main-title">{mode_title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Oyuncu isimlerini belirleyin:</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        p1_input = st.text_input("1. Oyuncu Adı", value=st.session_state.p1_name)
    with c2:
        p2_input = st.text_input("2. Oyuncu Adı", value=st.session_state.p2_name)

    st.write("")
    if st.button("🎮 Oyunu Başlat"):
        st.session_state.p1_name = p1_input.strip() if p1_input.strip() else "Oyuncu 1"
        st.session_state.p2_name = p2_input.strip() if p2_input.strip() else "Oyuncu 2"

        if st.session_state.game_mode == "market":
            st.session_state.target = random.randint(30, 350) * 1_000_000
        else:
            pool = df.dropna(subset=['height_in_cm'])
            sample_sum = pool.sample(5)['height_in_cm'].sum()
            st.session_state.target = int(sample_sum * random.uniform(0.97, 1.03))

        st.session_state.turn = 1
        st.session_state.p1_picks = []
        st.session_state.p2_picks = []
        st.session_state.stage = "game"
        st.rerun()

    if st.button("← Ana Menüye Dön"):
        st.session_state.stage = "menu"
        st.rerun()

# 3. EKRAN: OYUN ALANI
elif st.session_state.stage == "game":
    top_col1, _ = st.columns([1, 4])
    with top_col1:
        if st.button("← Ana Menü", key="btn_top_menu"):
            st.session_state.stage = "menu"
            st.rerun()

    is_market = (st.session_state.game_mode == "market")
    metric_col = 'market_value_in_eur' if is_market else 'height_in_cm'
    unit = "€" if is_market else "cm"
    
    target_display = f"{st.session_state.target:,} {unit}"
    if is_market:
        target_display += f" ({st.session_state.target // 1_000_000}M €)"

    title_label = f"HEDEF TOPLAM ({unit})"

    st.markdown(f"""
    <div class="target-card">
        <div style="font-size: 26px;">🎯</div>
        <div class="target-number">{target_display}</div>
        <div style="font-weight: 800; font-size: 16px; letter-spacing: 1px; color: #94a3b8;">{title_label}</div>
        <div style="color: #64748b; font-size: 13px; margin-top: 5px;">5'er futbolcu seçip hedefe en çok yaklaşan kazanır</div>
    </div>
    """, unsafe_allow_html=True)

    p1_total = sum(x['val'] for x in st.session_state.p1_picks)
    p2_total = sum(x['val'] for x in st.session_state.p2_picks)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="score-card">
            <div style="color: #94a3b8; font-size: 15px; font-weight: bold;">{st.session_state.p1_name} ({len(st.session_state.p1_picks)}/5)</div>
            <div class="score-val">{p1_total:,} {unit}</div>
            <div style="color: #64748b; font-size: 13px;">Kalan Fark: {abs(st.session_state.target - p1_total):,} {unit}</div>
        </div>
        """, unsafe_allow_html=True)
        for p in st.session_state.p1_picks:
            st.markdown(f"<span style='color:#94a3b8;'>• {p['name']}</span>: <b>{p['val']:,} {unit}</b>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="score-card">
            <div style="color: #94a3b8; font-size: 15px; font-weight: bold;">{st.session_state.p2_name} ({len(st.session_state.p2_picks)}/5)</div>
            <div class="score-val">{p2_total:,} {unit}</div>
            <div style="color: #64748b; font-size: 13px;">Kalan Fark: {abs(st.session_state.target - p2_total):,} {unit}</div>
        </div>
        """, unsafe_allow_html=True)
        for p in st.session_state.p2_picks:
            st.markdown(f"<span style='color:#94a3b8;'>• {p['name']}</span>: <b>{p['val']:,} {unit}</b>", unsafe_allow_html=True)

    st.write("---")
    curr_player = st.session_state.p1_name if st.session_state.turn == 1 else st.session_state.p2_name
    st.markdown(f"### Sıradaki Oyuncu: <span style='color: #38bdf8;'>{curr_player}</span>", unsafe_allow_html=True)

    pool_df = df.dropna(subset=['market_value_in_eur']) if is_market else df.dropna(subset=['height_in_cm'])
    used_names = [x['name'] for x in st.session_state.p1_picks + st.session_state.p2_picks]
    selectable_names = pool_df[~pool_df['name'].isin(used_names)]['name'].tolist()

    selected_player = st.selectbox("Futbolcu arayın veya seçin:", options=[""] + selectable_names)

    if st.button("⚽ Futbolcuyu Kadroya Ekle"):
        if selected_player:
            val = int(df[df['name'] == selected_player][metric_col].iloc[0])
            pick_item = {"name": selected_player, "val": val}

            if st.session_state.turn == 1:
                st.session_state.p1_picks.append(pick_item)
                st.session_state.turn = 2
            else:
                st.session_state.p2_picks.append(pick_item)
                st.session_state.turn = 1

            if len(st.session_state.p1_picks) == 5 and len(st.session_state.p2_picks) == 5:
                st.session_state.stage = "result"

            st.rerun()
        else:
            st.warning("Lütfen bir futbolcu seçin!")

# 4. EKRAN: MAÇ SONUCU
elif st.session_state.stage == "result":
    st.markdown('<div class="main-title">MAÇ SONUCU 🏆</div>', unsafe_allow_html=True)

    is_market = (st.session_state.game_mode == "market")
    unit = "€" if is_market else "cm"

    p1_total = sum(x['val'] for x in st.session_state.p1_picks)
    p2_total = sum(x['val'] for x in st.session_state.p2_picks)
    diff1 = abs(st.session_state.target - p1_total)
    diff2 = abs(st.session_state.target - p2_total)

    if diff1 < diff2:
        winner = f"🎉 KAZANAN: {st.session_state.p1_name}!"
    elif diff2 < diff1:
        winner = f"🎉 KAZANAN: {st.session_state.p2_name}!"
    else:
        winner = "🤝 DOSTLUK KAZANDI (BERABERE)!"

    st.markdown(f"<h2 style='text-align: center; color: #38bdf8;'>{winner}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Ortak Hedef: <b>{st.session_state.target:,} {unit}</b></p>", unsafe_allow_html=True)

    res_c1, res_c2 = st.columns(2)
    with res_c1:
        st.markdown(f"""
        <div class="score-card">
            <div style="font-weight: bold; font-size: 18px;">{st.session_state.p1_name}</div>
            <div class="score-val" style="color: #38bdf8;">{p1_total:,} {unit}</div>
            <div style="color: #94a3b8;">Hedefe Fark: <b>{diff1:,} {unit}</b></div>
        </div>
        """, unsafe_allow_html=True)
        for p in st.session_state.p1_picks:
            st.write(f"• **{p['name']}**: {p['val']:,} {unit}")

    with res_c2:
        st.markdown(f"""
        <div class="score-card">
            <div style="font-weight: bold; font-size: 18px;">{st.session_state.p2_name}</div>
            <div class="score-val" style="color: #38bdf8;">{p2_total:,} {unit}</div>
            <div style="color: #94a3b8;">Hedefe Fark: <b>{diff2:,} {unit}</b></div>
        </div>
        """, unsafe_allow_html=True)
        for p in st.session_state.p2_picks:
            st.write(f"• **{p['name']}**: {p['val']:,} {unit}")

    st.write("")
    if st.button("🔄 Yeni Maç Başlat"):
        st.session_state.stage = "menu"
        st.rerun()
