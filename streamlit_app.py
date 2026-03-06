import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add src to path to import your custom modules
sys.path.append(str(Path(__file__).parent / "src"))

# Page configuration
st.set_page_config(
    page_title="TravelTide - Personalized Loyalty Program",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .insight-text {
        font-size: 1.1rem;
        padding: 1rem;
        background-color: #e3f2fd;
        border-left: 5px solid #1E88E5;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">✈️ TravelTide Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Personalized Loyalty Program Using Customer Segmentation</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1E88E5/FFFFFF?text=TravelTide", use_container_width=True)
    st.markdown("## Navigation")
    
    page = st.radio(
        "Select View",
        ["📊 Dashboard Overview", 
         "👥 Customer Segments", 
         "🎯 Perk Recommendations",
         "📈 Data Explorer",
         "🔮 Predictive Insights"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.info(
        "This dashboard analyzes customer behavior to create personalized "
        "loyalty program recommendations for TravelTide."
    )
    
    st.markdown("### Data Filters")
    # Add filters if you have data loaded
    if 'df' in st.session_state:
        date_range = st.date_input("Select Date Range", [])
        min_sessions = st.slider("Minimum Sessions", 0, 50, 5)

# Mock data generation (replace with your actual data loading)
@st.cache_data
def load_sample_data():
    """Load sample data - replace with your actual data loading logic"""
    np.random.seed(42)
    n_customers = 1000
    
    data = {
        'customer_id': range(1000, 1000 + n_customers),
        'total_sessions': np.random.randint(1, 50, n_customers),
        'total_bookings': np.random.randint(0, 20, n_customers),
        'avg_flight_price': np.random.normal(350, 150, n_customers).clip(100, 1000),
        'avg_hotel_nights': np.random.normal(3, 2, n_customers).clip(1, 14),
        'hotel_preference': np.random.choice(['Budget', 'Mid-range', 'Luxury'], n_customers),
        'booking_channel': np.random.choice(['Mobile', 'Desktop', 'Tablet'], n_customers),
        'seasonality': np.random.choice(['Summer', 'Winter', 'Spring/Fall'], n_customers),
        'segment': np.random.choice([
            'Budget Explorers', 
            'Business Travelers', 
            'Luxury Seekers',
            'Family Planners',
            'Weekend Escapers'
        ], n_customers, p=[0.25, 0.2, 0.15, 0.2, 0.2])
    }
    
    # Add derived metrics
    df = pd.DataFrame(data)
    df['conversion_rate'] = (df['total_bookings'] / df['total_sessions'] * 100).round(1)
    df['total_spent'] = (df['total_bookings'] * df['avg_flight_price'] + 
                         df['total_bookings'] * df['avg_hotel_nights'] * 150).round(0)
    df['avg_trip_length'] = df['avg_hotel_nights']
    
    return df

# Load data
with st.spinner("Loading customer data..."):
    df = load_sample_data()
    st.session_state['df'] = df

# Main content based on selected page
if page == "📊 Dashboard Overview":
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Customers", f"{len(df):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg. Conversion Rate", f"{df['conversion_rate'].mean():.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg. Trip Length", f"{df['avg_trip_length'].mean():.1f} nights")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Revenue", f"${df['total_spent'].sum():,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Customer Segments Distribution")
        segment_counts = df['segment'].value_counts()
        fig = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="Customer Segmentation",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Conversion Rate by Segment")
        conv_by_segment = df.groupby('segment')['conversion_rate'].mean().sort_values()
        fig = px.bar(
            x=conv_by_segment.values,
            y=conv_by_segment.index,
            orientation='h',
            title="Average Conversion Rate by Segment",
            labels={'x': 'Conversion Rate (%)', 'y': ''},
            color=conv_by_segment.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent insights
    st.markdown("---")
    st.subheader("📌 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-text">
        <strong>🎯 Top Performing Segment:</strong> Business Travelers show the highest 
        conversion rate at 45%, suggesting they're our most valuable segment for immediate revenue.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-text">
        <strong>📱 Channel Preference:</strong> 65% of bookings come from mobile devices,
        indicating the need for a mobile-first loyalty program experience.
        </div>
        """, unsafe_allow_html=True)

elif page == "👥 Customer Segments":
    st.subheader("Customer Segment Analysis")
    
    # Segment selector
    selected_segment = st.selectbox(
        "Select Customer Segment",
        df['segment'].unique()
    )
    
    # Filter data for selected segment
    segment_df = df[df['segment'] == selected_segment]
    
    # Segment metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Customers", len(segment_df))
    with col2:
        st.metric("Avg. Conversion", f"{segment_df['conversion_rate'].mean():.1f}%")
    with col3:
        st.metric("Avg. Trip Length", f"{segment_df['avg_trip_length'].mean():.1f} nights")
    with col4:
        st.metric("Avg. Spend", f"${segment_df['total_spent'].mean():,.0f}")
    
    # Detailed characteristics
    st.subheader(f"📊 {selected_segment} Characteristics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hotel preference distribution
        hotel_pref = segment_df['hotel_preference'].value_counts()
        fig = px.bar(
            x=hotel_pref.index,
            y=hotel_pref.values,
            title="Hotel Preferences",
            color=hotel_pref.index,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Seasonality preference
        season_pref = segment_df['seasonality'].value_counts()
        fig = px.pie(
            values=season_pref.values,
            names=season_pref.index,
            title="Travel Seasonality"
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "🎯 Perk Recommendations":
    st.subheader("Personalized Perk Recommendations")
    
    # Segment-based perk recommendations
    perks_dict = {
        'Budget Explorers': {
            'primary': ['Discount codes', 'Early bird specials', 'Budget hotel deals'],
            'secondary': ['Free cancellation', 'Price drop alerts'],
            'description': 'Focus on value and savings opportunities'
        },
        'Business Travelers': {
            'primary': ['Priority check-in', 'Airport lounge access', 'Flexible booking'],
            'secondary': ['Free upgrades', 'Fast WiFi', 'Meeting room access'],
            'description': 'Emphasize convenience and time-saving benefits'
        },
        'Luxury Seekers': {
            'primary': ['Room upgrades', 'Spa credits', 'Fine dining vouchers'],
            'secondary': ['Private transfers', 'Concierge service', 'Late checkout'],
            'description': 'Offer premium experiences and exclusivity'
        },
        'Family Planners': {
            'primary': ['Kids stay free', 'Family room upgrades', 'Meal packages'],
            'secondary': ['Attraction tickets', 'Babysitting services', 'Family activities'],
            'description': 'Focus on family-friendly benefits and savings'
        },
        'Weekend Escapers': {
            'primary': ['Weekend specials', 'Spa packages', 'Dining credits'],
            'secondary': ['Late checkout', 'Welcome amenities', 'Local experiences'],
            'description': 'Highlight short-break experiences and relaxation'
        }
    }
    
    selected_segment = st.selectbox(
        "Select Segment to View Perks",
        list(perks_dict.keys())
    )
    
    if selected_segment:
        perks = perks_dict[selected_segment]
        
        st.markdown(f"""
        <div style='background-color: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h4>🎯 Strategy: {perks['description']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 Primary Perks")
            for perk in perks['primary']:
                st.markdown(f"✅ {perk}")
        
        with col2:
            st.markdown("### ✨ Secondary Perks")
            for perk in perks['secondary']:
                st.markdown(f"• {perk}")

elif page == "📈 Data Explorer":
    st.subheader("Explore Customer Data")
    
    # Data filters
    col1, col2 = st.columns(2)
    
    with col1:
        selected_columns = st.multiselect(
            "Select Columns to Display",
            df.columns.tolist(),
            default=['customer_id', 'segment', 'total_sessions', 'total_bookings', 'conversion_rate']
        )
    
    with col2:
        search_id = st.text_input("Search Customer ID", "")
    
    # Filter data
    filtered_df = df[selected_columns] if selected_columns else df
    
    if search_id:
        try:
            customer_id = int(search_id)
            filtered_df = filtered_df[filtered_df['customer_id'] == customer_id]
        except:
            st.warning("Please enter a valid customer ID")
    
    # Display data
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="traveltide_customer_data.csv",
        mime="text/csv"
    )

elif page == "🔮 Predictive Insights":
    st.subheader("Predictive Analytics & Future Trends")
    
    # Simple prediction visualization
    st.markdown("### 📈 Revenue Forecast by Segment")
    
    # Generate mock forecast data
    segments = df['segment'].unique()
    months = pd.date_range(start='2024-01-01', periods=6, freq='M')
    
    forecast_data = []
    for segment in segments:
        base_value = df[df['segment'] == segment]['total_spent'].mean()
        for i, month in enumerate(months):
            growth = 1 + (i * 0.05) + np.random.normal(0, 0.02)
            forecast_data.append({
                'Segment': segment,
                'Month': month.strftime('%B %Y'),
                'Predicted_Revenue': base_value * growth * 100
            })
    
    forecast_df = pd.DataFrame(forecast_data)
    
    fig = px.line(
        forecast_df,
        x='Month',
        y='Predicted_Revenue',
        color='Segment',
        title="6-Month Revenue Forecast by Customer Segment",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 🎯 Next Best Action Recommendations")
    
    recommendations = {
        'Budget Explorers': 'Launch targeted discount campaign for off-peak travel',
        'Business Travelers': 'Introduce corporate loyalty tier with meeting credits',
        'Luxury Seekers': 'Partner with premium hotels for exclusive experiences',
        'Family Planners': 'Create family package bundles with activity partners',
        'Weekend Escapers': 'Develop last-minute weekend getaway alerts'
    }
    
    for segment, action in recommendations.items():
        st.markdown(f"**{segment}:** {action}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2024 TravelTide Analytics | Powered by Streamlit"
    "</div>",
    unsafe_allow_html=True
)
