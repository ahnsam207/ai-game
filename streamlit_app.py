import random

import streamlit as st

st.title("🧠 중학생 영단어 게임")
st.write("아래 문제를 풀어보세요. 알맞은 영어 단어를 골라 점수를 높여봅시다!")

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

if "question_index" not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.used_questions = random.sample(WORDS, k=5)
    st.session_state.answer_checked = False
    st.session_state.last_correct = None

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
        if st.session_state.question_index < len(st.session_state.used_questions) - 1:
            st.session_state.question_index += 1
            st.session_state.answer_checked = False
            st.experimental_rerun()
        else:
            st.session_state.question_index += 1
            st.experimental_rerun()

if st.session_state.answer_checked:
    if st.session_state.last_correct:
        st.success("정답입니다! 잘했어요 😊")
    else:
        st.error(f"틀렸어요. 정답은 '{correct_word}'입니다.")

if st.session_state.question_index >= len(st.session_state.used_questions):
    st.write("---")
    st.header("게임 종료")
    st.write(f"총 점수: {st.session_state.score} / {len(st.session_state.used_questions)}")
    if st.button("다시 시작하기"):
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.used_questions = random.sample(WORDS, k=5)
        st.session_state.answer_checked = False
        st.experimental_rerun()
