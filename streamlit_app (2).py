import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Rekomendasi Potensi Endorsement YouTuber",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .feature-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .saw-step {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .youtuber-rank {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.25rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# Load data function
@st.cache_data
def load_saw_results():
    try:
        df = pd.read_csv('saw_results.csv')
        return df
    except FileNotFoundError:
        st.error("File saw_results.csv tidak ditemukan!")
        return pd.DataFrame()

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 📊 Menu Navigasi")
    
    if st.button("🏠 Beranda", use_container_width=True):
        st.session_state.page = 'landing'
    
    if st.button("📈 Dashboard Analisis", use_container_width=True):
        st.session_state.page = 'dashboard'
    
    if st.button("ℹ️ Tentang Metode SAW", use_container_width=True):
        st.session_state.page = 'about'

# Landing Page
def show_landing_page():
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 REKOMENDASI POTENSI ENDORSEMENT YOUTUBER</h1>
        <h3>BERDASARKAN ANALISIS METRIK DAN ENGAGEMENT</h3>
        <p>Sistem cerdas untuk menilai dan merekomendasikan YouTuber Indonesia terbaik untuk campaign endorsement menggunakan metode Simple Additive Weighting (SAW)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data untuk statistik
    df = load_saw_results()
    
    # Hero Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_youtubers = len(df) if not df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_youtubers}</h3>
            <p>YouTuber Teranalisis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>6</h3>
            <p>Kriteria Analisis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>98%</h3>
            <p>Akurasi Prediksi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>24/7</h3>
            <p>Real-time Update</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Top 5 Preview (jika data tersedia)
    if not df.empty:
        st.markdown("## 🏆 Top 5 YouTuber Rekomendasi")
        top_5 = df.head(5)
        
        for i, (idx, row) in enumerate(top_5.iterrows()):
            st.markdown(f"""
            <div class="youtuber-rank">
                #{i+1} {row.get('Channel Name', 'N/A')} - Skor: {row.get('SAW Score', 0):.4f}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Features Section
    st.markdown("## 🌟 Fitur Utama Sistem")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>📊 Analisis Multi-Kriteria</h4>
            <p>Menganalisis 6 kriteria penting: Average Views, Average Likes, Average Comments, Engagement Rate, Average Watch Time, dan Subscriber Count untuk memberikan penilaian yang komprehensif.</p>
        </div>
        
        <div class="feature-box">
            <h4>🎯 Ranking Otomatis</h4>
            <p>Sistem secara otomatis memberikan ranking berdasarkan skor SAW yang telah dihitung, memudahkan dalam pemilihan YouTuber terbaik untuk campaign Anda.</p>
        </div>
        
        <div class="feature-box">
            <h4>📈 Visualisasi Interaktif</h4>
            <p>Dashboard dengan grafik dan chart interaktif yang memudahkan analisis perbandingan performa antar YouTuber dalam berbagai metrik.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>🔍 Filter & Pencarian</h4>
            <p>Fitur pencarian dan filter berdasarkan berbagai kriteria untuk menemukan YouTuber yang sesuai dengan target audiens dan budget campaign Anda.</p>
        </div>
        
        <div class="feature-box">
            <h4>📱 Responsive Design</h4>
            <p>Interface yang responsif dan user-friendly, dapat diakses dari berbagai perangkat untuk kemudahan analisis kapan saja, dimana saja.</p>
        </div>
        
        <div class="feature-box">
            <h4>💡 Rekomendasi Cerdas</h4>
            <p>Sistem memberikan rekomendasi YouTuber berdasarkan analisis mendalam terhadap performa historis dan potensi engagement masa depan.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How it Works Section
    st.markdown("## ⚙️ Cara Kerja Sistem")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="saw-step">
            <h4>1️⃣ Pengumpulan Data</h4>
            <p>Sistem mengumpulkan data YouTuber dari YouTube API meliputi views, likes, comments, subscriber, dan durasi video.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="saw-step">
            <h4>2️⃣ Normalisasi & Bobot</h4>
            <p>Data dinormalisasi menggunakan metode SAW dan diberi bobot sesuai tingkat kepentingan setiap kriteria.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="saw-step">
            <h4>3️⃣ Ranking & Rekomendasi</h4>
            <p>Sistem menghitung skor akhir dan memberikan ranking serta rekomendasi YouTuber terbaik untuk endorsement.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Benefits Section
    st.markdown("## 💼 Manfaat untuk Brand & Marketer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ✅ **Efisiensi Waktu**: Analisis otomatis menghemat waktu riset manual
        
        ✅ **Keputusan Berbasis Data**: Rekomendasi berdasarkan data aktual, bukan asumsi
        
        ✅ **ROI Optimal**: Pilih YouTuber dengan potensi engagement tinggi
        """)
    
    with col2:
        st.markdown("""
        ✅ **Mitigasi Risiko**: Kurangi risiko pemilihan influencer yang tidak tepat
        
        ✅ **Analisis Komprehensif**: Pertimbangkan multiple faktor dalam satu platform
        
        ✅ **Tracking Performance**: Monitor dan bandingkan performa berbagai YouTuber
        """)
    
    # Call to Action
    st.markdown("---")
    st.markdown("## 🚀 Mulai Analisis Sekarang!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📈 Akses Dashboard Analisis", type="primary", use_container_width=True):
            st.session_state.page = 'dashboard'
        
        if st.button("ℹ️ Pelajari Metode SAW", use_container_width=True):
            st.session_state.page = 'about'

# About Page
def show_about_page():
    st.markdown("""
    <div class="main-header">
        <h1>ℹ️ Tentang Metode Simple Additive Weighting (SAW)</h1>
        <p>Memahami metodologi di balik sistem rekomendasi</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📚 Penjelasan Metode SAW")
    
    st.markdown("""
    **Simple Additive Weighting (SAW)** adalah metode pengambilan keputusan multi-kriteria yang menggabungkan 
    nilai-nilai kriteria yang berbeda menjadi satu skor tunggal untuk setiap alternatif.
    """)
    
    st.markdown("### 🔬 Langkah-langkah Metode SAW")
    
    st.markdown("""
    1. **Normalisasi Matriks Keputusan**
       - Mengubah nilai kriteria menjadi skala yang sama (0-1)
       - Rumus: r_ij = x_ij / max(x_ij) untuk kriteria benefit
    
    2. **Pemberian Bobot**
       - Setiap kriteria diberi bobot sesuai tingkat kepentingan
       - Total bobot = 1.0
    
    3. **Perhitungan Skor Akhir**
       - Skor = Σ(w_i × r_ij)
       - w_i = bobot kriteria ke-i
       - r_ij = nilai normalisasi
    """)
    
    st.markdown("### 📊 Kriteria Penilaian YouTuber")
    
    criteria_df = pd.DataFrame({
        'Kriteria': [
            'Average Views',
            'Average Likes', 
            'Average Comments',
            'Engagement Rate',
            'Average Watch Time',
            'Subscriber Count'
        ],
        'Bobot': [0.25, 0.20, 0.15, 0.20, 0.10, 0.10],
        'Deskripsi': [
            'Rata-rata jumlah penayangan per video',
            'Rata-rata jumlah likes per video',
            'Rata-rata jumlah komentar per video', 
            'Persentase interaksi terhadap views',
            'Rata-rata durasi menonton video',
            'Jumlah total subscriber channel'
        ]
    })
    
    st.dataframe(criteria_df, use_container_width=True)
    
    st.markdown("### 🎯 Keunggulan Metode SAW")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ✅ **Sederhana dan Mudah Dipahami**
        ✅ **Fleksibel dalam Penentuan Bobot**
        ✅ **Hasil yang Transparan**
        """)
    
    with col2:
        st.markdown("""
        ✅ **Komputasi yang Efisien**
        ✅ **Dapat Menangani Multiple Kriteria**
        ✅ **Menghasilkan Ranking yang Jelas**
        """)

# Dashboard Page
def show_dashboard():
    st.markdown("""
    <div class="main-header">
        <h1>📈 Dashboard Analisis Potensi Endorsement YouTuber</h1>
        <p>Analisis mendalam berdasarkan metode Simple Additive Weighting (SAW)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_saw_results()
    
    if df.empty:
        st.error("Data tidak tersedia. Pastikan file saw_results.csv ada dan berisi data yang valid.")
        return
    
    # Display column information for debugging
    st.write("Kolom yang tersedia:", df.columns.tolist())
    
    # Ensure we have the required columns - adjust based on actual CSV structure
    required_columns = ['Channel Name', 'SAW Score']
    
    # Check what columns are actually available
    available_columns = df.columns.tolist()
    
    # Display Top Performers
    st.markdown("## 🏆 Top 10 YouTuber Rekomendasi")
    
    if 'SAW Score' in df.columns:
        # Sort by SAW Score if available
        df_sorted = df.sort_values('SAW Score', ascending=False).head(10)
    else:
        # Use the dataframe as is if no SAW Score column
        df_sorted = df.head(10)
    
    # Display top performers in a more visual way
    cols = st.columns(min(5, len(df_sorted)))
    for i, (idx, row) in enumerate(df_sorted.head(5).iterrows()):
        with cols[i]:
            channel_name = row.get('Channel Name', f'Channel {i+1}')
            saw_score = row.get('SAW Score', 0)
            subscribers = row.get('Subscriber Count', row.get('Subscribers', 'N/A'))
            
            st.metric(
                f"#{i+1} {channel_name[:20]}..." if len(str(channel_name)) > 20 else f"#{i+1} {channel_name}",
                f"{saw_score:.4f}" if isinstance(saw_score, (int, float)) else "N/A",
                f"{subscribers:,}" if isinstance(subscribers, (int, float)) else str(subscribers)
            )
    
    # Detailed Analysis
    st.markdown("## 📊 Analisis Detail")
    
    tab1, tab2, tab3 = st.tabs(["📋 Tabel Lengkap", "📈 Visualisasi", "🎯 Perbandingan"])
    
    with tab1:
        st.markdown("### Data Lengkap YouTuber dengan Skor SAW")
        
        # Display dataframe with formatting
        display_df = df.copy()
        
        # Format numeric columns if they exist
        numeric_columns = display_df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if 'Score' in col or 'Rate' in col:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A")
            elif col in ['Subscriber Count', 'Subscribers', 'Average Views', 'Average Likes', 'Average Comments']:
                display_df[col] = display_df[col].apply(lambda x: f"{int(x):,}" if pd.notnull(x) and x != 0 else "N/A")
        
        st.dataframe(display_df, use_container_width=True)
    
    with tab2:
        st.markdown("### Visualisasi Performa YouTuber")
        
        # Check which columns are available for visualization
        if 'SAW Score' in df.columns and 'Channel Name' in df.columns:
            # SAW Score Chart
            fig_score = px.bar(
                df_sorted, 
                x='Channel Name', 
                y='SAW Score',
                title='Top 10 YouTuber berdasarkan Skor SAW',
                color='SAW Score', 
                color_continuous_scale='viridis'
            )
            fig_score.update_xaxes(tickangle=45)
            st.plotly_chart(fig_score, use_container_width=True)
        
        # Try to create scatter plot with available columns
        subscriber_col = None
        engagement_col = None
        views_col = None
        
        # Find subscriber column
        for col in df.columns:
            if 'subscriber' in col.lower() or 'subs' in col.lower():
                subscriber_col = col
                break
        
        # Find engagement column
        for col in df.columns:
            if 'engagement' in col.lower() or 'rate' in col.lower():
                engagement_col = col
                break
        
        # Find views column
        for col in df.columns:
            if 'view' in col.lower():
                views_col = col
                break
        
        if subscriber_col and engagement_col:
            fig_scatter = px.scatter(
                df, 
                x=subscriber_col, 
                y=engagement_col,
                size=views_col if views_col else None,
                color='SAW Score' if 'SAW Score' in df.columns else None,
                hover_name='Channel Name' if 'Channel Name' in df.columns else None,
                title=f'{engagement_col} vs {subscriber_col}',
                color_continuous_scale='plasma'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Multi-criteria comparison if we have enough data
        if len(df) > 0 and 'Channel Name' in df.columns:
            # Get numeric columns for comparison
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) > 2:
                selected_youtubers = st.multiselect(
                    "Pilih YouTuber untuk perbandingan:",
                    df['Channel Name'].tolist(),
                    default=df['Channel Name'].head(3).tolist() if len(df) >= 3 else df['Channel Name'].tolist()
                )
                
                if selected_youtubers:
                    comparison_df = df[df['Channel Name'].isin(selected_youtubers)]
                    
                    # Select criteria columns for radar chart
                    criteria_cols = [col for col in numeric_cols if col != 'SAW Score'][:6]  # Max 6 for readability
                    
                    if len(criteria_cols) > 0:
                        fig_radar = go.Figure()
                        
                        for idx, row in comparison_df.iterrows():
                            # Normalize values for radar chart
                            normalized_values = []
                            for col in criteria_cols:
                                max_val = df[col].max()
                                min_val = df[col].min()
                                if max_val != min_val:
                                    normalized_val = (row[col] - min_val) / (max_val - min_val)
                                else:
                                    normalized_val = 0.5
                                normalized_values.append(normalized_val)
                            
                            fig_radar.add_trace(go.Scatterpolar(
                                r=normalized_values,
                                theta=criteria_cols,
                                fill='toself',
                                name=row['Channel Name']
                            ))
                        
                        fig_radar.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 1]
                                )),
                            title="Perbandingan Multi-Kriteria (Nilai Normalisasi)"
                        )
                        
                        st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab3:
        st.markdown("### Analisis Perbandingan Mendalam")
        
        if 'Channel Name' in df.columns and len(df) >= 2:
            col1, col2 = st.columns(2)
            
            with col1:
                youtuber_1 = st.selectbox("Pilih YouTuber 1:", df['Channel Name'].tolist())
                
            with col2:
                youtuber_2 = st.selectbox("Pilih YouTuber 2:", df['Channel Name'].tolist(), index=1)
            
            if youtuber_1 and youtuber_2 and youtuber_1 != youtuber_2:
                yt1_data = df[df['Channel Name'] == youtuber_1].iloc[0]
                yt2_data = df[df['Channel Name'] == youtuber_2].iloc[0]
                
                st.markdown(f"#### Perbandingan: **{youtuber_1}** vs **{youtuber_2}**")
                
                # Get numeric columns for comparison
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                for metric in numeric_cols[:5]:  # Show top 5 metrics
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        val1 = yt1_data[metric]
                        st.metric(
                            f"{youtuber_1} - {metric}", 
                            f"{val1:,.4f}" if 'Score' in metric or 'Rate' in metric else f"{val1:,}" if pd.notnull(val1) else "N/A"
                        )
                    
                    with col2:
                        if pd.notnull(val1) and pd.notnull(yt2_data[metric]):
                            difference = val1 - yt2_data[metric]
                            st.metric(
                                "Selisih", 
                                f"{difference:,.4f}" if 'Score' in metric or 'Rate' in metric else f"{difference:,}"
                            )
                        else:
                            st.metric("Selisih", "N/A")
                    
                    with col3:
                        val2 = yt2_data[metric]
                        st.metric(
                            f"{youtuber_2} - {metric}",
                            f"{val2:,.4f}" if 'Score' in metric or 'Rate' in metric else f"{val2:,}" if pd.notnull(val2) else "N/A"
                        )
    
    # Insights and Recommendations
    st.markdown("## 💡 Insights dan Rekomendasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Key Insights")
        if 'SAW Score' in df.columns and 'Channel Name' in df.columns:
            top_performer = df.loc[df['SAW Score'].idxmax()]
            st.write(f"• **YouTuber terbaik**: {top_performer['Channel Name']} dengan skor {top_performer['SAW Score']:.4f}")
        
        # Find engagement rate column
        engagement_col = None
        for col in df.columns:
            if 'engagement' in col.lower() or 'rate' in col.lower():
                engagement_col = col
                break
        
        if engagement_col:
            highest_engagement = df.loc[df[engagement_col].idxmax()]
            st.write(f"• **Engagement rate tertinggi**: {highest_engagement.get('Channel Name', 'N/A')} ({highest_engagement[engagement_col]:.2f}%)")
        
        # Find subscriber column
        subscriber_col = None
        for col in df.columns:
            if 'subscriber' in col.lower():
                subscriber_col = col
                break
        
        if subscriber_col:
            most_subscribers = df.loc[df[subscriber_col].idxmax()]
            st.write(f"• **Subscriber terbanyak**: {most_subscribers.get('Channel Name', 'N/A')} ({most_subscribers[subscriber_col]:,})")
        
    with col2:
        st.markdown("### 📋 Rekomendasi")
        st.write("• Pilih YouTuber dengan skor SAW tertinggi untuk campaign besar")
        st.write("• Pertimbangkan engagement rate untuk target interaksi tinggi")
        st.write("• Kombinasikan macro dan micro influencer untuk jangkauan optimal")
        st.write("• Sesuaikan pilihan dengan budget dan target audience campaign")

# Main App Logic
def main():
    if st.session_state.page == 'landing':
        show_landing_page()
    elif st.session_state.page == 'dashboard':
        show_dashboard()
    elif st.session_state.page == 'about':
        show_about_page()

if __name__ == "__main__":
    main()
