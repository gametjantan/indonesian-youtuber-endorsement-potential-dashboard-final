import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Konfigurasi halaman
st.set_page_config(
    page_title="Indonesian YouTuber Endorsement Potential Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

def show_landing_page():
    """Tampilkan landing page"""
    
    # Header dengan gradient background effect menggunakan CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #4ECDC4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    .btn-dashboard {
        background: linear-gradient(90deg, #4ECDC4, #44A08D);
        color: white;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .btn-dashboard:hover {
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Indonesian YouTuber Endorsement Potential Dashboard</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Sistem Penilaian Potensi Endorsement YouTuber Indonesia Menggunakan Metode SAW
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 📊 Tentang Sistem")
        st.markdown("""
        Dashboard ini adalah sistem analisis komprehensif untuk menilai potensi endorsement 
        YouTuber Indonesia berdasarkan performa konten mereka. Sistem menggunakan metode 
        **Simple Additive Weighting (SAW)** untuk memberikan penilaian objektif terhadap 
        berbagai metrik performa.
        
        ### 🎯 Tujuan Sistem
        - **Objektifitas**: Memberikan penilaian berbasis data yang akurat
        - **Efisiensi**: Membantu brands menemukan YouTuber yang tepat
        - **Transparansi**: Metodologi penilaian yang jelas dan terukur
        - **Analisis Mendalam**: Insights comprehensive tentang performa creator
        """)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Data Metrics</h3>
            <p>Rata-rata Views, Likes, Comments, Engagement Rate, Watch Time, Subscriber</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card" style="margin-top: 1rem;">
            <h3>⚖️ SAW Method</h3>
            <p>Simple Additive Weighting untuk penilaian objektif</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features Section
    st.markdown("## ✨ Fitur Utama Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🏆 Ranking System</h4>
            <p>Sistem perangkingan berdasarkan skor SAW yang memberikan urutan YouTuber dengan potensi endorsement terbaik.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Visualisasi Data</h4>
            <p>Grafik interaktif untuk memahami performa dan distribusi metrik dengan lebih mudah.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🔍 Analisis Mendalam</h4>
            <p>Analisis korelasi antar metrik dan insights tentang faktor-faktor yang mempengaruhi performa.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>⚙️ Kustomisasi Bobot</h4>
            <p>Pengaturan bobot kriteria yang dapat disesuaikan dengan kebutuhan kampanye endorsement.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📱 Export Data</h4>
            <p>Kemampuan export hasil analisis dalam format CSV untuk keperluan reporting lebih lanjut.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Filter & Search</h4>
            <p>Fitur pencarian dan filter untuk menemukan YouTuber dengan kriteria spesifik yang diinginkan.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Methodology Section
    st.markdown("## 🧮 Metodologi SAW")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Kriteria Penilaian:
        
        1. **Average Views** - Rata-rata penayangan video
        2. **Average Likes** - Rata-rata jumlah like
        3. **Average Comments** - Rata-rata komentar
        4. **Engagement Rate** - Tingkat interaksi audience
        5. **Average Watch Time** - Durasi tonton rata-rata
        6. **Subscriber Count** - Jumlah subscriber
        
        ### Proses Perhitungan:
        1. **Normalisasi** data menggunakan min-max scaling
        2. **Pembobotan** sesuai kepentingan kriteria
        3. **Agregasi** skor untuk mendapatkan nilai akhir
        """)
    
    with col2:
        # Sample calculation visualization
        sample_data = {
            'Kriteria': ['Avg Views', 'Avg Likes', 'Avg Comments', 'Engagement Rate', 'Watch Time', 'Subscribers'],
            'Bobot': [0.25, 0.20, 0.15, 0.20, 0.10, 0.10],
            'Normalisasi': [0.85, 0.78, 0.92, 0.88, 0.75, 0.95]
        }
        
        df_sample = pd.DataFrame(sample_data)
        df_sample['Skor Tertimbang'] = df_sample['Bobot'] * df_sample['Normalisasi']
        
        fig = px.bar(df_sample, x='Kriteria', y='Skor Tertimbang', 
                     title="Contoh Perhitungan Skor SAW",
                     color='Skor Tertimbang',
                     color_continuous_scale='viridis')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # CTA Section
    st.markdown("## 🚀 Mulai Analisis")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; color: white;">
            <h3>Siap untuk menganalisis potensi endorsement YouTuber Indonesia?</h3>
            <p>Akses dashboard lengkap dengan data real-time dan analisis mendalam</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Button to go to dashboard
        if st.button("🎯 Buka Dashboard", key="open_dashboard", help="Akses dashboard analisis"):
            st.session_state.show_dashboard = True
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>📧 Dashboard ini menilai potensi endorsement YouTuber Indonesia dengan metode SAW berbasis data YouTube API</p>
        <p><strong>Indonesian YouTuber Endorsement Potential Dashboard</strong> | Powered by Streamlit & Plotly</p>
    </div>
    """, unsafe_allow_html=True)

# Fungsi dashboard yang sudah ada (tidak diubah)
def load_data():
    """Memuat data dari file CSV"""
    try:
        df = pd.read_csv('saw_results.csv')
        return df
    except FileNotFoundError:
        st.error("File saw_results.csv tidak ditemukan. Pastikan file tersedia di direktori yang sama.")
        return None
    except Exception as e:
        st.error(f"Error saat memuat data: {str(e)}")
        return None

def calculate_saw_scores(df, weights):
    """Menghitung skor SAW berdasarkan bobot yang diberikan"""
    # Kolom untuk normalisasi (benefit criteria - semakin tinggi semakin baik)
    criteria_columns = ['avg_views', 'avg_likes', 'avg_comments', 'engagement_rate', 'avg_watch_time_minutes', 'subscriber_count']
    
    # Normalisasi data menggunakan min-max normalization
    df_normalized = df.copy()
    for col in criteria_columns:
        if col in df.columns:
            max_val = df[col].max()
            min_val = df[col].min()
            if max_val != min_val:
                df_normalized[f'{col}_norm'] = (df[col] - min_val) / (max_val - min_val)
            else:
                df_normalized[f'{col}_norm'] = 1.0
    
    # Hitung skor SAW
    normalized_columns = [f'{col}_norm' for col in criteria_columns if col in df.columns]
    saw_scores = []
    
    for idx, row in df_normalized.iterrows():
        score = 0
        for i, col in enumerate(normalized_columns):
            if i < len(weights):
                score += weights[i] * row[col]
        saw_scores.append(score)
    
    df['saw_score'] = saw_scores
    return df.sort_values('saw_score', ascending=False).reset_index(drop=True)

def show_dashboard():
    """Tampilkan dashboard utama"""
    
    # Header dashboard
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎬 Indonesian YouTuber Endorsement Potential Dashboard")
        st.markdown("*Sistem Penilaian Potensi Endorsement YouTuber Indonesia Menggunakan Metode SAW*")
    
    with col2:
        if st.button("🏠 Kembali ke Beranda", key="back_to_home"):
            st.session_state.show_dashboard = False
            st.rerun()
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar untuk konfigurasi
    st.sidebar.header("⚙️ Konfigurasi Analisis")
    
    # Pengaturan bobot kriteria
    st.sidebar.subheader("🏋️ Bobot Kriteria")
    st.sidebar.markdown("*Sesuaikan bobot sesuai prioritas kampanye endorsement*")
    
    weight_views = st.sidebar.slider("📈 Average Views", 0.0, 1.0, 0.25, 0.05)
    weight_likes = st.sidebar.slider("👍 Average Likes", 0.0, 1.0, 0.20, 0.05)
    weight_comments = st.sidebar.slider("💬 Average Comments", 0.0, 1.0, 0.15, 0.05)
    weight_engagement = st.sidebar.slider("🎯 Engagement Rate", 0.0, 1.0, 0.20, 0.05)
    weight_watch_time = st.sidebar.slider("⏱️ Average Watch Time", 0.0, 1.0, 0.10, 0.05)
    weight_subscribers = st.sidebar.slider("👥 Subscriber Count", 0.0, 1.0, 0.10, 0.05)
    
    weights = [weight_views, weight_likes, weight_comments, weight_engagement, weight_watch_time, weight_subscribers]
    
    # Normalisasi bobot agar total = 1
    total_weight = sum(weights)
    if total_weight > 0:
        weights = [w/total_weight for w in weights]
    
    st.sidebar.markdown(f"**Total Bobot:** {total_weight:.2f}")
    
    # Filter data
    st.sidebar.subheader("🔍 Filter Data")
    
    # Filter berdasarkan subscriber
    if 'subscriber_count' in df.columns:
        min_subs = st.sidebar.number_input("Minimum Subscribers", min_value=0, value=0, step=1000)
        df = df[df['subscriber_count'] >= min_subs]
    
    # Filter berdasarkan engagement rate
    if 'engagement_rate' in df.columns:
        min_engagement = st.sidebar.slider("Minimum Engagement Rate (%)", 0.0, 100.0, 0.0, 0.1)
        df = df[df['engagement_rate'] >= min_engagement]
    
    # Hitung skor SAW
    df_scored = calculate_saw_scores(df, weights)
    
    # Main dashboard content
    if len(df_scored) == 0:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
        return
    
    # Metrics overview
    st.markdown("## 📊 Overview Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total YouTubers", len(df_scored))
    
    with col2:
        avg_score = df_scored['saw_score'].mean()
        st.metric("Average SAW Score", f"{avg_score:.3f}")
    
    with col3:
        if 'subscriber_count' in df_scored.columns:
            avg_subs = df_scored['subscriber_count'].mean()
            st.metric("Average Subscribers", f"{avg_subs:,.0f}")
    
    with col4:
        if 'engagement_rate' in df_scored.columns:
            avg_engagement = df_scored['engagement_rate'].mean()
            st.metric("Average Engagement", f"{avg_engagement:.2f}%")
    
    # Top performers
    st.markdown("## 🏆 Top 10 YouTuber Berpotensi")
    
    top_10 = df_scored.head(10)
    
    # Tabel ranking
    display_columns = ['channel_name', 'saw_score']
    if 'subscriber_count' in df_scored.columns:
        display_columns.append('subscriber_count')
    if 'engagement_rate' in df_scored.columns:
        display_columns.append('engagement_rate')
    if 'avg_views' in df_scored.columns:
        display_columns.append('avg_views')
    
    # Format data untuk display
    top_10_display = top_10[display_columns].copy()
    top_10_display['Rank'] = range(1, len(top_10_display) + 1)
    top_10_display = top_10_display.set_index('Rank')
    
    # Rename columns for better display
    column_mapping = {
        'channel_name': 'Channel Name',
        'saw_score': 'SAW Score',
        'subscriber_count': 'Subscribers',
        'engagement_rate': 'Engagement Rate (%)',
        'avg_views': 'Avg Views'
    }
    
    top_10_display = top_10_display.rename(columns=column_mapping)
    
    # Format numbers
    if 'SAW Score' in top_10_display.columns:
        top_10_display['SAW Score'] = top_10_display['SAW Score'].apply(lambda x: f"{x:.3f}")
    if 'Subscribers' in top_10_display.columns:
        top_10_display['Subscribers'] = top_10_display['Subscribers'].apply(lambda x: f"{x:,.0f}")
    if 'Engagement Rate (%)' in top_10_display.columns:
        top_10_display['Engagement Rate (%)'] = top_10_display['Engagement Rate (%)'].apply(lambda x: f"{x:.2f}")
    if 'Avg Views' in top_10_display.columns:
        top_10_display['Avg Views'] = top_10_display['Avg Views'].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(top_10_display, use_container_width=True)
    
    # Visualisasi
    st.markdown("## 📈 Visualisasi Data")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SAW Score Distribution", "🎯 Performance Metrics", "📈 Correlation Analysis", "🏆 Top Performers"])
    
    with tab1:
        # Histogram SAW scores
        fig_hist = px.histogram(df_scored, x='saw_score', nbins=20, 
                               title='Distribusi SAW Score',
                               labels={'saw_score': 'SAW Score', 'count': 'Jumlah YouTuber'})
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Box plot
        fig_box = px.box(df_scored, y='saw_score', title='Box Plot SAW Score')
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with tab2:
        # Scatter plots untuk berbagai metrics
        col1, col2 = st.columns(2)
        
        with col1:
            if 'subscriber_count' in df_scored.columns:
                fig_scatter1 = px.scatter(df_scored, x='subscriber_count', y='saw_score',
                                        hover_data=['channel_name'],
                                        title='SAW Score vs Subscriber Count',
                                        labels={'subscriber_count': 'Subscribers', 'saw_score': 'SAW Score'})
                st.plotly_chart(fig_scatter1, use_container_width=True)
        
        with col2:
            if 'engagement_rate' in df_scored.columns:
                fig_scatter2 = px.scatter(df_scored, x='engagement_rate', y='saw_score',
                                        hover_data=['channel_name'],
                                        title='SAW Score vs Engagement Rate',
                                        labels={'engagement_rate': 'Engagement Rate (%)', 'saw_score': 'SAW Score'})
                st.plotly_chart(fig_scatter2, use_container_width=True)
    
    with tab3:
        # Correlation heatmap
        numeric_columns = df_scored.select_dtypes(include=[np.number]).columns
        correlation_data = df_scored[numeric_columns].corr()
        
        fig_heatmap = px.imshow(correlation_data,
                               labels=dict(x="Metrics", y="Metrics", color="Correlation"),
                               title="Correlation Heatmap",
                               aspect="auto")
        fig_heatmap.update_layout(height=500)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab4:
        # Bar chart top performers
        fig_bar = px.bar(top_10, x='channel_name', y='saw_score',
                        title='Top 10 YouTuber Berdasarkan SAW Score',
                        labels={'channel_name': 'Channel Name', 'saw_score': 'SAW Score'})
        fig_bar.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detail analysis
    st.markdown("## 🔍 Detail Analysis")
    
    # Search functionality
    search_term = st.text_input("🔍 Cari YouTuber:", placeholder="Masukkan nama channel...")
    
    if search_term:
        filtered_df = df_scored[df_scored['channel_name'].str.contains(search_term, case=False, na=False)]
        
        if len(filtered_df) > 0:
            st.markdown(f"**Hasil pencarian untuk '{search_term}':**")
            
            for idx, row in filtered_df.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**{row['channel_name']}**")
                    if 'subscriber_count' in row:
                        st.markdown(f"👥 {row['subscriber_count']:,.0f} subscribers")
                
                with col2:
                    st.metric("SAW Score", f"{row['saw_score']:.3f}")
                
                with col3:
                    if 'engagement_rate' in row:
                        st.metric("Engagement", f"{row['engagement_rate']:.2f}%")
                
                st.markdown("---")
        else:
            st.warning(f"Tidak ditemukan YouTuber dengan nama '{search_term}'")
    
    # Export functionality
    st.markdown("## 📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df_scored.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Complete Data (CSV)",
            data=csv,
            file_name=f'youtuber_saw_analysis_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )
    
    with col2:
        top_csv = top_10.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Top 10 Data (CSV)",
            data=top_csv,
            file_name=f'top_10_youtuber_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )

# Main app logic
def main():
    """Fungsi utama aplikasi"""
    
    # Custom CSS untuk styling
    st.markdown("""
    <style>
    .reportview-container {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    h1, h2, h3 {
        color: #2c3e50;
    }
    
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Routing berdasarkan session state
    if st.session_state.show_dashboard:
        show_dashboard()
    else:
        show_landing_page()

if __name__ == "__main__":
    main()
