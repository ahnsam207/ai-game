import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import re
import subprocess

st.set_page_config(
    page_title="소개하기",
    page_icon="👩‍🏫",
    layout="wide"
)

st.markdown("""
<style>
:root {
    --label-color: #333;
    --date-color:  #666;
    --sub-color:   #555;
    --hr-color:    #e0e0e0;
}
@media (prefers-color-scheme: dark) {
    :root {
        --label-color: #e8e8e8;
        --date-color:  #aaaaaa;
        --sub-color:   #cccccc;
        --hr-color:    #444444;
    }
}
[data-theme="dark"] {
    --label-color: #e8e8e8;
    --date-color:  #aaaaaa;
    --sub-color:   #cccccc;
    --hr-color:    #444444;
}
.section-label-box {
    font-size: 14px;
    font-weight: 700;
    color: var(--label-color);
    line-height: 1.6;
    padding-top: 6px;
}
.section-subtitle {
    font-size: 12px;
    font-weight: 400;
    color: var(--sub-color);
    display: block;
    margin-top: 2px;
}
.section-date {
    font-size: 12px;
    font-weight: 400;
    color: var(--date-color);
    display: block;
    margin-top: 2px;
}
.section-hr {
    border: none;
    border-top: 1px solid var(--hr-color);
    margin: 4px 0 12px 0;
}
.title-name {
    margin: 0;
    font-size: 32px;
    font-weight: 800;
    color: var(--label-color);
}
</style>
""", unsafe_allow_html=True)

if "intro_page" not in st.session_state:
    st.session_state.intro_page = "소개"

project_root   = os.path.dirname(os.path.abspath(__file__))
sam_folder     = os.path.join(project_root, "sam", "ped")
intro_folder   = os.path.join(project_root, "sam", "intro")
edu_folder     = os.path.join(project_root, "sam", "edu")
make_folder    = os.path.join(project_root, "sam", "make")
gallery_folder = os.path.join(project_root, "sam", "gallery")

THUMB_W  = 180
THUMB_H  = 130
GAP      = 10
CAP_H    = 24
PER_ROW  = 5
IMG_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def natural_key(s):
    """파일명에서 숫자를 정수로 변환해 자연 정렬에 사용"""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]


def get_git_commit_time(filepath):
    """Git 커밋 로그에서 파일의 최초 커밋 시간(업로드 날짜)을 반환"""
    try:
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%ct", "--", filepath],
            capture_output=True, text=True
        )
        lines = result.stdout.strip().splitlines()
        if lines:
            return int(lines[-1])  # 최초 커밋 timestamp
    except Exception:
        pass
    return 0


def img_to_base64(img_path):
    ext  = img_path.split(".")[-1].lower()
    mime = "image/png" if ext == "png" else "image/jpeg"
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return mime, b64


def get_images_from_folder(folder, sort_by_date=False):
    if not os.path.exists(folder):
        return []
    paths = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in IMG_EXTS
    ]
    if sort_by_date:
        files = sorted(
            paths,
            key=lambda p: get_git_commit_time(p),
            reverse=True  # 최신 커밋(업로드)이 앞으로
        )
    else:
        files = sorted(
            paths,
            key=lambda p: natural_key(os.path.basename(p))
        )
    return [(f, 1, "cover") for f in files]


def calc_height(count, show_caption):
    rows  = max(1, (count + PER_ROW - 1) // PER_ROW)
    cap_h = CAP_H if show_caption else 0
    return rows * (THUMB_H + GAP + cap_h) + 60


def make_gallery_html(image_infos, show_caption=False):
    thumbs_html = ""
    for img_path, _, fit in image_infos:
        if os.path.exists(img_path):
            mime, b64 = img_to_base64(img_path)
            src      = "data:" + mime + ";base64," + b64
            obj      = "contain" if fit == "contain" else "cover"
            bg       = "#ebebeb" if fit == "contain" else "#d8d8d8"
            caption  = os.path.splitext(os.path.basename(img_path))[0] if show_caption else ""
            cap_html = '<div class="caption">' + caption + '</div>' if show_caption else ""
            thumbs_html += (
                '<div class="thumb-wrap">'
                '<div class="thumb-cell">'
                '<img src="' + src + '" data-full="' + src + '" '
                'style="object-fit:' + obj + '; background:' + bg + ';" '
                'onmouseenter="showPopup(this)" onmouseleave="hidePopup()">'
                '</div>'
                + cap_html +
                '</div>'
            )
        else:
            name = os.path.basename(img_path)
            thumbs_html += (
                '<div class="thumb-wrap">'
                '<div class="thumb-cell error">'
                '파일 없음<br><small>' + name + '</small>'
                '</div>'
                '</div>'
            )

    count  = len(image_infos)
    height = calc_height(count, show_caption)

    html = (
        "<!DOCTYPE html><html><head><style>"
        "* { box-sizing: border-box; margin: 0; padding: 0; }"
        "html, body { background: transparent; overflow-x: hidden; overflow-y: auto; }"
        ".gallery { display: flex; flex-wrap: wrap; gap: " + str(GAP) + "px; padding: 4px 2px 8px 2px; }"
        ".thumb-wrap { display: flex; flex-direction: column; align-items: center; width: " + str(THUMB_W) + "px; }"
        ".thumb-cell {"
        "  width: " + str(THUMB_W) + "px; height: " + str(THUMB_H) + "px;"
        "  border-radius: 8px; overflow: hidden;"
        "  box-shadow: 0 1px 6px rgba(0,0,0,0.15);"
        "  cursor: zoom-in; flex-shrink: 0;"
        "}"
        ".thumb-cell img { width: 100%; height: 100%; display: block; }"
        ".thumb-cell.error {"
        "  display: flex; align-items: center; justify-content: center;"
        "  text-align: center; font-size: 11px; color: #c00;"
        "  border: 1px dashed #c00; background: #fff0f0;"
        "}"
        ".caption {"
        "  font-size: 11px; color: #666; margin-top: 4px;"
        "  text-align: center; width: 100%;"
        "  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
        "}"
        "</style></head><body>"
        "<script>"
        "(function() {"
        "  if (parent.document.getElementById('hpop-overlay')) return;"
        "  var ov = parent.document.createElement('div');"
        "  ov.id = 'hpop-overlay';"
        "  ov.style.cssText = 'display:none;position:fixed;inset:0;"
        "    background:rgba(0,0,0,0.75);z-index:99999;"
        "    align-items:center;justify-content:center;pointer-events:none;';"
        "  var img = parent.document.createElement('img');"
        "  img.id = 'hpop-img';"
        "  img.style.cssText = 'max-width:70vw;max-height:70vh;object-fit:contain;"
        "    border-radius:10px;box-shadow:0 8px 32px rgba(0,0,0,.55);';"
        "  ov.appendChild(img);"
        "  parent.document.body.appendChild(ov);"
        "})();"
        "function showPopup(el){"
        "  var ov=parent.document.getElementById('hpop-overlay');"
        "  var img=parent.document.getElementById('hpop-img');"
        "  if(!ov||!img)return;"
        "  img.src=el.dataset.full;"
        "  ov.style.display='flex';"
        "}"
        "function hidePopup(){"
        "  var ov=parent.document.getElementById('hpop-overlay');"
        "  if(ov)ov.style.display='none';"
        "}"
        "</script>"
        '<div class="gallery">' + thumbs_html + "</div>"
        "</body></html>"
    )
    return html, height


def show_section_auto(label, subtitle, date, folder, show_caption=True, sort_by_date=False):
    image_infos = get_images_from_folder(folder, sort_by_date=sort_by_date)

    if not image_infos:
        placeholder_html = (
            "<!DOCTYPE html><html><head><style>"
            "* { box-sizing:border-box; margin:0; padding:0; }"
            "body { background:transparent; overflow:hidden; }"
            "</style></head><body>"
            '<div style="width:' + str(THUMB_W) + 'px; height:' + str(THUMB_H) + 'px;'
            ' border-radius:8px; border:2px dashed #bbb;'
            ' background:linear-gradient(135deg,#f0f0f0,#e0e0e0);'
            ' display:flex; align-items:center; justify-content:center;'
            ' font-size:12px; color:#888; text-align:center; line-height:1.6;">'
            '🖼️<br>사진 준비중</div>'
            "</body></html>"
        )
        html, height = placeholder_html, THUMB_H + 20
    else:
        html, height = make_gallery_html(image_infos, show_caption=show_caption)

    label_col, gallery_col = st.columns([1, 5])
    with label_col:
        subtitle_html = '<span class="section-subtitle">' + subtitle + '</span>' if subtitle else ""
        st.markdown(
            '<div class="section-label-box">'
            + label + subtitle_html
            + '<span class="section-date">' + date + '</span>'
            + '</div>',
            unsafe_allow_html=True
        )
    with gallery_col:
        components.html(html, height=height, scrolling=True)  # scrolling=True

    st.markdown("<hr class='section-hr'>", unsafe_allow_html=True)


def show_section(label, subtitle, date, image_infos):
    html, height = make_gallery_html(image_infos, show_caption=False)

    label_col, gallery_col = st.columns([1, 5])
    with label_col:
        subtitle_html = f'<span class="section-subtitle">{subtitle}</span>' if subtitle else ""
        st.markdown(f"""
<div class="section-label-box">
  {label}
  {subtitle_html}
  <span class="section-date">{date}</span>
</div>""", unsafe_allow_html=True)
    with gallery_col:
        components.html(html, height=height, scrolling=True)  # scrolling=True

    st.markdown("<hr class='section-hr'>", unsafe_allow_html=True)


# ── 타이틀 ──────────────────────────────────────────
icon_path = os.path.join(intro_folder, "icon.PNG")
if os.path.exists(icon_path):
    mime, b64 = img_to_base64(icon_path)
    st.markdown(f"""
<div style="display:flex; align-items:center; gap:16px; margin-bottom:8px;">
    <img src="data:{mime};base64,{b64}"
         style="height:60px; width:auto; object-fit:contain;">
    <h1 class="title-name">안이옥 선생님</h1>
</div>""", unsafe_allow_html=True)
else:
    st.title("👩‍🏫 안이옥 선생님")

# ── 상단 메뉴 ──────────────────────────────────────
mc    = st.columns(5)
pages = ["소개", "교육활동", "제작", "발자취", "갤러리"]
icons = ["👩‍🏫", "📚", "🛠️", "👣", "🖼️"]
for col, page, icon in zip(mc, pages, icons):
    with col:
        if st.button(f"{icon} {page}", key=f"btn_{page}",
                     use_container_width=True,
                     type="primary" if st.session_state.intro_page == page else "secondary"):
            st.session_state.intro_page = page


# ══════════════════════════════════════════════════
# 소개
# ══════════════════════════════════════════════════
if st.session_state.intro_page == "소개":
    intro_img = os.path.join(intro_folder, "intro.jpg")
    if os.path.exists(intro_img):
        st.image(intro_img, use_container_width=True)
    else:
        st.markdown("""
<div style="background:linear-gradient(135deg,#a8edea 0%,#fed6e3 100%);
     border-radius:16px; padding:60px; text-align:center; margin:20px 0;">
    <div style="font-size:80px;">👩‍🏫</div>
</div>""", unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 기본 정보")
        st.markdown("""
| | |
|---|---|
| 👩‍🏫 | 안이옥 선생님 |
| 📚 | 정보 · 컴퓨터 교과 |
| 🏫 | 경복비즈니스고등학교 |
| 📧 | 2ok25@daum.net |
| ⏰ | 월-금 08:20 ~ 16:20 |
""")
    with col2:
        st.subheader("🏆 담당 교과")
        st.markdown("""
| | 교과명 |
|---|---|
| 🖨️ | 3D프린터제품제작 |
| 💻 | 프로그래밍 |
| 🔌 | 디지털논리회로 |
| 📱 | 스마트문화앱콘텐츠제작 |
| 📊 | 비즈니스엑셀 |
| 🗂️ | 기타 정보관련 교과 |
""")
    st.divider()
    st.subheader("💬 선생님 한마디")
    st.success("""
💡 **"배움은 즐거운 도전입니다!"**

함께 새로운 기술을 배우고 멋진 결과물을 만들어 봐요.
궁금한 점이 있으면 언제든지 질문하세요. 언제나 응원합니다! 😊
""")
    st.divider()
    st.caption("© 2026 안이옥 선생님 소개 페이지")


# ══════════════════════════════════════════════════
# 교육활동
# ══════════════════════════════════════════════════
elif st.session_state.intro_page == "교육활동":
    st.header("📚 교육활동")
    st.caption("사진 위에 마우스를 올리면 확대해서 볼 수 있습니다.")
    st.divider()

    show_section_auto("✈️ 영마이스터 해외연수", "",          "2025년 호주",        os.path.join(edu_folder, "young"))
    show_section_auto("🌟 미인반 활동",       "미래인재반", "2024 ~ 2025년", os.path.join(edu_folder, "miin"))
    show_section_auto("🎓 동아리 특별활동",     "",          "2023년 알고리즘",        os.path.join(edu_folder, "club"))
    show_section_auto("🏙️ 강서구 샌드박스",  "",          "2023년 강서 미래인재 한마당",        os.path.join(edu_folder, "sandbox"))


# ══════════════════════════════════════════════════
# 제작
# ══════════════════════════════════════════════════
elif st.session_state.intro_page == "제작":
    st.header("🛠️ 제작")
    st.caption("사진 위에 마우스를 올리면 확대해서 볼 수 있습니다.")
    st.divider()

    show_section_auto("🚗 무선 조종 1인승 전기차", "", "", os.path.join(make_folder, "car"))
    show_section_auto("🚙 무선 조종 RC Car",       "", "", os.path.join(make_folder, "rc"))
    show_section_auto("🌱 스마트팜 만들기",        "", "", os.path.join(make_folder, "farm"))
    show_section_auto("🔌 선없는 실습실 만들기",   "", "", os.path.join(make_folder, "lab"))
    show_section_auto("🔧 이것저것",              "", "", os.path.join(make_folder, "maker"))


# ══════════════════════════════════════════════════
# 발자취
# ══════════════════════════════════════════════════
elif st.session_state.intro_page == "발자취":
    st.header("👣 발자취")
    st.caption("사진 위에 마우스를 올리면 확대해서 볼 수 있습니다.")
    st.divider()

    show_section(
        "📰 숙명여자대학원 재학중", "AI융합전공", "2025.09 입학",
        [(os.path.join(sam_folder, "sook.jpg"), 1, "cover")]
    )
    show_section(
        "📰 전자신문 기사", "무선 조종 1인승 전기차 제작", "2025.12.29",
        [
            (os.path.join(sam_folder, "intro1.jpg"), 1, "cover"),
            (os.path.join(sam_folder, "intro2.jpg"), 1, "cover"),
            (os.path.join(sam_folder, "intro3.jpg"), 1, "cover"),
        ]
    )
    show_section(
        "🏆 교육부 장관상 수상", "정보과학분야 우수교사 공모전", "2025.10.29",
        [
            (os.path.join(sam_folder, "intro4.jpg"), 1, "cover"),
            (os.path.join(sam_folder, "intro5.jpg"), 1, "cover"),
            (os.path.join(sam_folder, "intro6.jpg"), 1, "cover"),
            (os.path.join(sam_folder, "intro7.jpg"), 1, "cover"),
        ]
    )
    show_section(
        "📌 AI 로봇 피지컬 강사", "강서양천 교육청 교사 대상", "2024.10.31",
        [
            (os.path.join(sam_folder, "intro8.jpg"),  1, "cover"),
            (os.path.join(sam_folder, "intro9.jpg"),  1, "cover"),
            (os.path.join(sam_folder, "intro10.jpg"), 1, "contain"),
            (os.path.join(sam_folder, "intro11.jpg"), 1, "cover"),
        ]
    )
    show_section(
        "🏅 서울시 교육감 표창", "우수교사 부문", "2022.05.15",
        [(os.path.join(sam_folder, "intro12.jpg"), 1, "cover")]
    )


# ══════════════════════════════════════════════════
# 갤러리
# ══════════════════════════════════════════════════
elif st.session_state.intro_page == "갤러리":
    st.header("🖼️ 갤러리")
    st.caption("사진 위에 마우스를 올리면 확대해서 볼 수 있습니다.")
    st.divider()

    show_section_auto("🚴 라이딩 기록", "", "", os.path.join(gallery_folder, "riding"), sort_by_date=True)
    show_section_auto("☀️ 일상",       "", "", os.path.join(gallery_folder, "daily"),   sort_by_date=True)
    show_section_auto("📌 기타",       "", "", os.path.join(gallery_folder, "etc"),     sort_by_date=True)
