import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='dark')


def show_order_customers_city_df(df):
    order_customers_city_df = df['customer_city'].value_counts().head(10).reset_index()
    order_customers_city_df.columns = ['customer_city', 'order_count']

    fig1, ax1 = plt.subplots(figsize=(10,6))
    
    sns.barplot(data=order_customers_city_df, y='customer_city', x='order_count', hue='customer_city', palette='Blues_d', ax=ax1)
    
    ax1.set_title('Distribusi Pelanggan Berdasarkan Kota', fontsize=16)
    ax1.set_ylabel('Nama Kota', fontsize=12)
    ax1.set_xlabel('Jumlah Pelanggan', fontsize=12)

    st.pyplot(fig1)

def show_top_products(df):

    top_products_df = df['product_category_name'].value_counts().head(10).reset_index()
    top_products_df.columns = ['product_category_name', 'order_count']

    fig2, ax2 = plt.subplots(figsize=(10,6))
    
    sns.barplot(data=top_products_df, y='product_category_name', x='order_count', hue='product_category_name', palette='Blues_d', ax=ax2)
    
    ax2.set_title('Top 10 Produk Paling Populer Berdasarkan Jumlah Pembelian', fontsize=16)
    ax2.set_xlabel('Jumlah Pembelian', fontsize=12)
    ax2.set_ylabel('Nama Produk', fontsize=12)
    
    st.pyplot(fig2)

def show_order_distribution_by_day(df):

    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_day'] = df['order_purchase_timestamp'].dt.day_name()

    order_day_df = df['order_day'].value_counts().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]).reset_index()
    
    order_day_df.columns = ['order_day', 'order_count']

    fig3, ax3 = plt.subplots(figsize=(10,6))
    
    sns.barplot(data=order_day_df, x='order_day', y='order_count', hue='order_count',  palette='Blues_d', ax=ax3)
    
    ax3.set_title('Distribusi Pesanan Berdasarkan Hari dalam Seminggu', fontsize=16)
    ax3.set_xlabel('Hari dalam Seminggu', fontsize=12)
    ax3.set_ylabel('Jumlah Pesanan', fontsize=12)
    
    st.pyplot(fig3)

def show_rfm_distribution(df):

    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    recent_date = df['order_purchase_timestamp'].max()

    rfm_df = df.groupby('customer_id').agg({
        'order_purchase_timestamp': 'max',  # Mengambil tanggal pesanan terakhir
        'order_id': 'nunique',  # Frequency: menghitung jumlah pesanan unik
        'price': 'sum'  # Monetary: menjumlahkan total pembelanjaan
    }).reset_index()

    rfm_df['recency'] = (recent_date - rfm_df['order_purchase_timestamp']).dt.days

    rfm_df.rename(columns={'order_id': 'frequency', 'price': 'monetary'}, inplace=True)

    rfm_df['R_Score'] = pd.cut(rfm_df['recency'], 4, labels=[4, 3, 2, 1], duplicates='drop').astype(int)
    rfm_df['F_Score'] = pd.cut(rfm_df['frequency'], 4, labels=[1, 2, 3, 4], duplicates='drop').astype(int)
    rfm_df['M_Score'] = pd.cut(rfm_df['monetary'], 4, labels=[1, 2, 3, 4], duplicates='drop').astype(int)

    rfm_df['RFM_Score'] = rfm_df['R_Score'] + rfm_df['F_Score'] + rfm_df['M_Score']

    fig4, ax4 = plt.subplots(figsize=(10,6))
    
    sns.histplot(rfm_df['RFM_Score'], bins=10, kde=False, color='skyblue', ax=ax4)
    
    ax4.set_title('Skor RFM Distribusi', fontsize=16)
    ax4.set_xlabel('Skor RFM', fontsize=12)
    ax4.set_ylabel('Frekuensi', fontsize=12)
    plt.tight_layout()


    st.pyplot(fig4)



def main():

    st.header('Rizqi Adiputra - E-Commerce Dashboard :sparkles:')

    df = pd.read_csv('all_data_new.csv', low_memory=False)

    st.subheader('Pelanggan terbanyak berdasarkan kota')    
    show_order_customers_city_df(df)

    st.subheader('Produk terlaris')
    show_top_products(df)

    st.subheader('Hari paling ramai')    
    show_order_distribution_by_day(df)

    st.subheader('Skor RMF Distribusi')    
    show_rfm_distribution(df)

if __name__ == "__main__":
    main()

