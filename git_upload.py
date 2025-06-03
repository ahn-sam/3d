import streamlit as st
import requests
import base64

GITHUB_REPO = st.secrets["repo"]
GITHUB_TOKEN = st.secrets["git_token"]
BRANCH = "main"

st.title("과제 제출")
uploaded_file = st.file_uploader("파일을 업로드하세요")

if uploaded_file is not None:
    file_content = uploaded_file.getvalue()
    file_path = f"upload/{uploaded_file.name}"
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"

    encoded_content = base64.b64encode(file_content).decode("utf-8")

    # 기존 파일 SHA 확인 (있으면 업데이트)
    get_response = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if get_response.status_code == 200:
        sha = get_response.json()["sha"]
    else:
        sha = None

    data = {
        "message": f"Upload {uploaded_file.name}",
        "content": encoded_content,
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    
    st.write(response.status_code)
    st.write(response.text)

    if response.status_code in [200, 201]:
        st.success(f"✅ 파일이 정상적으로 업로드되었습니다.\n\n {uploaded_file.name}")
    else:
        st.error("❌ 업로드 실패(파일의 이름을 수정하거나, 디렉토리 확인 필요)")
