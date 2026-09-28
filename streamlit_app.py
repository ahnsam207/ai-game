import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Streamlit UI Field Guide",
    page_icon="▦",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --paper: #F5F6F1;
        --ink: #1D2921;
        --muted: #45534A;
        --green: #1D5A45;
        --coral: #B44732;
        --line: #C5CEC4;
    }

    .stApp { background: var(--paper); color: var(--ink); font-family: "DM Sans", sans-serif; }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: #E5EBE4; border-right: 1px solid var(--line); }
    .block-container { max-width: 1240px; padding: 30px 42px 56px; }
    h1, h2, h3 { color: var(--ink); font-family: "Space Grotesk", "DM Sans", sans-serif; letter-spacing: 0; }
    h1 { font-size: 42px; line-height: 1.12; }
    [data-testid="stMetric"] { background: #fff; border: 1px solid var(--line); border-top: 3px solid var(--green); border-radius: 4px; padding: 14px 16px; }
    [data-testid="stMetricLabel"] p { color: var(--muted); }
    [data-testid="stForm"] { background: #E5EBE4; border: 1px solid var(--line); border-radius: 4px; padding: 20px; }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); }
    .stButton > button, [data-testid="stDownloadButton"] button, [data-testid="stFormSubmitButton"] button { border-radius: 3px; }
    .stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] button[kind="primary"] { background: var(--green); border-color: var(--green); }
    .stApp [data-testid="stWidgetLabel"] p, .stApp [data-testid="stWidgetLabel"] label, .stApp label { color: var(--ink); }
    .stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p { color: var(--muted); }
    .field-kicker { color: var(--green); font: 700 12px "Space Grotesk", sans-serif; letter-spacing: 1px; text-transform: uppercase; }
    .stApp .field-note { color: var(--muted); font-size: 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)

months = [f"{month}월" for month in range(1, 13)]
channels = ["웹", "매장", "파트너"]
orders_by_channel = {
    "웹": [168, 182, 194, 188, 216, 231, 225, 248, 242, 263, 279, 301],
    "매장": [142, 151, 147, 165, 171, 180, 176, 189, 202, 197, 218, 229],
    "파트너": [84, 91, 96, 102, 98, 112, 119, 117, 128, 136, 143, 151],
}
records = [
    {
        "월 순서": month_index,
        "월": month,
        "채널": channel,
        "주문량": orders,
        "매출 지수": orders * (4.1 + channel_index * 0.35),
    }
    for month_index, month in enumerate(months)
    for channel_index, (channel, values) in enumerate(orders_by_channel.items())
    for orders in [values[month_index]]
]
data = pd.DataFrame(records)

with st.sidebar:
    st.markdown('<div class="field-kicker">STREAMLIT / UI FIELD GUIDE</div>', unsafe_allow_html=True)
    st.title("화면 조정")
    st.caption("위젯을 바꾸면 본문 데이터와 차트가 함께 바뀝니다.")
    selected_channels = st.multiselect("판매 채널", channels, default=channels[:2])
    selected_months = st.select_slider(
        "조회 기간",
        options=months,
        value=(months[1], months[10]),
    )
    show_target = st.toggle("목표 기준 표시", value=True)
    st.divider()
    st.caption("사이드바 · 멀티셀렉트 · 슬라이더 · 토글")

st.markdown('<div class="field-kicker">COMPONENT STUDY &nbsp; / &nbsp; 01</div>', unsafe_allow_html=True)
st.title("Streamlit, in practice.")
st.markdown(
    '<p class="field-note">데이터 앱의 기본 요소를 한 화면에서 살펴보고 직접 조작해 보세요.</p>',
    unsafe_allow_html=True,
)
st.divider()

filtered = data[
    data["채널"].isin(selected_channels)
    & data["월 순서"].between(months.index(selected_months[0]), months.index(selected_months[1]))
]
monthly = (
    filtered.groupby(["월 순서", "월"], as_index=False)[["주문량", "매출 지수"]]
    .sum()
    .sort_values("월 순서")
)

order_total = int(filtered["주문량"].sum())
revenue_total = int(filtered["매출 지수"].sum())
first_month_orders = int(monthly["주문량"].iloc[0]) if not monthly.empty else 0
last_month_orders = int(monthly["주문량"].iloc[-1]) if not monthly.empty else 0
orders_change = (
    f"{(last_month_orders / first_month_orders - 1):+.1%}"
    if first_month_orders
    else None
)

metric_columns = st.columns(4)
metric_columns[0].metric("선택 기간 주문량", f"{order_total:,}건", orders_change, help="시작 월 대비 마지막 월 변화율")
metric_columns[1].metric("매출 지수", f"{revenue_total:,.0f}", "누적")
metric_columns[2].metric("활성 채널", f"{len(selected_channels)}개", "필터 반영")
average_orders = round(order_total / len(monthly)) if not monthly.empty else 0
metric_columns[3].metric("월평균 주문량", f"{average_orders:,}건")

st.markdown("### 01 / 데이터 시각화")
chart_controls = st.columns([1, 2])
with chart_controls[0]:
    metric_name = st.selectbox("표시 지표", ["주문량", "매출 지수"])
with chart_controls[1]:
    chart_style = st.segmented_control(
        "차트 유형",
        ["선형", "막대", "영역"],
        default="선형",
        label_visibility="collapsed",
    )

chart_data = monthly.set_index("월")[[metric_name]].copy()
if show_target:
    chart_data["목표"] = 450 if metric_name == "주문량" else 1900

if not monthly.empty:
    if chart_style == "막대":
        st.bar_chart(chart_data, color=["#1D5A45", "#B44732"] if show_target else "#1D5A45")
    elif chart_style == "영역":
        st.area_chart(chart_data, color=["#1D5A45", "#B44732"] if show_target else "#1D5A45")
    else:
        st.line_chart(chart_data, color=["#1D5A45", "#B44732"] if show_target else "#1D5A45")
else:
    st.info("차트를 표시하려면 사이드바에서 채널을 하나 이상 선택하세요.")

st.markdown("### 02 / 입력과 피드백")
widget_columns = st.columns([1.1, 0.9], gap="large")
with widget_columns[0]:
    st.markdown("#### 입력 폼")
    with st.form("feedback_form"):
        feedback = st.text_input("메모", placeholder="예: 다음 달 캠페인 확인")
        satisfaction = st.select_slider("화면 만족도", options=[1, 2, 3, 4, 5], value=4)
        submitted = st.form_submit_button("응답 기록", type="primary", icon=":material/check:")
    if submitted:
        st.success(f"응답을 기록했어요 · 만족도 {satisfaction}/5 · {feedback or '메모 없음'}")
    else:
        st.caption("폼 · 텍스트 입력 · 선택 슬라이더 · 제출 버튼")

with widget_columns[1]:
    st.markdown("#### 상태와 진행률")
    latest_progress = min(last_month_orders / 450, 1.0) if last_month_orders else 0.0
    st.progress(latest_progress, text=f"월간 목표 달성률 · {latest_progress:.0%}")
    st.success("데이터 연결 정상")
    st.info("필터 변경은 차트와 지표에 즉시 반영됩니다.")
    with st.expander("상태 메시지 더 보기"):
        st.warning("목표선은 비교를 위한 예시 데이터입니다.")
        st.caption("진행률 · 알림 · 펼침 영역")

st.markdown("### 03 / 데이터 테이블")
table_columns = st.columns([1, 2])
with table_columns[0]:
    search_text = st.text_input("표 검색", placeholder="월 또는 채널", icon=":material/search:")
with table_columns[1]:
    st.markdown('<p class="field-note">정렬, 열 크기 조정, 행 선택을 지원하는 데이터프레임</p>', unsafe_allow_html=True)

table_data = filtered.drop(columns="월 순서").copy()
if search_text:
    match = table_data.astype(str).apply(lambda column: column.str.contains(search_text, case=False)).any(axis=1)
    table_data = table_data[match]
st.dataframe(table_data, width="stretch", hide_index=True)
st.download_button(
    "CSV 다운로드",
    table_data.to_csv(index=False).encode("utf-8-sig"),
    file_name="streamlit-ui-sample.csv",
    mime="text/csv",
    icon=":material/download:",
)
