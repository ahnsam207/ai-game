from math import ceil, sqrt
from io import BytesIO

import pandas as pd
import streamlit as st


st.set_page_config(page_title="데이터 스튜디오", page_icon="📊", layout="wide")


def make_sample_data():
	return pd.DataFrame(
		{
			"월": [f"{month}월" for month in range(1, 13)],
			"매출(백만원)": [42, 38, 51, 57, 63, 72, 68, 76, 84, 91, 105, 128],
			"주문 수": [310, 286, 352, 391, 428, 476, 451, 502, 548, 603, 691, 824],
			"광고비(백만원)": [8, 7, 9, 10, 11, 13, 12, 14, 16, 17, 20, 24],
			"만족도": [4.1, 4.0, 4.2, 4.3, 4.4, 4.5, 4.3, 4.5, 4.6, 4.5, 4.7, 4.8],
			"지역": ["서울", "부산", "서울", "대구", "서울", "부산", "대구", "서울", "부산", "대구", "서울", "부산"],
		}
	)


st.title("데이터 스튜디오")
st.caption("직접 입력하거나 CSV를 불러와 데이터의 패턴을 살펴보세요.")

uploaded_file = st.file_uploader("CSV 파일", type=["csv"], help="파일을 올리지 않으면 아래 예시 데이터가 열립니다.")

if uploaded_file is not None:
	try:
		source_data = pd.read_csv(BytesIO(uploaded_file.getvalue()))
	except (UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
		st.error(f"CSV 파일을 읽지 못했습니다: {error}")
		st.stop()
else:
	source_data = make_sample_data()

if source_data.empty or len(source_data.columns) == 0:
	st.warning("시각화할 데이터가 없습니다. 다른 CSV 파일을 선택해 주세요.")
	st.stop()

st.subheader("데이터 편집")
st.caption("표의 셀을 수정하거나 행을 추가·삭제할 수 있습니다. 변경 내용은 아래 차트에 바로 반영됩니다.")
editor_key = f"data_editor_{uploaded_file.name if uploaded_file else 'sample'}"
data = st.data_editor(
	source_data,
	num_rows="dynamic",
	width="stretch",
	key=editor_key,
)

if data.empty:
	st.info("행을 추가해 데이터를 입력하면 시각화를 시작할 수 있습니다.")
	st.stop()

numeric_columns = data.select_dtypes(include="number").columns.tolist()
category_columns = [column for column in data.columns if column not in numeric_columns]

st.subheader("차트 만들기")
chart_type = st.radio(
	"차트 유형",
	["선형", "막대", "영역", "산점도", "히스토그램", "도넛"],
	horizontal=True,
)

if not numeric_columns:
	st.warning("차트에 사용할 숫자 열이 없습니다. 데이터 표에서 숫자 열을 추가하거나 CSV를 확인해 주세요.")
	st.stop()

control_columns = st.columns(3)
if chart_type == "히스토그램":
	y_axis = control_columns[0].selectbox("분포를 볼 숫자 열", numeric_columns)
	st.caption("히스토그램은 선택한 숫자 열의 값 분포를 구간별로 보여줍니다.")
else:
	if chart_type == "산점도":
		if len(numeric_columns) < 2:
			st.warning("산점도에는 숫자 열이 두 개 이상 필요합니다.")
			st.stop()
		x_options = numeric_columns
	elif chart_type == "도넛":
		if not category_columns:
			st.warning("도넛 차트에는 항목을 구분할 문자 열이 필요합니다.")
			st.stop()
		x_options = category_columns
	else:
		x_options = data.columns.tolist()

	x_axis = control_columns[0].selectbox("가로축", x_options)
	y_axis = control_columns[1].selectbox("세로축", numeric_columns)
	color_options = ["사용 안 함"] + category_columns
	color_column = control_columns[2].selectbox("색상 구분", color_options)

chart_frame = data.dropna(subset=[y_axis]).copy()
if chart_type != "히스토그램":
	required_columns = [x_axis]
	if color_column != "사용 안 함":
		required_columns.append(color_column)
	chart_frame = chart_frame.dropna(subset=required_columns)

if chart_frame.empty:
	st.info("선택한 열에 표시할 데이터가 없습니다. 축이나 입력값을 확인해 주세요.")
else:
	if chart_type == "히스토그램":
		values = pd.to_numeric(chart_frame[y_axis], errors="coerce").dropna()
		if values.empty:
			st.info("숫자로 읽을 수 있는 값이 없습니다.")
		else:
			bin_count = min(20, max(5, ceil(sqrt(len(values)))))
			bins = pd.cut(values, bins=bin_count)
			histogram = bins.value_counts(sort=False)
			histogram_data = pd.DataFrame(
				{"구간": histogram.index.astype(str), "개수": histogram.to_numpy()}
			)
			st.bar_chart(histogram_data, x="구간", y="개수", width="stretch")
	elif chart_type == "도넛":
		st.vega_lite_chart(
			chart_frame,
			{
				"mark": {"type": "arc", "innerRadius": 64},
				"encoding": {
					"theta": {"field": y_axis, "type": "quantitative", "aggregate": "sum"},
					"color": {"field": x_axis, "type": "nominal"},
					"tooltip": [
						{"field": x_axis, "type": "nominal"},
						{"field": y_axis, "type": "quantitative", "aggregate": "sum"},
					],
				},
				"height": 360,
			},
			width="stretch",
		)
	else:
		chart_function = {
			"선형": st.line_chart,
			"막대": st.bar_chart,
			"영역": st.area_chart,
			"산점도": st.scatter_chart,
		}[chart_type]
		chart_function(
			chart_frame,
			x=x_axis,
			y=y_axis,
			color=None if color_column == "사용 안 함" else color_column,
			width="stretch",
		)

st.subheader("데이터 요약")
summary_columns = st.columns(3)
summary_columns[0].metric("행", f"{len(data):,}")
summary_columns[1].metric("열", f"{len(data.columns):,}")
summary_columns[2].metric("숫자 열", f"{len(numeric_columns):,}")

if numeric_columns:
	with st.expander("숫자 열 통계 보기"):
		st.dataframe(data[numeric_columns].describe().T, width="stretch")
