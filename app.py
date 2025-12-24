import streamlit as st
import pandas as pd
import plotly.express as px
from bs4 import BeautifulSoup
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="YouTube Wrapped", layout="wide", page_icon="📺")

# --- DATA LOADER ---
@st.cache_data
def load_data_structure(file_path):
    data = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "lxml")
            
        # Find every link that looks like a video
        video_links = soup.find_all("a", href=lambda href: href and "youtube.com/watch" in href)
        
        for link in video_links:
            try:
                # 1. TITLE
                title = link.get_text()
                
                # 2. CHANNEL (The next link sibling)
                channel_link = link.find_next_sibling("a")
                if channel_link:
                    channel = channel_link.get_text()
                else:
                    channel = "Unknown"
                    
                # 3. DATE (Text node after channel)
                date_node = channel_link.next_sibling
                if date_node and date_node.name == 'br':
                    date_node = date_node.next_sibling
                
                if date_node:
                    date_str = str(date_node).strip()
                    if "GMT" in date_str:
                        date_str = date_str.split("GMT")[0].strip()
                    
                    # Parse Date
                    try:
                        dt = datetime.strptime(date_str, "%d %b %Y, %H:%M:%S")
                        data.append({"Title": title, "Channel": channel, "Date": dt})
                    except ValueError:
                        continue
            except Exception:
                continue
                
    except FileNotFoundError:
        return pd.DataFrame()
        
    return pd.DataFrame(data)

# --- MAIN APP ---
st.title("📺 YouTube Wrapped Dashboard")

# 1. Load Data
df = load_data_structure("watch-history.html")

if not df.empty:
    # Prepare Date Columns
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour

    # --- SIDEBAR: YEAR FILTER ---
    st.sidebar.title("⚙️ Filters")
    
    # Get all unique years from the data
    available_years = sorted(df['Year'].unique(), reverse=True)
    
    # Create the dropdown list
    year_options = ["All Time"] + list(available_years)
    selected_year = st.sidebar.selectbox("📅 Choose a Year:", year_options)
    
    # --- FILTER 1: YEAR ---
    if selected_year == "All Time":
        df_year_filtered = df
        st.header("Your All-Time Stats")
    else:
        df_year_filtered = df[df['Year'] == selected_year]
        st.header(f"Your Stats for {selected_year}")

    if not df_year_filtered.empty:
        
        # --- TOGGLE: TOTAL VS UNIQUE ---
        st.write("---")
        view_mode = st.radio(
            "📊 Ranking Logic:", 
            ["Total Views (Includes Re-watches)", "Unique Videos (Ignores Re-watches)"], 
            horizontal=True
        )
        
        # --- FILTER 2: UNIQUENESS ---
        if "Unique" in view_mode:
            # Keep only the first time you watched a specific video title from a specific channel
            df_display = df_year_filtered.drop_duplicates(subset=['Title', 'Channel'])
            metric_label = "Unique Videos"
        else:
            df_display = df_year_filtered
            metric_label = "Total Views"

        # --- METRICS ---
        st.write("") # Spacer
        col1, col2, col3 = st.columns(3)
        
        col1.metric(metric_label, len(df_display))
        
        # Most Watched Channel
        top_channel = df_display['Channel'].mode()
        if not top_channel.empty:
            col2.metric("Top Channel", top_channel[0])
        else:
            col2.metric("Top Channel", "-")
            
        # Estimated Hours (Only meaningful for Total Views really, but calculated for both)
        est_hours = int((len(df_display) * 10) / 60)
        col3.metric("Est. Hours (10m avg)", f"{est_hours} hrs")
        
        # --- CHARTS ---
        
        # 1. Top Channels Bar Chart
        st.subheader(f"🏆 Top Channels ({metric_label})")
        top_channels = df_display['Channel'].value_counts().head(10)
        st.bar_chart(top_channels)
        
        # 2. Activity Heatmap
        st.subheader("🔥 Viewing Heatmap")
        heatmap_data = df_display.groupby(['DayOfWeek', 'Hour']).size().reset_index(name='Count')
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        fig = px.density_heatmap(
            heatmap_data, 
            x='Hour', 
            y='DayOfWeek', 
            z='Count',
            category_orders={"DayOfWeek": days_order},
            color_continuous_scale="Viridis",
            title=f"When you watched YouTube in {selected_year}"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 3. Monthly Activity
        st.subheader("📅 Activity by Month")
        month_order = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        
        monthly_counts = df_display['Month'].value_counts().reindex(month_order, fill_value=0)
        st.bar_chart(monthly_counts)

    else:
        st.warning(f"No videos found for {selected_year}.")

else:
    st.error("Could not load data. Please ensure 'watch-history.html' is in the folder.")