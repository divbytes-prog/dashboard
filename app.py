import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load Data
df = pd.read_csv("india.csv")

st.set_page_config(page_title="India Dashboard", layout="wide")

# --- Sidebar ---
st.sidebar.title("🇮🇳 India Dashboard Pro")
st.sidebar.markdown("Visualize & Explore Indian District-Level Data")

state_list = ['Overall India'] + sorted(df['State'].unique().tolist())
selected_state = st.sidebar.selectbox("🗺️ Select State", state_list)

if selected_state != 'Overall India':
    df = df[df["State"] == selected_state]

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Map View", "📊 Advanced Charts", "🔍 District Explorer",
    "⚖️ Compare Districts", "📋 Data Table"
])

# --- KPI Cards ---
st.markdown("<h1 style='text-align:center;'>📈 Indian District Insights</h1>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("📍 Districts", df['District'].nunique())
col2.metric("👥 Avg Population", f"{df['Population'].mean():,.0f}")
col3.metric("🌐 Avg Internet HH", f"{df['Households_with_Internet'].mean():,.0f}")
col4.metric("📖 Avg Literacy", f"{df['literacy_rate'].mean():.2f}%")

# --- Tab 1: Map View ---
with tab1:
    st.subheader("Interactive District Map")
    map_style = st.selectbox("🗺️ Choose Map Style", ["carto-positron", "open-street-map", "stamen-terrain", "carto-darkmatter"])
    primary = st.selectbox("Select Size Parameter", ['Population', 'Households_with_Internet'])
    secondary = st.selectbox("Select Color Parameter", ['literacy_rate', 'sex_ratio'])

    fig = px.scatter_mapbox(
        df, lat="Latitude", lon="Longitude", hover_name="District",
        hover_data=["Population", "Households_with_Internet", "sex_ratio", "literacy_rate"],
        size=primary, color=secondary, zoom=4 if selected_state == "Overall India" else 6,
        size_max=30, mapbox_style=map_style, height=650
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2: Advanced Charts ---
with tab2:
    st.subheader("Top 10 Districts")
    colA, colB = st.columns(2)

    with colA:
        top_pop = df.sort_values("Population", ascending=False).head(10)
        st.plotly_chart(px.bar(top_pop, x='Population', y='District', orientation='h', title="Top 10 by Population"), use_container_width=True)

        top_internet = df.sort_values("Households_with_Internet", ascending=False).head(10)
        st.plotly_chart(px.bar(top_internet, x='Households_with_Internet', y='District', orientation='h', title="Top 10 by Internet Access"), use_container_width=True)

    with colB:
        top_literacy = df.sort_values("literacy_rate", ascending=False).head(10)
        st.plotly_chart(px.bar(top_literacy, x='literacy_rate', y='District', orientation='h', title="Top 10 by Literacy Rate"), use_container_width=True)

        avg_lit = df['literacy_rate'].mean()
        above = (df['literacy_rate'] > avg_lit).sum()
        below = (df['literacy_rate'] <= avg_lit).sum()
        pie = px.pie(values=[above, below], names=["Above Avg", "Below Avg"], title="District Literacy vs Average")
        st.plotly_chart(pie, use_container_width=True)

# --- Tab 3: District Explorer ---
with tab3:
    st.subheader("🔍 District Details")
    district_name = st.text_input("Enter District Name")

    if district_name:
        match = df[df['District'].str.lower() == district_name.lower()]
        if not match.empty:
            row = match.iloc[0]
            st.success(f"Details for {row['District']} in {row['State']}:")
            st.markdown(f"""
            - 👥 **Population:** {row['Population']:,}
            - 🌐 **Households with Internet:** {row['Households_with_Internet']:,}
            - 📖 **Literacy Rate:** {row['literacy_rate']}%
            - 🚻 **Sex Ratio:** {row['sex_ratio']}
            - 📍 **Coordinates:** ({row['Latitude']}, {row['Longitude']})
            """)
        else:
            st.warning("No matching district found.")

# --- Tab 4: Compare Districts ---
with tab4:
    st.subheader("⚖️ Compare Two Districts")
    d1, d2 = st.columns(2)
    dist1 = d1.selectbox("Select First District", sorted(df['District'].unique()))
    dist2 = d2.selectbox("Select Second District", sorted(df['District'].unique()), index=1)

    comp_df = df[df['District'].isin([dist1, dist2])].set_index('District')
    metrics = ['Population', 'Households_with_Internet', 'literacy_rate', 'sex_ratio']
    bar = go.Figure(data=[
        go.Bar(name=metric, x=comp_df.index, y=comp_df[metric]) for metric in metrics
    ])
    bar.update_layout(title="District Comparison", barmode='group')
    st.plotly_chart(bar, use_container_width=True)

# --- Tab 5: Data Table ---
with tab5:
    st.subheader("📋 Full Dataset")
    st.dataframe(df.reset_index(drop=True), use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, file_name="district_data.csv", mime="text/csv")
