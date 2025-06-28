{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1572a195",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import os\n",
    "\n",
    "# CSV 파일 경로 (사용자 지정)\n",
    "file_path = '/Users/hyunjin/Library/Mobile Documents/com~apple~CloudDocs/MacBook/Jin/Data.csv'\n",
    "\n",
    "# 파일이 존재하는지 확인\n",
    "if not os.path.exists(file_path):\n",
    "    st.error(f\"파일이 존재하지 않습니다: {file_path}\")\n",
    "else:\n",
    "    # CSV 파일 불러오기\n",
    "    df = pd.read_csv(file_path)\n",
    "\n",
    "    st.title(\"📊 가계부 품목/세부 가격 추세 확인 앱\")\n",
    "\n",
    "    # 사용자 검색 옵션 선택\n",
    "    search_option = st.radio('🔎 검색 기준을 선택하세요', ['품목', '세부'])\n",
    "    search_keyword = st.text_input(f'{search_option} 입력')\n",
    "\n",
    "    if search_keyword:\n",
    "        if search_option == '품목':\n",
    "            result_df = df[df['품목'].str.contains(search_keyword, case=False, na=False)]\n",
    "        else:\n",
    "            result_df = df[df['세부'].str.contains(search_keyword, case=False, na=False)]\n",
    "\n",
    "        if not result_df.empty:\n",
    "            st.write(f\"✅ 검색 결과: {len(result_df)}건\")\n",
    "            st.dataframe(result_df)\n",
    "\n",
    "            # 날짜별 가격 추세 시각화\n",
    "            result_df['날짜'] = pd.to_datetime(result_df['날짜'], errors='coerce')\n",
    "            result_df = result_df.sort_values('날짜')\n",
    "\n",
    "            plt.figure(figsize=(10, 5))\n",
    "            plt.plot(result_df['날짜'], result_df['단가 (100 g, ml당)'], marker='o')\n",
    "            plt.title(f'📈 {search_keyword} 가격 추세')\n",
    "            plt.xlabel('날짜')\n",
    "            plt.ylabel('단가 (100 g, ml당)')\n",
    "            plt.xticks(rotation=45)\n",
    "            plt.grid(True)\n",
    "            st.pyplot(plt)\n",
    "\n",
    "        else:\n",
    "            st.warning(\"검색 결과가 없습니다.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
