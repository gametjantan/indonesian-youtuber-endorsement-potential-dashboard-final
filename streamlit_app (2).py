import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import ast

# Page configuration (gabungan)
st.set_page_config(
    page_title="Indonesian YouTuber Endorsement Dashboard",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (gabungan dan disesuaikan)
st.markdown("""
<style>
    /* Landing page styles */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF0000;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .feature-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .saw-explanation {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #FF0000;
        margin: 2rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .cta-button {
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .cta-button:hover {
        transform: translateY(-2px);
    }

    /* Dashboard styles */
    .main-header-dashboard {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f1f1f;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sub-header-dashboard {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('saw_results.csv')
        return df
    except FileNotFoundError:
        st.error("File saw_results.csv tidak ditemukan!")
        return pd.DataFrame()

# Landing page function
def landing_page():
    """Landing page dengan informasi tentang aplikasi"""
    
    # Hero Section
    st.markdown("""
        <div class="main-header">
            📺 Indonesian YouTuber<br>Endorsement Dashboard
        </div>
        <div class="sub-header">
            Sistem Penilaian Potensi Endorsement YouTuber Indonesia<br>
            Menggunakan Metode Simple Additive Weighting (SAW)
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SAW Method Explanation
    st.markdown("""
        <div class="saw-explanation">
            <h3>🎯 Tentang Metode SAW (Simple Additive Weighting)</h3>
            <p>
                Sistem ini menggunakan metode SAW untuk menilai potensi endorsement YouTuber Indonesia 
                berdasarkan berbagai kriteria penting:
            </p>
            <ul>
                <li><strong>Average Views:</strong> Rata-rata jumlah views per video</li>
                <li><strong>Average Likes:</strong> Rata-rata jumlah likes per video</li>
                <li><strong>Average Comments:</strong> Rata-rata jumlah komentar per video</li>
                <li><strong>Engagement Rate:</strong> Tingkat interaksi dengan audience</li>
                <li><strong>Subscriber Count:</strong> Jumlah total subscriber</li>
            </ul>
            <p>
                Setiap kriteria memiliki bobot yang telah ditentukan untuk menghasilkan 
                ranking yang objektif dan akurat.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("### ✨ Fitur Utama Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">📊 Analisis Komprehensif</div>
                <div>Visualisasi data lengkap dengan berbagai jenis chart dan grafik interaktif</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🏆 Ranking SAW</div>
                <div>Sistem pemeringkatan berdasarkan metode Simple Additive Weighting</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">📈 Perbandingan YouTuber</div>
                <div>Radar chart untuk membandingkan performa antar YouTuber</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Statistics Preview
    df = load_data()
    if not df.empty:
        st.markdown("### 📈 Statistik Data")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #FF0000;">{len(df)}</h3>
                    <p>Total YouTuber</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_views = df['avg_view_count'].mean()
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #FF0000;">{avg_views:,.0f}</h3>
                    <p>Rata-rata Views</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_subs = df['subscriber_count'].sum()
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #FF0000;">{total_subs:,.0f}</h3>
                    <p>Total Subscribers</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_engagement = df['avg_engagement_rate'].mean()
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #FF0000;">{avg_engagement:.2f}%</h3>
                    <p>Rata-rata Engagement</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to Action
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Masuk ke Dashboard", use_container_width=True, type="primary"):
            st.session_state.page = "dashboard"
            st.experimental_rerun()
    
    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
            <p>Dashboard ini menggunakan data YouTube API untuk menganalisis potensi endorsement</p>
            <p>© 2024 Indonesian YouTuber Endorsement Analysis Dashboard</p>
        </div>
    """, unsafe_allow_html=True)

# Dashboard page function
def dashboard_page():
    """Dashboard utama dengan semua analisis"""
    
    # Sidebar navigation
    st.sidebar.markdown("## 📺 Navigation")
    if st.sidebar.button("⬅️ Kembali ke Landing Page", use_container_width=True):
        st.session_state.page = "landing"
        st.experimental_rerun()
    
    st.sidebar.markdown("---")
    
    # Load data
    df = load_data()
    if df.empty:
        st.warning("Data tidak tersedia untuk ditampilkan di dashboard.")
        return
    
    # Header
    st.markdown("""
        <div class="main-header-dashboard">
            Sistem Rekomendasi Potensi Endorsement YouTuber
        </div>
        <div class="sub-header-dashboard">
            Analisis dan visualisasi performa YouTuber Indonesia menggunakan metode SAW
        </div>
    """, unsafe_allow_html=True)
    
    # Contoh visualisasi: Ranking YouTuber berdasarkan score SAW
    st.markdown("### 🏆 Ranking YouTuber Berdasarkan Skor SAW")
    df_sorted = df.sort_values(by='saw_score', ascending=False)
    st.dataframe(df_sorted[['youtuber_name', 'saw_score']].reset_index(drop=True))
    
    # Visualisasi bar chart top 10 YouTuber
    top10 = df_sorted.head(10)
    fig_bar = px.bar(top10, x='youtuber_name', y='saw_score',
                     labels={'youtuber_name': 'YouTuber', 'saw_score': 'Skor SAW'},
                     title='Top 10 YouTuber Berdasarkan Skor SAW',
                     color='saw_score', color_continuous_scale='Viridis')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Radar chart perbandingan kriteria untuk YouTuber terpilih
    st.markdown("### 📊 Perbandingan Kriteria YouTuber")
    youtuber_list = df['youtuber_name'].tolist()
    selected_youtubers = st.multiselect("Pilih YouTuber untuk dibandingkan (maks 3)", youtuber_list, default=youtuber_list[:3], max_selections=3)
    
    if selected_youtubers:
        categories = ['avg_view_count', 'avg_like_count', 'avg_comment_count', 'avg_engagement_rate', 'subscriber_count']
        categories_labels = ['Views', 'Likes', 'Comments', 'Engagement Rate', 'Subscribers']
        
        fig = go.Figure()
        
        for yt in selected_youtubers:
            row = df[df['youtuber_name'] == yt].iloc[0]
            values = [row[c] for c in categories]
            # Normalisasi nilai agar skala sama (misal min-max scaling)
            min_vals = df[categories].min()
            max_vals = df[categories].max()
            norm_values = [(row[c] - min_vals[c]) / (max_vals[c] - min_vals[c]) if max_vals[c] != min_vals[c] else 0 for c in categories]
            fig.add_trace(go.Scatterpolar(
                r=norm_values,
                theta=categories_labels,
                fill='toself',
                name=yt
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title="Radar Chart Perbandingan Kriteria"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Silakan pilih minimal satu YouTuber untuk dibandingkan.")
    
    # Contoh analisis tambahan bisa ditambahkan di sini

# Initialize session state page
if 'page' not in st.session_state:
    st.session_state.page = "landing"

# Main app logic
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
