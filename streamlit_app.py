import random

import streamlit as st

st.title("🧠 중학생 영단어 & BTS 앱")
st.write("탭을 선택해서 영단어 게임과 BTS 소개 페이지를 확인해보세요.")

WORDS = [
    {"word": "apple", "meaning": "사과"},
    {"word": "school", "meaning": "학교"},
    {"word": "friend", "meaning": "친구"},
    {"word": "happy", "meaning": "행복한"},
    {"word": "teacher", "meaning": "선생님"},
    {"word": "book", "meaning": "책"},
    {"word": "family", "meaning": "가족"},
    {"word": "summer", "meaning": "여름"},
    {"word": "music", "meaning": "음악"},
    {"word": "schoolbag", "meaning": "책가방"},
]

TAB_NAMES = ["영단어", "BTS 소개"]
selected_tab = st.tabs(TAB_NAMES)

if "question_index" not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.used_questions = random.sample(WORDS, k=5)
    st.session_state.answer_checked = False
    st.session_state.last_correct = None


def reset_game():
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.used_questions = random.sample(WORDS, k=5)
    st.session_state.answer_checked = False
    st.session_state.last_correct = None

with selected_tab[0]:
    st.header("영단어 퀴즈")
    if st.session_state.question_index >= len(st.session_state.used_questions):
        st.write("---")
        st.header("게임 종료")
        st.write(f"총 점수: {st.session_state.score} / {len(st.session_state.used_questions)}")
        if st.button("다시 시작하기"):
            reset_game()
            st.experimental_rerun()
    else:
        current = st.session_state.used_questions[st.session_state.question_index]
        correct_word = current["word"]
        meaning = current["meaning"]

        all_words = [w["word"] for w in WORDS if w["word"] != correct_word]
        choices = random.sample(all_words, k=3) + [correct_word]
        random.shuffle(choices)

        st.markdown(f"### 문제 {st.session_state.question_index + 1} / {len(st.session_state.used_questions)}")
        st.markdown(f"**{meaning}**에 해당하는 영어 단어를 선택하세요.")
        selected = st.radio("보기", choices, index=0, key=f"choice_{st.session_state.question_index}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("정답 확인", key=f"check_{st.session_state.question_index}"):
                st.session_state.answer_checked = True
                st.session_state.last_correct = selected == correct_word
                if st.session_state.last_correct:
                    st.session_state.score += 1
        with col2:
            if st.button("다음 문제", key=f"next_{st.session_state.question_index}"):
                st.session_state.question_index += 1
                st.session_state.answer_checked = False

        if st.session_state.answer_checked:
            if st.session_state.last_correct:
                st.success("정답입니다! 잘했어요 😊")
            else:
                st.error(f"틀렸어요. 정답은 '{correct_word}'입니다.")

with selected_tab[1]:
    st.header("BTS 소개")
    st.write("BTS는 대한민국의 힙합 보이 그룹으로, 7명의 멤버로 구성되어 있습니다.")
    st.write("아래는 BTS의 주요 정보입니다.")
    st.markdown("- 데뷔: 2013년 6월 13일")
    st.markdown("- 소속사: 빅히트 뮤직 (HYBE)")
    st.markdown("- 대표곡: Dynamite, Butter, Permission to Dance, 봄날")
    st.markdown("- 팬클럽 이름: ARMY")
    st.markdown("- 특징: 퍼포먼스, 자작곡, 긍정 메시지")

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/BTS_in_Singapore_20180901.jpg/1200px-BTS_in_Singapore_20180901.jpg",
        caption="BTS의 대표 무대 사진",
        use_column_width=True,
    )

    st.subheader("더 멋진 사진")
    col1, col2 = st.columns(2)
    with col1:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/BTS_at_The_2018_Melon_Music_Awards_%285%29.jpg/1280px-BTS_at_The_2018_Melon_Music_Awards_%285%29.jpg",
            caption="무대 위 BTS",
            use_column_width=True,
        )
    with col2:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/BTS_%28Bangtan_Boys%29_%EC%A0%84%EC%B2%B4_2019.png/1200px-BTS_%28Bangtan_Boys%29_%EC%A0%84%EC%B2%B4_2019.png",
            caption="BTS 공식 그룹 사진",
            use_column_width=True,
        )

    st.subheader("멤버 소개")
    st.markdown("**RM** - 리더, 래퍼")
    st.markdown("**진** - 보컬")
    st.markdown("**슈가** - 래퍼")
    st.markdown("**제이홉** - 래퍼, 댄서")
    st.markdown("**지민** - 보컬, 댄서")
    st.markdown("**뷔** - 보컬")
    st.markdown("**정국** - 메인보컬")

    st.write("BTS는 음악과 춤, 긍정적인 메시지로 많은 사랑을 받고 있습니다.")
