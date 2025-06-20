import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="데이터 분석 웹앱", layout="wide")
st.title("데이터 분석 웹앱")

# 1. CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    # 2. 기본 정보
    st.subheader("기본 정보")
    st.write(f"행 개수: {df.shape[0]}, 열 개수: {df.shape[1]}")
    st.write("컬럼 타입:")
    st.write(df.dtypes)
    st.write("결측치 개수:")
    st.write(df.isnull().sum())

    # 3. 데이터 전처리
    st.subheader("데이터 전처리")
    if st.checkbox("결측치 제거"):
        df = df.dropna()
        st.success("결측치가 제거되었습니다.")

    # 4. 수치형/범주형 컬럼 분리
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # 5. 시각화
    st.subheader("데이터 시각화")
    if numeric_cols:
        col = st.selectbox("수치형 컬럼 선택", numeric_cols)
        plot_type = st.radio("그래프 종류 선택", ["히스토그램", "박스플롯"])
        fig, ax = plt.subplots()
        if plot_type == "히스토그램":
            sns.histplot(df[col], kde=True, ax=ax)
        else:
            sns.boxplot(x=df[col], ax=ax)
        st.pyplot(fig)
    else:
        st.info("수치형 컬럼이 없습니다.")

    if categorical_cols:
        st.subheader("범주형 컬럼 시각화")
        cat_col = st.selectbox("범주형 컬럼 선택", categorical_cols)
        fig2, ax2 = plt.subplots()
        df[cat_col].value_counts().plot(kind='bar', ax=ax2)
        st.pyplot(fig2)

    # 6. 상관관계 분석
    st.subheader("상관관계 히트맵")
    if len(numeric_cols) >= 2:
        fig3, ax3 = plt.subplots()
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax3)
        st.pyplot(fig3)
    else:
        st.info("상관관계 분석을 위한 수치형 컬럼이 부족합니다.")
else:
    st.info("먼저 CSV 파일을 업로드하세요.")