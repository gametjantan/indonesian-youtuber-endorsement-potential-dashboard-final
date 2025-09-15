import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import ast

# Page config
st.set_page_config(
    page_title="Rekomendasi Potensi Endorsement YouTuber",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-header {
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
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .landing-container {
        text-align: center;
        padding: 5rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);

        display: flex;              
        flex-direction: column;     
        align-items: center;        
        justify-content: center;   
    }
    .landing-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .landing-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    .landing-description {
        font-size: 1.1rem;
        margin: 0 auto 3rem; /* auto kiri-kanan, bawah 3rem */
        text-align: center;
        max-width: 800px;
        line-height: 1.6;
    }
    .feature-card {
        background: white;
        color: #333;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem;
        text-align: center;
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if os.path.exists('saw_results.csv'):
        try:
            df = pd.read_csv('saw_results.csv')
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    else:
        st.error("❌ File 'saw_results.csv' tidak ditemukan!")
        st.info("💡 Silakan jalankan Google Colab notebook terlebih dahulu untuk generate data.")
        return None

def format_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:,.0f}"

def create_ranking_chart(df_filtered, top_n=15):
    top_channels = df_filtered.head(top_n)
    fig = px.bar(
        top_channels,
        x='rank',
        y='saw_score',
        color='genre',
        hover_data=['channel_title', 'avg_view_count', 'subscriber_count'],
        title=f"Top {top_n} Channel - Ranking Potensi Endorsement",
        labels={'saw_score': 'SAW Score', 'rank': 'Ranking'}
    )
    fig.update_layout(
        height=500,
        showlegend=True,
        title_font_size=16,
        title_x=0.5,
        xaxis_title="Ranking",
        yaxis_title="SAW Score"
    )
    return fig

def create_genre_analysis_chart(df):
    genre_stats = df.groupby('genre').agg({
        'saw_score': ['mean', 'count', 'std'],
        'avg_view_count': 'mean',
        'subscriber_count': 'mean'
    }).round(4)
    genre_stats.columns = ['avg_score', 'count', 'std_score', 'avg_views', 'avg_subscribers']
    genre_stats = genre_stats.reset_index().sort_values('avg_score', ascending=False)

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Rata-rata Skor SAW per Genre', 'Jumlah Channel per Genre'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    fig.add_trace(
        go.Bar(
            x=genre_stats['genre'],
            y=genre_stats['avg_score'],
            name='Avg SAW Score',
            marker_color='lightblue',
            text=genre_stats['avg_score'].round(3),
            textposition='outside'
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(
            x=genre_stats['genre'],
            y=genre_stats['count'],
            name='Channel Count',
            marker_color='lightcoral',
            text=genre_stats['count'],
            textposition='outside'
        ),
        row=1, col=2
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        title_text="Analisis per Genre",
        title_x=0.5
    )
    return fig, genre_stats

def create_criteria_radar_chart(df, channel_title):
    channel_data = df[df['channel_title'] == channel_title].iloc[0]
    criteria = ['avg_view_count', 'avg_like_count', 'avg_comment_count', 
                'avg_watch_time','avg_engagement_rate', 'subscriber_count']
    normalized_values = []
    for criterion in criteria:
        max_val = df[criterion].max()
        normalized_val = channel_data[criterion] / max_val if max_val > 0 else 0
        normalized_values.append(normalized_val)
    criteria_labels = [
        'Avg Views',
        'Avg Likes', 
        'Avg Comments',
        'Avg Watch Time',
        'Engagement Rate',
        'Subscribers'
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=criteria_labels,
        fill='toself',
        name=channel_title,
        line_color='rgb(102, 126, 234)'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=f"Profil Kriteria: {channel_title}",
        title_x=0.5,
        height=400
    )
    return fig

def landing_page():
    st.markdown("""
    <div class="landing-container">
        <h1 class="landing-title">🎯 YouTube Endorsement Analyzer</h1>
        <p class="landing-subtitle">Sistem Rekomendasi Potensi Endorsement YouTuber</p>
        <p class="landing-description">
            Platform analisis canggih yang menggunakan metode SAW (Simple Additive Weighting) 
            untuk mengevaluasi potensi endorsement channel YouTube berdasarkan multiple kriteria 
            seperti engagement rate, view count, subscriber count, dan metrik lainnya.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### ✨ Fitur Utama")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Analisis Multi-Kriteria</h3>
            <p>Evaluasi comprehensive menggunakan 6 kriteria utama dengan bobot yang telah dioptimalkan menggunakan metode ROC.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏆</div>
            <h3>Ranking Otomatis</h3>
            <p>Sistem ranking otomatis berdasarkan SAW score untuk mengidentifikasi channel dengan potensi endorsement tertinggi.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Visualisasi Interaktif</h3>
            <p>Dashboard interaktif dengan berbagai chart dan grafik untuk analisis yang lebih mendalam dan insight yang actionable.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 Kriteria Analisis")
        st.markdown("""
        - **Engagement Rate (40.83%)** - Tingkat interaksi audience
        - **Average Watch Time (24.17%)** - Durasi rata-rata menonton
        - **Average Views (15.83%)** - Jumlah views rata-rata
        - **Subscribers (10.28%)** - Jumlah subscriber
        - **Average Likes (6.11%)** - Rata-rata likes per video
        - **Average Comments (2.78%)** - Rata-rata komentar per video
        """)
    with col2:
        st.markdown("### 📋 Yang Bisa Anda Lakukan")
        st.markdown("""
        - 🔍 **Filter berdasarkan genre** untuk analisis spesifik
        - 📊 **Lihat ranking channel** berdasarkan potensi endorsement
        - 📈 **Analisis performa per genre** dan statistik detail
        - 🎬 **Eksplorasi top videos** dari setiap channel
        - 📥 **Download hasil analisis** dalam format CSV
        - 🕸️ **Analisis radar chart** untuk profil channel detail
        """)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Mulai Analisis Sekarang", use_container_width=True):
            st.session_state.page = "dashboard"
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><em>Dikembangkan dengan metode SAW untuk memberikan rekomendasi endorsement yang akurat dan objektif</em></p>
    </div>
    """, unsafe_allow_html=True)

def dashboard_page():
    if st.button("← Kembali ke Landing Page", key="back_button"):
        st.session_state.page = "landing"
    st.markdown('<h1 class="main-header">Sistem Rekomendasi Potensi Endorsement YouTuber</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analisis Metrik dan Engagement Menggunakan Metode SAW (Simple Additive Weighting)</p>', unsafe_allow_html=True)
    df = load_data()
    if df is None:
        st.stop()
    st.sidebar.header("🔧 Filter & Pengaturan")
    selected_genres = st.sidebar.multiselect(
        "Pilih Genre:",
        options=df['genre'].unique(),
        default=df['genre'].unique(),
        help="Pilih satu atau lebih genre untuk dianalisis"
    )
    top_n = st.sidebar.slider(
        "Jumlah Top Channel:",
        min_value=5,
        max_value=50,
        value=15,
        step=5,
        help="Pilih jumlah channel teratas yang ingin ditampilkan"
    )
    st.sidebar.markdown("### 📊 Kriteria SAW")
    st.sidebar.markdown("""
    **Bobot ROC Prioritas Kriteria:**
    - 📈 Engagement Rate: 40,83%
    - 👀 Avg Watch Time: 24,17%
    - 🎥 Avg Views: 15,83%
    - 👥 Subscribers: 10,28%
    - ❤️ Avg Likes: 6,11%
    - 💬 Avg Comments: 2,78%
    """)
    if selected_genres:
        df_filtered = df[df['genre'].isin(selected_genres)].copy()
    else:
        df_filtered = df.copy()
    if len(df_filtered) == 0:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
        return
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="📊 Total Channel",
            value=len(df_filtered),
            delta=f"{len(selected_genres)} genre"
        )
    with col2:
        best_channel = df_filtered.iloc[0]
        st.metric(
            label="🏆 Channel Terbaik",
            value=best_channel['channel_title'],
            delta=f"Score: {best_channel['saw_score']:.4f}"
        )
    with col3:
        avg_score = df_filtered['saw_score'].mean()
        st.metric(
            label="📈 Rata-rata Skor",
            value=f"{avg_score:.4f}",
            delta=f"Range: {df_filtered['saw_score'].min():.3f}-{df_filtered['saw_score'].max():.3f}"
        )
    with col4:
        total_avg_views = df_filtered['avg_view_count'].sum()
        st.metric(
            label="👀 Total Avg Views",
            value=format_number(total_avg_views),
            delta=f"Avg: {format_number(df_filtered['avg_view_count'].mean())}"
        )
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        ranking_fig = create_ranking_chart(df_filtered, top_n)
        st.plotly_chart(ranking_fig, use_container_width=True)
    with col2:
        st.subheader(f"🏆 Top {min(10, len(df_filtered))} Channel")
        top_channels = df_filtered.head(10)[['rank', 'channel_title', 'genre', 'saw_score']]
        display_df = top_channels.copy()
        display_df['saw_score'] = display_df['saw_score'].round(4)
        display_df.columns = ['Rank', 'Channel', 'Genre', 'Score']
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=350)
    st.subheader("📊 Analisis per Genre")
    genre_fig, genre_stats = create_genre_analysis_chart(df_filtered)
    st.plotly_chart(genre_fig, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Statistik Genre")
        st.dataframe(genre_stats[['genre', 'avg_score', 'count', 'std_score']].round(4), use_container_width=True, hide_index=True)
    with col2:
        st.subheader("🔍 Channel Detail Analysis")
        selected_channel = st.selectbox(
            "Pilih Channel untuk Analisis Detail:",
            options=df_filtered['channel_title'].tolist(),
            help="Pilih channel untuk melihat profil kriteria detail"
        )
        if selected_channel:
            radar_fig = create_criteria_radar_chart(df_filtered, selected_channel)
            st.plotly_chart(radar_fig, use_container_width=True)
            st.markdown("#### 🎬 Top Videos")
            channel_data = df_filtered[df_filtered['channel_title'] == selected_channel].iloc[0]
            try:
                top_video_titles = ast.literal_eval(channel_data['top_video_titles'])
                top_video_views = ast.literal_eval(channel_data['top_video_views'])
                top_video_links = ast.literal_eval(channel_data['top_video_links'])
                for i in range(len(top_video_titles)):
                    st.markdown(f"""
                    - **{top_video_titles[i]}**
                      - Views: {format_number(top_video_views[i])}
                      - Link: [Watch Here]({top_video_links[i]})
                    """)
            except (ValueError, SyntaxError):
                st.warning(f"Data video tidak dapat diparsing dengan benar untuk channel {selected_channel}.")
    st.subheader("📋 Data Lengkap")
    display_columns = st.multiselect(
        "Pilih kolom yang ingin ditampilkan:",
        options=['rank', 'channel_title', 'genre', 'saw_score', 'avg_view_count', 
                'avg_like_count', 'avg_comment_count', 'avg_watch_time', 'avg_engagement_rate', 'subscriber_count',
                'top_video_titles', 'top_video_views', 'top_video_links'],
        default=['rank', 'channel_title', 'genre', 'saw_score', 'avg_view_count', 'subscriber_count']
    )
    if display_columns:
        display_data = df_filtered[display_columns].copy()
        numeric_columns = ['saw_score', 'avg_view_count', 'avg_like_count', 
                          'avg_comment_count', 'avg_watch_time', 'avg_engagement_rate', 'subscriber_count', 'top_video_views']
        for col in numeric_columns:
            if col in display_data.columns:
                if col == 'saw_score' or col == 'avg_engagement_rate':
                    display_data[col] = display_data[col].round(4)
                elif col == 'top_video_views':
                    display_data[col] = display_data[col].apply(lambda x: [f"{v:,.0f}" for v in ast.literal_eval(x)] if isinstance(x, str) else x)
                else:
                    display_data[col] = display_data[col].apply(lambda x: f"{x:,.0f}")
        st.dataframe(display_data, use_container_width=True, hide_index=True, height=400)
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f"youtube_endorsement_analysis_{len(selected_genres)}_genres.csv",
            mime="text/csv"
        )
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>Sistem Rekomendasi Potensi Endorsement YouTuber</strong></p>
        <p>Menggunakan Metode SAW (Simple Additive Weighting) untuk analisis multi-kriteria</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()

if __name__ == "__main__":
    main()
