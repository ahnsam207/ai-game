from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="안이옥 선생님 소개",
    page_icon="👩‍🏫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

IMAGE_DIR = Path(__file__).resolve().parent.parent / "img"
ICON_PATH = IMAGE_DIR / "icon.PNG"
INTRO_PATH = IMAGE_DIR / "intro.jpg"

st.markdown(
    """
    <style>
    .block-container { max-width: 1120px; padding: 2rem 2rem 3rem; }
    h1, h2, h3 { letter-spacing: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

if ICON_PATH.exists():
    title_col, name_col = st.columns([0.14, 0.86], vertical_alignment="center")
    with title_col:
        st.image(str(ICON_PATH), width=76)
    with name_col:
        st.title("안이옥 선생님")
else:
    st.title("👩‍🏫 안이옥 선생님")

st.caption("정보 · 컴퓨터 교과 | 경복비즈니스고등학교")
st.caption("2026학년도 3학기 AI융합교육동향과이슈 과제")
st.divider()

hero_col, intro_col = st.columns([1.1, 1], gap="large", vertical_alignment="center")
with hero_col:
    if INTRO_PATH.exists():
        st.image(str(INTRO_PATH), width="stretch")
    else:
        st.info("소개 사진을 준비하고 있습니다.")

with intro_col:
    st.subheader("배움은 즐거운 도전입니다")
    st.write(
        "새로운 기술을 함께 배우고, 아이디어를 직접 만들어 보는 수업을 합니다. "
        "궁금한 점은 언제든 편하게 질문해 주세요."
    )

st.divider()
info_col, subject_col = st.columns(2, gap="large")
with info_col:
    st.subheader("기본 정보")
    st.markdown(
        """
        - **학교** 경복비즈니스고등학교
        - **수업 시간** 월-금 08:20 ~ 16:20
        - **이메일** 2ok25@daum.net
        """
    )

with subject_col:
    st.subheader("담당 교과")
    st.write(
        "3D프린터제품제작 · 프로그래밍 · 디지털논리회로 · "
        "스마트문화앱콘텐츠제작 · 비즈니스엑셀"
    )

st.divider()
st.subheader("교육과 활동")
education_tab, projects_tab, career_tab = st.tabs(["교육활동", "만든 작품", "발자취"])

with education_tab:
    st.markdown(
        """
        - **영마이스터 해외연수** · 호주, 2025년
        - **미래인재반 활동** · 2024–2025년
        - **동아리 알고리즘 특별활동** · 2023년
        - **강서 미래인재 한마당** · 2023년
        """
    )

with projects_tab:
    st.markdown(
        """
        - 무선 조종 1인승 전기차와 RC Car
        - 스마트팜 만들기
        - 선 없는 실습실 만들기
        """
    )

with career_tab:
    st.markdown(
        """
        - 숙명여자대학교 대학원 AI융합전공 2026년 3학기 재학중
        - 정보과학분야 우수교사 공모전 교육부 장관상 · 2025년
        - 강서양천교육지원청 AI 로봇 피지컬 강사 · 2024년
        - 서울시교육감 우수교사 표창 · 2022년
        """
    )

st.divider()
st.caption("© 2026 안이옥 선생님")