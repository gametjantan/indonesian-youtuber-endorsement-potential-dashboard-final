import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configure page
st.set_page_config(
    page_title="Indonesian YouTuber Endorsement Dashboard",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('saw_results.csv')
        return df
    except FileNotFoundError:
        st.error("File saw_results.csv tidak ditemukan!")
        return pd.DataFrame()

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
    
    # Add hero image or video thumbnail placeholder
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://storage.googleapis.com/workspace-0f70711f-8b4e-4d94-86f1-2a93ccde5887/image/c637900d-fb6b-48fd-8346-d7b1cbd18722.png", 
                caption="Dashboard Analytics YouTube Indonesia")
    
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
            st.markdown("""
                <div class="metric-card">
                    <h3 style="color: #FF0000;">{}</h3>
                    <p>Total YouTuber</p>
                </div>
            """.format(len(df)), unsafe_allow_html=True)
        
        with col2:
            avg_views = df['Average_Views'].mean()
            st.markdown("""
                <div class="metric-card">
                    <h3 style="color: #FF0000;">{:,.0f}</h3>
                    <p>Rata-rata Views</p>
                </div>
            """.format(avg_views), unsafe_allow_html=True)
        
        with col3:
            total_subs = df['Subscriber_Count'].sum()
            st.markdown("""
                <div class="metric-card">
                    <h3 style="color: #FF0000;">{:,.0f}</h3>
                    <p>Total Subscribers</p>
                </div>
            """.format(total_subs), unsafe_allow_html=True)
        
        with col4:
            avg_engagement = df['Engagement_Rate'].mean()
            st.markdown("""
                <div class="metric-card">
                    <h3 style="color: #FF0000;">{:.2f}%</h3>
                    <p>Rata-rata Engagement</p>
                </div>
            """.format(avg_engagement), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to Action
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Masuk ke Dashboard", use_container_width=True, type="primary"):
            st.session_state.page = "dashboard"
            st.rerun()
    
    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
            <p>Dashboard ini menggunakan data YouTube API untuk menganalisis potensi endorsement</p>
            <p>© 2024 Indonesian YouTuber Endorsement Analysis Dashboard</p>
        </div>
    """, unsafe_allow_html=True)

def dashboard_page():
    """Dashboard utama dengan semua analisis"""
    
    # Sidebar navigation
    st.sidebar.markdown("## 📺 Navigation")
    if st.sidebar.button("⬅️ Kembali ke Landing Page", use_container_width=True):
        st.session_state.page = "landing"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.error("Tidak ada data untuk ditampilkan!")
        return
    
    # Dashboard header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #FF0000;">📊 Dashboard Analisis YouTuber</h1>
            <p style="font-size: 1.2rem; color: #666;">Ranking Potensi Endorsement berdasarkan Metode SAW</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Key metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total YouTuber",
            value=len(df),
            delta="Teranalisis"
        )
    
    with col2:
        avg_score = df['SAW_Score'].mean()
        st.metric(
            label="Rata-rata SAW Score",
            value=f"{avg_score:.3f}",
            delta=f"{(avg_score/df['SAW_Score'].max()*100):.1f}% dari maksimal"
        )
    
    with col3:
        top_engagement = df.nlargest(1, 'Engagement_Rate')['Engagement_Rate'].iloc[0]
        st.metric(
            label="Engagement Rate Tertinggi",
            value=f"{top_engagement:.2f}%",
            delta="Terbaik"
        )
    
    with col4:
        total_avg_views = df['Average_Views'].sum()
        st.metric(
            label="Total Average Views",
            value=f"{total_avg_views:,.0f}",
            delta="Akumulatif"
        )
    
    st.markdown("---")
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Ranking SAW", "📊 Analisis Perbandingan", "📈 Top Videos", "📋 Data Detail"])
    
    with tab1:
        st.subheader("🏆 Ranking Potensi Endorsement (SAW Method)")
        
        # Top 10 YouTuber
        top_10 = df.nlargest(10, 'SAW_Score')
        
        # Bar chart for top 10
        fig_ranking = px.bar(
            top_10, 
            x='SAW_Score', 
            y='Channel_Name',
            orientation='h',
            title="Top 10 YouTuber dengan Score SAW Tertinggi",
            labels={'SAW_Score': 'SAW Score', 'Channel_Name': 'Channel'},
            color='SAW_Score',
            color_continuous_scale='Reds'
        )
        fig_ranking.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig_ranking, use_container_width=True)
        
        # Detailed ranking table
        st.subheader("📋 Tabel Ranking Lengkap")
        ranking_df = df.copy()
        ranking_df['Rank'] = range(1, len(ranking_df) + 1)
        ranking_df = ranking_df[['Rank', 'Channel_Name', 'SAW_Score', 'Average_Views', 
                               'Average_Likes', 'Average_Comments', 'Engagement_Rate', 'Subscriber_Count']]
        
        # Format numbers for better readability
        ranking_df['Average_Views'] = ranking_df['Average_Views'].apply(lambda x: f"{x:,.0f}")
        ranking_df['Average_Likes'] = ranking_df['Average_Likes'].apply(lambda x: f"{x:,.0f}")
        ranking_df['Average_Comments'] = ranking_df['Average_Comments'].apply(lambda x: f"{x:,.0f}")
        ranking_df['Engagement_Rate'] = ranking_df['Engagement_Rate'].apply(lambda x: f"{x:.2f}%")
        ranking_df['Subscriber_Count'] = ranking_df['Subscriber_Count'].apply(lambda x: f"{x:,.0f}")
        ranking_df['SAW_Score'] = ranking_df['SAW_Score'].apply(lambda x: f"{x:.4f}")
        
        st.dataframe(ranking_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("📊 Analisis Perbandingan YouTuber")
        
        # YouTuber selector for comparison
        selected_youtubers = st.multiselect(
            "Pilih YouTuber untuk dibandingkan (maksimal 5):",
            options=df['Channel_Name'].tolist(),
            default=df.nlargest(5, 'SAW_Score')['Channel_Name'].tolist()[:5],
            max_selections=5
        )
        
        if selected_youtubers:
            comparison_df = df[df['Channel_Name'].isin(selected_youtubers)]
            
            # Radar Chart
            fig_radar = go.Figure()
            
            # Normalize data for radar chart (0-1 scale)
            metrics = ['Average_Views', 'Average_Likes', 'Average_Comments', 'Engagement_Rate', 'Subscriber_Count']
            metric_labels = ['Avg Views', 'Avg Likes', 'Avg Comments', 'Engagement Rate', 'Subscribers']
            
            for idx, channel in enumerate(selected_youtubers):
                channel_data = comparison_df[comparison_df['Channel_Name'] == channel].iloc[0]
                
                # Normalize each metric (min-max normalization)
                normalized_values = []
                for metric in metrics:
                    min_val = df[metric].min()
                    max_val = df[metric].max()
                    normalized = (channel_data[metric] - min_val) / (max_val - min_val) if max_val != min_val else 0
                    normalized_values.append(normalized)
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=normalized_values + [normalized_values[0]],  # Close the radar
                    theta=metric_labels + [metric_labels[0]],
                    fill='toself',
                    name=channel,
                    line_color=px.colors.qualitative.Set1[idx % len(px.colors.qualitative.Set1)]
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1])
                ),
                showlegend=True,
                title="Perbandingan Performa YouTuber (Normalized)",
                height=600
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Comparison metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Views comparison
                fig_views = px.bar(
                    comparison_df,
                    x='Channel_Name',
                    y='Average_Views',
                    title="Perbandingan Average Views",
                    color='Average_Views',
                    color_continuous_scale='Blues'
                )
                fig_views.update_xaxis(tickangle=45)
                st.plotly_chart(fig_views, use_container_width=True)
            
            with col2:
                # Engagement rate comparison
                fig_engagement = px.bar(
                    comparison_df,
                    x='Channel_Name',
                    y='Engagement_Rate',
                    title="Perbandingan Engagement Rate",
                    color='Engagement_Rate',
                    color_continuous_scale='Greens'
                )
                fig_engagement.update_xaxis(tickangle=45)
                st.plotly_chart(fig_engagement, use_container_width=True)
    
    with tab3:
        st.subheader("📈 Top Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top channels by views
            top_views = df.nlargest(10, 'Average_Views')
            fig_top_views = px.bar(
                top_views,
                x='Average_Views',
                y='Channel_Name',
                orientation='h',
                title="Top 10 - Highest Average Views",
                color='Average_Views',
                color_continuous_scale='Reds'
            )
            fig_top_views.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_top_views, use_container_width=True)
        
        with col2:
            # Top channels by subscribers
            top_subs = df.nlargest(10, 'Subscriber_Count')
            fig_top_subs = px.bar(
                top_subs,
                x='Subscriber_Count',
                y='Channel_Name',
                orientation='h',
                title="Top 10 - Highest Subscriber Count",
                color='Subscriber_Count',
                color_continuous_scale='Blues'
            )
            fig_top_subs.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_top_subs, use_container_width=True)
        
        # Scatter plot analysis
        st.subheader("🔍 Analisis Korelasi")
        
        fig_scatter = px.scatter(
            df,
            x='Average_Views',
            y='Engagement_Rate',
            size='Subscriber_Count',
            color='SAW_Score',
            hover_name='Channel_Name',
            title="Hubungan antara Views, Engagement Rate, dan Subscribers",
            labels={
                'Average_Views': 'Average Views',
                'Engagement_Rate': 'Engagement Rate (%)',
                'Subscriber_Count': 'Subscribers',
                'SAW_Score': 'SAW Score'
            },
            color_continuous_scale='Viridis'
        )
        fig_scatter.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab4:
        st.subheader("📋 Data Lengkap")
        
        # Search and filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Cari Channel:", placeholder="Masukkan nama channel...")
        
        with col2:
            min_score = st.number_input("SAW Score Minimum:", min_value=0.0, max_value=1.0, value=0.0, step=0.001)
        
        with col3:
            min_subs = st.number_input("Minimum Subscribers:", min_value=0, value=0, step=1000)
        
        # Apply filters
        filtered_df = df.copy()
        
        if search_term:
            filtered_df = filtered_df[filtered_df['Channel_Name'].str.contains(search_term, case=False, na=False)]
        
        if min_score > 0:
            filtered_df = filtered_df[filtered_df['SAW_Score'] >= min_score]
        
        if min_subs > 0:
            filtered_df = filtered_df[filtered_df['Subscriber_Count'] >= min_subs]
        
        st.write(f"Menampilkan {len(filtered_df)} dari {len(df)} channels")
        
        # Display filtered data
        display_df = filtered_df.copy()
        display_df = display_df.round(4)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="youtuber_saw_analysis.csv",
            mime="text/csv"
        )

def main():
    """Main application function"""
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    
    # Page routing
    if st.session_state.page == "landing":
        landing_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
