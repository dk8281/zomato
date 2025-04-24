
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Zomato Analytics", layout="wide")

st.title("📊 Zomato Analytics Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Zomato_Project.csv", encoding="ISO-8859-1")

df = load_data()

# ----- Overview
st.header("🔍 Dataset Overview")
st.write(df.head())

# ----- Number of Restaurants by City and Country
st.subheader("📌 Number of Restaurants by City and Country")
city_country_counts = df.groupby(['City', 'CountryCode'])['RestaurantID'].nunique().reset_index(name='RestaurantCount')
st.dataframe(city_country_counts.sort_values(by="RestaurantCount", ascending=False))

# ----- Restaurant Openings Over Time
st.subheader("📆 Restaurants Opened Over Time")
df['Datekey_Opening'] = pd.to_datetime(df['Datekey_Opening'], errors='coerce')
df['Year'] = df['Datekey_Opening'].dt.year
openings_by_year = df.groupby('Year')['RestaurantID'].nunique().reset_index(name='RestaurantCount')

fig, ax = plt.subplots()
ax.plot(openings_by_year['Year'], openings_by_year['RestaurantCount'], marker='o')
ax.set_title("Restaurants Opened per Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Restaurants")
st.pyplot(fig)

# ----- Rating Distribution
st.subheader("🌟 Rating Distribution")
rating_bins = [0, 1.99, 2.99, 3.99, 4.99, 5]
rating_labels = ['0-1.99', '2-2.99', '3-3.99', '4-4.99', '5']
df['RatingBucket'] = pd.cut(df['Rating'], bins=rating_bins, labels=rating_labels, include_lowest=True)

rating_counts = df['RatingBucket'].value_counts().sort_index().reset_index(name='RestaurantCount')
rating_counts.columns = ['RatingBucket', 'RestaurantCount']

fig2, ax2 = plt.subplots()
ax2.pie(rating_counts['RestaurantCount'], labels=rating_counts['RatingBucket'], autopct='%1.1f%%')
ax2.set_title("Distribution of Ratings")
st.pyplot(fig2)
