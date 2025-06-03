import streamlit as st
import requests

# GitHub 레포지토리 정보
GITHUB_USER = st.secrets['user']  # GitHub 사용자 이름
REPO_NAME = st.secrets['name']      # 레포지토리 이름
FOLDER_PATH = st.secrets['path']        # 폴더 경로 (예: 'src' 또는 'docs')

# GitHub API URL
url = f'https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FOLDER_PATH}'

# API 요청
response = requests.get(url)

# Streamlit 앱
st.title(f"과제 제출 확인")

if response.status_code == 200:
    files = response.json()
    if isinstance(files, list):
        for file in files:
            st.write(file['name'], end = "   ")
    else:
        st.write("폴더가 비어 있습니다.")
else:
    st.write("폴더를 가져오는 데 실패했습니다.")
