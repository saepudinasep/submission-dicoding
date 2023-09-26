import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca Data csv
main_data = pd.read_csv("dashboard/main_data.csv")

# Title Dashboard
st.title("Dashboard Visualisasi Proyek Data Analysis Data")

# Convert order_purchase_timestamp ke datetime
main_data["order_purchase_timestamp"] = pd.to_datetime(main_data["order_purchase_timestamp"])

st.write("Pilih Rentang Tanggal")
tgl_awal, tgl_akhir = st.columns(2)
# widget untuk memilih tanggal mulai
with tgl_awal:
    start_date = st.date_input("Tanggal Mulai ", pd.to_datetime("2017-01-01"))
# widget untuk memilih tanggal mulai
with tgl_akhir:
    end_date = st.date_input("Tanggal Akhir ", pd.to_datetime("2017-12-01"))

# Ubah tanggal ke format datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_orders_df = main_data[(main_data['order_purchase_timestamp'] >= start_date) & (main_data['order_purchase_timestamp'] <= end_date)]

# Dataframe pesanan bulanan
monthly_orders_df = filtered_orders_df.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_item_id": "nunique",
    "price": "sum"
})
monthly_orders_df.index = monthly_orders_df.index.strftime('%B')  # Mengubah format order date menjadi nama bulan

monthly_orders_df = monthly_orders_df.reset_index()
monthly_orders_df.rename(columns={
    "order_item_id": "order_count",
    "price": "revenue"
}, inplace=True)

# Visualisasi jumlah pesanan per bulan
st.write("### Jumlah Pesanan per Bulan")
fig_bulan, ax_bulan = plt.subplots(figsize=(10, 5))
plt.plot(monthly_orders_df["order_purchase_timestamp"], monthly_orders_df["revenue"], marker='o', linewidth=2, color="#72BCD4")
ax_bulan.set_title('Jumlah Pesanan per Bulan', fontsize=20)
ax_bulan.set_xlabel('Bulan')
ax_bulan.set_ylabel('Jumlah Pesanan')
ax_bulan.tick_params(axis='x', rotation=0)
st.pyplot(fig_bulan)

# Visualisasi total pendapatan per bulan
st.write("### Total Pendapatan per Bulan")
fig_revenue, ax_revenue = plt.subplots(figsize=(15, 10))
plt.plot(
    monthly_orders_df["order_purchase_timestamp"],
    monthly_orders_df["revenue"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
ax_revenue.set_title('Total Pendapatan per Bulan', fontsize=20)
ax_revenue.set_xlabel('Bulan')
ax_revenue.set_ylabel('Total Pendapatan')
ax_revenue.tick_params(axis='x', rotation=0)
st.pyplot(fig_revenue)


#Visualisasi Best and Worst Performing Product by Number of Sales
st.write("### Best and Worst Performing Product by Number of Sales")
# Create a figure with two subplots
sum_order_items_df = main_data.groupby("product_category_name").order_item_id.sum().sort_values(ascending=False).reset_index()
fig_best, ax_best = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors_best = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors_worst = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]


# Plot the best performing product
sns.barplot(x="order_item_id", y="product_category_name", data=sum_order_items_df.head(5), palette=colors_best, ax=ax_best[0])
ax_best[0].set_ylabel(None)
ax_best[0].set_xlabel(None)
ax_best[0].set_title("Best Performing Product", loc="center", fontsize=15)
ax_best[0].tick_params(axis='y', labelsize=12)

# Plot the worst performing product
sns.barplot(x="order_item_id", y="product_category_name", data=sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(5), palette=colors_worst, ax=ax_best[1])
ax_best[1].set_ylabel(None)
ax_best[1].set_xlabel(None)
ax_best[1].invert_xaxis()
ax_best[1].yaxis.set_label_position("right")
ax_best[1].yaxis.tick_right()
ax_best[1].set_title("Worst Performing Product", loc="center", fontsize=15)
ax_best[1].tick_params(axis='y', labelsize=12)

# Display the plots in Streamlit
st.pyplot(fig_best)


#Visualisasi distribusi negara pelanggan
st.write("### Jumlah Customer Berdasarkan Negara")
# Group and aggregate data by customer_state
bystate_df = main_data.groupby(by="customer_state").customer_id.nunique().reset_index()
bystate_df.rename(columns={
    "customer_id": "customer_count"
}, inplace=True)

# Create a figure
fig_state, ax_state = plt.subplots(figsize=(10, 5))

colors_state = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Plot the bar chart
sns.barplot(
    x="customer_count",
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False).head(5),
    palette=colors_state,
    ax=ax_state
)

# Customize the plot
ax_state.set_title("Number of Customers by States", loc="center", fontsize=15)
ax_state.set_ylabel(None)
ax_state.set_xlabel(None)
ax_state.tick_params(axis='y', labelsize=12)

# Display the plot in Streamlit
st.pyplot(fig_state)


#Visualisasi distribusi kota pelanggan
st.write("### Jumlah Customer Berdasarkan Kota")
# Group and aggregate data by customer_city
bystate_df = main_data.groupby(by="customer_city").customer_id.nunique().reset_index()
bystate_df.rename(columns={
    "customer_id": "customer_count"
}, inplace=True)

# Create a figure
fig_city, ax_city = plt.subplots(figsize=(10, 5))

colors_city = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Plot the bar chart
sns.barplot(
    x="customer_count",
    y="customer_city",
    data=bystate_df.sort_values(by="customer_count", ascending=False).head(5),
    palette=colors_city,
    ax=ax_city
)

# Customize the plot
ax_city.set_title("Number of Customers by City", loc="center", fontsize=15)
ax_city.set_ylabel(None)
ax_city.set_xlabel(None)
ax_city.tick_params(axis='y', labelsize=12)

# Display the plot in Streamlit
st.pyplot(fig_city)


# Visualisasi RFM Analysis
st.write("## RFM Analysis")
st.write("### Best City Based on RFM Parameters (customer_state)")
# Convert "order_purchase_timestamp" to datetime
main_data["order_purchase_timestamp"] = pd.to_datetime(main_data["order_purchase_timestamp"])

# Your existing code for generating the rfm_df dataframe goes here
rfm_df = main_data.groupby(by="customer_state", as_index=False).agg({
    "order_purchase_timestamp": "max", # mengambil tanggal order terakhir
    "order_id": "nunique", # menghitung jumlah order
    "price": "sum" # menghitung jumlah revenue yang dihasilkan
})
rfm_df.columns = ["customer_state", "max_order_timestamp", "frequency", "monetary"]
# rfm_df.columns
# menghitung kapan terakhir pelanggan melakukan transaksi (hari)
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
recent_date = main_data["order_purchase_timestamp"].dt.date.max()
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 6))

colors_recency = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4", "#72BCD4"]
colors_frequency = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors_monetary = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(y="recency", x="customer_state", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors_recency, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=14)
ax[0].tick_params(axis ='x', labelsize=12)

sns.barplot(y="frequency", x="customer_state", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors_frequency, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=14)
ax[1].tick_params(axis='x', labelsize=12)

sns.barplot(y="monetary", x="customer_state", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors_monetary, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=14)
ax[2].tick_params(axis='x', labelsize=12)

st.pyplot(fig)
