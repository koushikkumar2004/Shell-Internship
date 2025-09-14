import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.linear_model import LinearRegression

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    file_path = r"C:\Users\Koushik Kumar\OneDrive\Desktop\Shell\sdg_index_2000-2022.csv"
    if not os.path.exists(file_path):
        st.error(f"CSV file not found!\nExpected at: {file_path}")
        st.stop()
    return pd.read_csv(file_path)

df = load_data()
goal_columns = [col for col in df.columns if "goal_" in col]

st.set_page_config(page_title="SDG Index Dashboard", layout="wide")

# ==============================
# Sidebar Navigation with Icons
# ==============================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page):
    st.session_state.page = page
    st.rerun()

st.sidebar.markdown("<h2 style='margin-bottom:10px;'> 🌍 SDG Explorer </h2>", unsafe_allow_html=True)

home_selected = st.sidebar.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.page == "home" else "secondary")
feature_selected = st.sidebar.button("📑 Feature Description", use_container_width=True, type="primary" if st.session_state.page == "feature" else "secondary")
future_selected = st.sidebar.button("🔮 Future Predictions", use_container_width=True, type="primary" if st.session_state.page == "future" else "secondary")

if home_selected:
    go_to("home")
if feature_selected:
    go_to("feature")
if future_selected:
    go_to("future")

# ==============================
# Global Filters (Available for all pages)
# ==============================
countries = st.sidebar.multiselect(
    "🌎 Select Country",
    options=sorted(df['country'].unique()),
    default=["India"]
)

# Dropdown for year range instead of slider
years = st.sidebar.selectbox(
    "📅 Select Year Range",
    options=[
        (2000, 2005),
        (2006, 2010),
        (2011, 2015),
        (2016, 2020),
        (2021, 2022)
    ],
    index=4  # Default: last option (2021–2022)
)

filtered_df = df[(df['country'].isin(countries)) & (df['year'].between(years[0], years[1]))]



# ==============================
# Home Page
# ==============================
if st.session_state.page == "home":
    st.markdown(
        "<h1 style='display:flex;align-items:center;gap:10px;'>"
        "<img src='https://img.icons8.com/fluency/48/globe-earth.png' width='35'/>"
        "SDG Index Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.markdown("Explore Sustainable Development Goal (SDG) scores from 2000 to 2022.")

    st.info("Want to learn what each goal means?")
    if st.button("🔍 View Goal Descriptions", use_container_width=True):
        go_to("feature")

    # Filtered Table
    st.subheader("📊 Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)

    # Line Chart
    st.subheader("📈 SDG Index Trend Over Time")
    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        for country in filtered_df['country'].unique():
            country_data = filtered_df[filtered_df['country'] == country]
            ax.plot(country_data['year'], country_data['sdg_index_score'], marker='o', label=country)

        ax.set_xlabel("Year")
        ax.set_ylabel("SDG Index Score")
        ax.legend()
        ax.grid()
        st.pyplot(fig)
    else:
        st.warning("No data available for selected filters.")

    # Goal-wise Bar Chart
    st.subheader("🎯 Goal-wise Average Scores (Selected Range)")
    if not filtered_df.empty:
        avg_scores = filtered_df[goal_columns].mean().reset_index()
        avg_scores.columns = ["Goal", "Average Score"]
        avg_scores["Goal"] = avg_scores["Goal"].str.replace("_score", "").str.replace("goal_", "Goal ")

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.bar(avg_scores["Goal"], avg_scores["Average Score"], color="skyblue")
        ax.set_ylabel("Average Score")
        ax.set_xticklabels(avg_scores["Goal"], rotation=45, ha="right")
        ax.grid(axis='y')
        st.pyplot(fig)

    # Correlation Table
    st.subheader("📊 Correlation Between Goals")
    if not filtered_df.empty:
        corr = filtered_df[goal_columns].corr()
        st.dataframe(corr.style.background_gradient(cmap='Blues'), use_container_width=True)

# ==============================
# Feature Description Page
# ==============================
elif st.session_state.page == "feature":
    st.markdown(
        "<h1 style='display:flex;align-items:center;gap:10px;'>"
        "<img src='https://img.icons8.com/fluency/48/tasklist.png' width='35'/>"
        "Feature Description</h1>",
        unsafe_allow_html=True
    )

    st.info("💡 Hover over each goal icon to learn more about it!")

    if st.button("How does this work?"):
        st.success("👉 Move your mouse pointer over each goal icon to see a short description. "
                   "Click the icon to visit the official SDG page in a new tab.")

    cols = st.columns(3)

    feature_data = [
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-01.jpg", "caption": "Goal 1 — No Poverty", "tooltip": "End poverty in all its forms everywhere", "link": "https://sdgs.un.org/goals/goal1"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-02.jpg", "caption": "Goal 2 — Zero Hunger", "tooltip": "End hunger, achieve food security and improved nutrition, and promote sustainable agriculture", "link": "https://sdgs.un.org/goals/goal2"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-03.jpg", "caption": "Goal 3 — Good Health & Well-being", "tooltip": "Ensure healthy lives and promote well-being for all at all ages", "link": "https://sdgs.un.org/goals/goal3"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-04.jpg", "caption": "Goal 4 — Quality Education", "tooltip": "Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all", "link": "https://sdgs.un.org/goals/goal4"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-05.jpg", "caption": "Goal 5 — Gender Equality", "tooltip": "Achieve gender equality and empower all women and girls", "link": "https://sdgs.un.org/goals/goal5"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-06.jpg", "caption": "Goal 6 — Clean Water & Sanitation", "tooltip": "Ensure availability and sustainable management of water and sanitation for all", "link": "https://sdgs.un.org/goals/goal6"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-07.jpg", "caption": "Goal 7 — Affordable & Clean Energy", "tooltip": "Ensure access to affordable, reliable, sustainable and modern energy for all", "link": "https://sdgs.un.org/goals/goal7"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-08.jpg", "caption": "Goal 8 — Decent Work & Economic Growth", "tooltip": "Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all", "link": "https://sdgs.un.org/goals/goal8"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-09.jpg", "caption": "Goal 9 — Industry, Innovation & Infrastructure", "tooltip": "Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation", "link": "https://sdgs.un.org/goals/goal9"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-10.jpg", "caption": "Goal 10 — Reduced Inequalities", "tooltip": "Reduce inequality within and among countries", "link": "https://sdgs.un.org/goals/goal10"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-11.jpg", "caption": "Goal 11 — Sustainable Cities & Communities", "tooltip": "Make cities and human settlements inclusive, safe, resilient and sustainable", "link": "https://sdgs.un.org/goals/goal11"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-12.jpg", "caption": "Goal 12 — Responsible Consumption & Production", "tooltip": "Ensure sustainable consumption and production patterns", "link": "https://sdgs.un.org/goals/goal12"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-13.jpg", "caption": "Goal 13 — Climate Action", "tooltip": "Take urgent action to combat climate change and its impacts", "link": "https://sdgs.un.org/goals/goal13"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-14.jpg", "caption": "Goal 14 — Life Below Water", "tooltip": "Conserve and sustainably use the oceans, seas and marine resources", "link": "https://sdgs.un.org/goals/goal14"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-15.jpg", "caption": "Goal 15 — Life on Land", "tooltip": "Protect, restore and promote sustainable use of terrestrial ecosystems", "link": "https://sdgs.un.org/goals/goal15"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-16.jpg", "caption": "Goal 16 — Peace, Justice & Strong Institutions", "tooltip": "Promote peaceful and inclusive societies, provide access to justice for all, and build effective institutions", "link": "https://sdgs.un.org/goals/goal16"},
        {"img": "https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-17.jpg", "caption": "Goal 17 — Partnerships for the Goals", "tooltip": "Strengthen the means of implementation and revitalize the global partnership for sustainable development", "link": "https://sdgs.un.org/goals/goal17"}
    ]

    for i, item in enumerate(feature_data):
        with cols[i % 3]:
            st.markdown(
                f"""
                <a href="{item['link']}" target="_blank" style="text-decoration:none; color:inherit;">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:15px;cursor:pointer;">
                        <img src="{item['img']}" title="{item['tooltip']}" width="50" style="border-radius:8px;">
                        <span style="font-size:14px;">{item['caption']}</span>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )

    if st.button("⬅ Back to Home", key="back_from_feature", use_container_width=True):
        go_to("home")

# ==============================
# Future Prediction Page
# ==============================
elif st.session_state.page == "future":
    st.markdown(
        "<h1 style='display:flex;align-items:center;gap:10px;'>"
        "<img src='https://img.icons8.com/fluency/48/futurama-bender.png' width='35'/>"
        "Future SDG Index Prediction</h1>",
        unsafe_allow_html=True
    )

    st.info("📊 Select a future year and see predicted SDG Index scores for your selected countries.")

    last_available_year = int(df['year'].max())
    future_year = st.selectbox(
        "📅 Select Year Until Which to Predict",
        options=list(range(last_available_year + 1, 2051)),
        index=2
    )

    if not filtered_df.empty:
        prediction_data = []
        for country in filtered_df['country'].unique():
            country_data = df[df['country'] == country]
            X = country_data['year'].values.reshape(-1, 1)
            y = country_data['sdg_index_score'].values

            model = LinearRegression()
            model.fit(X, y)

            last_year = int(country_data['year'].max())
            future_X = np.arange(last_year + 1, future_year + 1).reshape(-1, 1)
            future_preds = model.predict(future_X)

            prediction_data.append({
                "country": country,
                "last_year": last_year,
                "future_year": future_year,
                "predicted_score": round(float(future_preds[-1]), 2)
            })

        st.subheader(f"📈 Average Predictions for {future_year}")
        cols = st.columns(min(len(prediction_data), 3))
        for i, item in enumerate(prediction_data):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="background-color:#f9f9f9;
                                border:1px solid #ddd;
                                border-radius:12px;
                                padding:15px;
                                margin-bottom:15px;
                                text-align:center;
                                box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
                        <h3 style="margin:0;">🌎 {item['country']}</h3>
                        <p style="margin:4px 0;color:#666;">Prediction from {item['last_year']} → {item['future_year']}</p>
                        <h2 style="color:#2c7be5;">{item['predicted_score']}</h2>
                        <p style="margin:0;font-size:13px;color:#777;">Predicted SDG Index Score</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.success(f"✅ Predictions generated until {future_year}")
    else:
        st.warning("⚠️ Please select at least one country and a valid year range from the sidebar.")






