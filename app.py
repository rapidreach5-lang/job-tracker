import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Job Market Intelligence", page_icon="📊", layout="wide"
)

st.title("📊 Remote Tech Job Market Intelligence Dashboard")
st.markdown(
    "Tracking real-time remote positions and top-paying career opportunities."
)


# Load top-paying jobs leaderboard from SQLite (Filtered to ignore unrealistic outliers > $2M)
@st.cache_data
def load_leaderboard():
  conn = sqlite3.connect("jobs.db")
  df = pd.read_sql(
      "SELECT title, salary_min, source FROM jobs WHERE salary_min > 0 AND"
      " salary_min < 2000000 ORDER BY salary_min DESC LIMIT 3",
      conn,
  )
  conn.close()
  return df


# --- LEADERBOARD SECTION ---
st.subheader("🏆 Top-Paying Jobs Leaderboard")
leaderboard_df = load_leaderboard()

if not leaderboard_df.empty:
  cols = st.columns(len(leaderboard_df))
  for i, (index, row) in enumerate(leaderboard_df.iterrows()):
    with cols[i]:
      st.metric(
          label=row["title"],
          value=f"${row['salary_min']:,}/yr",
          delta="Top Earner",
      )
else:
  st.info("Run your scraper to populate salary listings for the leaderboard!")

st.divider()

# --- FULL DATA TABLE ---


@st.cache_data
def load_all_data():
  conn = sqlite3.connect("jobs.db")
  df = pd.read_sql("SELECT * FROM jobs", conn)
  conn.close()
  return df


df = load_all_data()
st.subheader("📋 All Scraped Job Listings")
if not df.empty:
  st.dataframe(df, use_container_width=True)
else:
  st.info("No data found in database yet.")