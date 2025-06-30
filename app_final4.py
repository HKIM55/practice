import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 한글 폰트 설정
matplotlib.rc('font', family='AppleGothic')

# CSV 파일 URL
url = 'https://raw.githubusercontent.com/HKIM55/practice/main/grocery_rawdata.csv'

# CSV 불러오기
try:
    df = pd.read_csv(url)

    # 문자열 컬럼 공백 제거
    for col in ['품목', '세부', '마트']:
        df[col] = df[col].astype(str).str.strip()

    # 날짜 처리: float형 → 정수형 → 문자열 변환
    df['날짜'] = df['날짜'].apply(lambda x: str(int(x)) if pd.notnull(x) else '')

    # 날짜 8자리만 남기기
    df = df[df['날짜'].str.len() == 8]

    # 날짜 컬럼 변환
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d', errors='coerce')
    df = df.dropna(subset=['날짜'])

    # 단가 (원) 처리
    df['단가 (원)'] = df['단가 (원)'].astype(str).str.replace(',', '').str.strip()
    df['단가 (원)'] = pd.to_numeric(df['단가 (원)'], errors='coerce')

    st.title("📊 가계부 품목/세부 가격 추세 확인 앱")



    search_option = st.radio('🔎 검색 기준을 선택하세요', ['품목', '세부'])
    search_keyword = st.text_input(f'{search_option} 입력')

    if search_keyword:
        if search_option == '품목':
            result_df = df[df['품목'].str.contains(search_keyword, case=False, na=False)]
        else:
            result_df = df[df['세부'].str.contains(search_keyword, case=False, na=False)]

        if not result_df.empty:
            display_df = result_df[['날짜', '품목', '세부', '마트', '단가 (원)', '단가 (100 g, ml당 가격)']]\
                .dropna(subset=['단가 (원)']).sort_values('날짜').reset_index(drop=True)

            st.write(f"✅ 검색 결과: {len(display_df)}건")
            st.dataframe(display_df)

            if not display_df.empty:
                min_idx = display_df['단가 (원)'].idxmin()
                max_idx = display_df['단가 (원)'].idxmax()

                min_row = display_df.loc[min_idx]
                max_row = display_df.loc[max_idx]

                plt.figure(figsize=(12, 6))
                plt.plot(display_df['날짜'], display_df['단가 (원)'], marker='o', linestyle='-', color='tab:blue')

                plt.scatter(min_row['날짜'], min_row['단가 (원)'], color='red', label=f"최소: {min_row['단가 (원)']}원 ({min_row['날짜'].date()})")
                plt.scatter(max_row['날짜'], max_row['단가 (원)'], color='green', label=f"최대: {max_row['단가 (원)']}원 ({max_row['날짜'].date()})")

                plt.title(f'📈 {search_keyword} 단가 추세')
                plt.xlabel('날짜')
                plt.ylabel('단가 (원)')
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.warning("📉 유효한 단가 데이터가 없습니다.")
        else:
            st.warning("검색 결과가 없습니다.")

except Exception as e:
    st.error(f"CSV를 불러오는 중 문제가 발생했습니다: {e}")
