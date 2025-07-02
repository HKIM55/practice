import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 그래프 한글 깨짐 방지: 영어로 변경
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 경로
file_url = 'https://raw.githubusercontent.com/HKIM55/practice/main/grocery_rawdata.csv'

try:
    df = pd.read_csv(file_url)

    # 날짜 데이터 전처리
    df = df[df['날짜'].astype(str).str.len() == 6]
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%y%m%d', errors='coerce')
    df = df.dropna(subset=['날짜'])
    df['날짜'] = df['날짜'].dt.date  # 시간 제거

    # 단가 데이터 전처리
    df['단가 (원)'] = df['단가 (원)'].astype(str).str.replace(',', '').str.strip()
    df['단가 (원)'] = pd.to_numeric(df['단가 (원)'], errors='coerce')
    df = df.dropna(subset=['단가 (원)'])

    st.title("📊 Grocery Price Tracker")

    search_option = st.radio('🔍 Search by:', ['Item', 'Detail'])
    search_keyword = st.text_input(f'Enter {search_option}')

    if search_keyword:
        if search_option == 'Item':
            result_df = df[df['품목'].str.contains(search_keyword, case=False, na=False)]
        else:
            result_df = df[df['세부'].str.contains(search_keyword, case=False, na=False)]

        if not result_df.empty:
            display_df = result_df[['날짜', '품목', '세부', '마트', '단가 (원)', '단가 (100 g, ml당 가격)']].sort_values('날짜').reset_index(drop=True)

            st.write(f"✅ Search Results: {len(display_df)} items found")
            st.dataframe(display_df)

            min_idx = display_df['단가 (원)'].idxmin()
            max_idx = display_df['단가 (원)'].idxmax()
            mode_price = int(display_df['단가 (원)'].mode().iloc[0])

            min_row = display_df.loc[min_idx]
            max_row = display_df.loc[max_idx]

            st.subheader("📋 Price Summary")
            st.table({
                'Label': ['Minimum', 'Maximum', 'Mode (Most Frequent Price)'],
                'Price (KRW)': [f"{int(min_row['단가 (원)']):,}", f"{int(max_row['단가 (원)']):,}", f"{mode_price:,}"]
            })

            plt.figure(figsize=(12, 6))
            plt.plot(display_df['날짜'], display_df['단가 (원)'], marker='o', linestyle='-', color='tab:blue')

            plt.scatter(min_row['날짜'], min_row['단가 (원)'], color='red',
                        label=f"Min: {int(min_row['단가 (원)'])} KRW ({min_row['날짜']})")
            plt.scatter(max_row['날짜'], max_row['단가 (원)'], color='green',
                        label=f"Max: {int(max_row['단가 (원)'])} KRW ({max_row['날짜']})")
            plt.axhline(mode_price, color='orange', linestyle='--', label=f"Mode: {mode_price} KRW")

            plt.title(f'Price Trend for {search_keyword}')
            plt.xlabel('Date')
            plt.ylabel('Price (KRW)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            st.pyplot(plt)

        else:
            st.warning("No matching items found.")
except Exception as e:
    st.error(f"Failed to load CSV file. Error: {e}")
