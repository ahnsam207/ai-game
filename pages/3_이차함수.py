import matplotlib.pyplot as plt
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import streamlit as st


st.set_page_config(page_title="이차함수 그래프", page_icon="📈")


@st.cache_resource
def load_korean_font():
	font_path = Path(__file__).resolve().parent.parent / "fonts" / "NotoSansKR-Black.ttf"
	font_manager.fontManager.addfont(str(font_path))
	return font_manager.FontProperties(fname=str(font_path))


korean_font = load_korean_font()
plt.rcParams["font.family"] = korean_font.get_name()
plt.rcParams["axes.unicode_minus"] = False

st.title("이차함수 그래프")
st.latex(r"y = ax^2 + bx + c")

coefficient_columns = st.columns(3)
with coefficient_columns[0]:
	coefficient_a = st.number_input("a", value=1.0, step=0.5)
with coefficient_columns[1]:
	coefficient_b = st.number_input("b", value=-2.0, step=0.5)
with coefficient_columns[2]:
	coefficient_c = st.number_input("c", value=-3.0, step=0.5)

x_min, x_max = st.slider(
	"x축 범위",
	min_value=-20.0,
	max_value=20.0,
	value=(-10.0, 10.0),
	step=0.5,
)

if coefficient_a == 0:
	st.warning("이차함수가 되려면 a는 0이 아니어야 합니다.")
	st.stop()

x_values = [x_min + (x_max - x_min) * index / 400 for index in range(401)]
y_values = [
	coefficient_a * x**2 + coefficient_b * x + coefficient_c
	for x in x_values
]
vertex_x = -coefficient_b / (2 * coefficient_a)
vertex_y = coefficient_a * vertex_x**2 + coefficient_b * vertex_x + coefficient_c

figure, axis = plt.subplots(figsize=(9, 5))
axis.plot(x_values, y_values, color="#176b58", linewidth=2.5, label="y = ax² + bx + c")
axis.scatter(vertex_x, vertex_y, color="#d76446", zorder=3, label="꼭짓점")
axis.annotate(
	f"({vertex_x:.2f}, {vertex_y:.2f})",
	(vertex_x, vertex_y),
	xytext=(8, 8),
	textcoords="offset points",
)
axis.axhline(0, color="#687168", linewidth=0.8)
axis.axvline(0, color="#687168", linewidth=0.8)
axis.set_xlim(x_min, x_max)
axis.set_xlabel("x값")
axis.set_ylabel("y값")
axis.set_title(f"y = {coefficient_a:g}x² {coefficient_b:+g}x {coefficient_c:+g}")
axis.grid(True, linestyle="--", alpha=0.35)
axis.legend()
figure.tight_layout()
st.pyplot(figure)
plt.close(figure)
