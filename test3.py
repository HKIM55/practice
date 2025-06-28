import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV 파일 경로 (사용자 지정)
file_path = '/Users/hyunjin/Library/Mobile Documents/com~apple~CloudDocs/MacBook/Jin/Data.csv'

# 파일이 존재하는지 확인
if not os.path.exists(file_path):
    st.error(f"파일이 존재하지 않습니다: {file_path}")
else:
    # CSV 파일 불러오기
    df = pd.read_csv(file_path)

    st.title("📊 가계부 품목/세부 가격 추세 확인 앱")

    # 사용자 검색 옵션 선택
    search_option = st.radio('🔎 검색 기준을 선택하세요', ['품목', '세부'])
    search_keyword = st.text_input(f'{search_option} 입력')

    if search_keyword:
        if search_option == '품목':
            result_df = df[df['품목'].str.contains(search_keyword, case=False, na=False)]
        else:
            result_df = df[df['세부'].str.contains(search_keyword, case=False, na=False)]

        if not result_df.empty:
            st.write(f"✅ 검색 결과: {len(result_df)}건")
            st.dataframe(result_df)

            # 날짜별 가격 추세 시각화
            result_df['날짜'] = pd.to_datetime(result_df['날짜'], errors='coerce')
            result_df = result_df.sort_values('날짜')

            plt.figure(figsize=(10, 5))
            plt.plot(result_df['날짜'], result_df['단가 (100 g, ml당)'], marker='o')
            plt.title(f'📈 {search_keyword} 가격 추세')
            plt.xlabel('날짜')
            plt.ylabel('단가 (100 g, ml당)')
            plt.xticks(rotation=45)
            plt.grid(True)
            st.pyplot(plt)

        else:
            st.warning("검색 결과가 없습니다.")