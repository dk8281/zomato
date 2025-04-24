
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
df['Datekey_Opening'] = pd.to_datetime(df['Datekey_Opening'])
df['Year'] = df['Datekey_Opening'].dt.year
df['Quarter'] = df['Datekey_Opening'].dt.quarter
df['Month'] = df['Datekey_Opening'].dt.month
openings_by_time = df.groupby(['Year', 'Quarter', 'Month'])['RestaurantID'].nunique().reset_index(name='RestaurantCount')
st.dataframe(openings_by_time.sort_values(by="RestaurantCount", ascending=False))

# ----- Rating Distribution
st.subheader("🌟 Rating Distribution")
rating_bins = [0, 1.99, 2.99, 3.99, 4.99, 5]
rating_labels = ['0-1.99', '2-2.99', '3-3.99', '4-4.99', '5']
df['RatingBucket'] = pd.cut(df['Rating'], bins=rating_bins, labels=rating_labels, include_lowest=True)
rating_counts = df['RatingBucket'].value_counts().sort_index().reset_index(name='RestaurantCount')
rating_counts.columns = ['RatingBucket', 'RestaurantCount']
st.dataframe(rating_counts.sort_values(by="RestaurantCount", ascending=False))

fig2, ax2 = plt.subplots()
ax2.pie(rating_counts['RestaurantCount'], labels=rating_counts['RatingBucket'], autopct='%1.1f%%')
ax2.set_title("Distribution of Ratings")
st.pyplot(fig2)

# ----- Price Distribution
st.subheader("💲 Price Distribution")
price_bins = [0, 200, 400, 600, 800, 10000]
price_labels = ['0-200', '201-400', '401-600', '601-800', '800+']
df['PriceBucket'] = pd.cut(df['Average_Cost_for_two'], bins=price_bins, labels=price_labels, include_lowest=True)
price_counts = df['PriceBucket'].value_counts().sort_index().reset_index(name='RestaurantCount')
price_counts.columns = ['PriceBucket', 'RestaurantCount']
st.dataframe(price_counts.sort_values(by="RestaurantCount", ascending=False))

fig2, ax2 = plt.subplots()
ax2.pie(price_counts['RestaurantCount'], labels=price_counts['PriceBucket'], autopct='%1.1f%%')
ax2.set_title("Distribution of Price")
st.pyplot(fig2)

# ----- Percentage of Restaurants with Table Booking
st.subheader("🗃️ Percentage of Restaurants with Table Booking")
table_booking_percent = df['Has_Table_booking'].value_counts(normalize=True) * 100
st.write(table_booking_percent.astype(str) + '%')
st.dataframe(table_booking_percent.sort_values(by="table_booking_percent", ascending=False))

# ----- Percentage of Restaurants with Online Delivery
st.subheader("📲 Percentage of Restaurants with Online Delivery")
online_delivery_percent = df['Has_Online_delivery'].value_counts(normalize=True) * 100
st.write(online_delivery_percent.astype(str) + '%')
st.dataframe(online_delivery_percent.sort_values(by="Has_Online_delivery", ascending=False))
