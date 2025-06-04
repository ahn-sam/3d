import streamlit as st
import requests
import base64

GITHUB_REPO = st.secrets["repo"]  # "username/repo" 형태
GITHUB_TOKEN = st.secrets["git_token"]
BRANCH = "main"  # "master"일 수도 있으니 꼭 확인!

st.title("과제 제출")

uploaded_file = st.file_uploader("파일을 업로드하세요")

if uploaded_file is not None:
    file_content = uploaded_file.getvalue()
    file_path = f"upload/{uploaded_file.name}"
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"

    encoded_content = base64.b64encode(file_content).decode("utf-8")

    # 기존 파일 존재 여부 확인 (sha)
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

    if response.status_code in [200, 201]:
        st.success(f"✅ 파일이 정상적으로 업로드되었습니다.\n\n {uploaded_file.name}")
    else:
        st.error("❌ 업로드 실패 (파일 이름을 확인하세요.)")
