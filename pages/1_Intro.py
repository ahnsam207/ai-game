import streamlit as st


st.set_page_config(
	page_title="자기소개 | Portfolio",
	page_icon="✳",
	layout="wide",
	initial_sidebar_state="collapsed",
)

PAGE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
	--paper: #f2f3ed;
	--ink: #202720;
	--muted: #687168;
	--green: #205947;
	--coral: #dc6a4e;
	--lime: #e3eb9e;
	--line: #d6dbd1;
}

.stApp,
[data-testid="stAppViewContainer"] {
	background-color: var(--paper);
	color: var(--ink);
	font-family: "DM Sans", sans-serif;
}

[data-testid="stHeader"] {
	background: transparent;
}

.block-container {
	max-width: 1200px;
	padding: 24px 42px 48px;
}

.intro-page {
	color: var(--ink);
	font-family: "DM Sans", sans-serif;
	background-image: linear-gradient(rgba(32, 39, 32, 0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(32, 39, 32, 0.025) 1px, transparent 1px);
	background-size: 28px 28px;
	animation: arrive 650ms ease-out both;
}

.intro-page * {
	box-sizing: border-box;
}

.intro-nav {
	min-height: 54px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	border-bottom: 1px solid var(--line);
	margin-bottom: 54px;
}

.intro-mark,
.intro-nav-links,
.eyebrow,
.section-kicker,
.hero-index,
.project-meta,
.contact-label {
	font-family: "Space Grotesk", sans-serif;
	font-size: 12px;
	font-weight: 600;
	line-height: 1.4;
}

.intro-mark {
	color: var(--green);
}

.intro-nav-links {
	display: flex;
	gap: 26px;
}

.intro-nav-links a,
.intro-actions a,
.project-row a,
.contact-link {
	color: inherit;
	text-decoration: none;
}

.intro-nav-links a:hover,
.project-row a:hover {
	color: var(--coral);
}

.hero {
	display: grid;
	grid-template-columns: 1.05fr 0.95fr;
	align-items: center;
	gap: 56px;
	padding-bottom: 92px;
}

.eyebrow,
.section-kicker {
	color: var(--green);
	text-transform: uppercase;
}

.eyebrow::before {
	content: "";
	display: inline-block;
	width: 8px;
	height: 8px;
	background: var(--coral);
	border-radius: 50%;
	margin-right: 9px;
}

.hero h1 {
	max-width: 590px;
	margin: 22px 0 20px;
	font-family: "Space Grotesk", sans-serif;
	font-size: 64px;
	font-weight: 600;
	line-height: 1.06;
	letter-spacing: 0;
}

.hero h1 span {
	color: var(--green);
}

.hero-copy {
	max-width: 470px;
	color: #515c52;
	font-size: 17px;
	line-height: 1.8;
}

.intro-actions {
	display: flex;
	align-items: center;
	flex-wrap: wrap;
	gap: 24px;
	margin-top: 30px;
}

.action-primary {
	display: inline-flex;
	align-items: center;
	gap: 18px;
	min-height: 48px;
	padding: 0 18px;
	background: var(--green);
	color: white !important;
	font-size: 14px;
	font-weight: 600;
	transition: background 160ms ease, transform 160ms ease;
}

.action-primary:hover {
	background: #173f33;
	transform: translateY(-2px);
}

.action-primary::after {
	content: "↘";
	font-size: 18px;
}

.action-secondary {
	color: var(--ink);
	font-size: 14px;
	font-weight: 600;
	text-decoration: underline !important;
	text-decoration-color: var(--coral) !important;
	text-underline-offset: 5px;
}

.hero-visual {
	position: relative;
	padding: 0 0 36px 28px;
}

.hero-visual::before {
	content: "";
	position: absolute;
	inset: 28px 28px 64px 0;
	background: var(--lime);
}

.hero-photo {
	position: relative;
	display: block;
	width: 100%;
	aspect-ratio: 1.14 / 1;
	object-fit: cover;
	filter: saturate(0.78);
}

.hero-index {
	position: absolute;
	right: 0;
	bottom: 0;
	display: flex;
	align-items: center;
	gap: 12px;
	color: var(--green);
}

.hero-index span {
	width: 34px;
	height: 1px;
	background: var(--coral);
}

.intro-section {
	border-top: 1px solid var(--line);
	padding: 32px 0 72px;
	scroll-margin-top: 24px;
}

.about-grid {
	display: grid;
	grid-template-columns: 0.65fr 1.35fr;
	gap: 48px;
}

.section-kicker {
	margin: 4px 0 0;
}

.about-copy h2,
.section-heading {
	margin: 0 0 16px;
	font-family: "Space Grotesk", sans-serif;
	font-size: 34px;
	font-weight: 600;
	line-height: 1.2;
	letter-spacing: 0;
}

.about-copy p,
.section-intro {
	max-width: 680px;
	margin: 0;
	color: var(--muted);
	font-size: 15px;
	line-height: 1.85;
}

.interest-list {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	border-top: 1px solid var(--line);
	margin-top: 34px;
}

.interest-item {
	padding: 18px 20px 0 0;
}

.interest-number {
	display: block;
	margin-bottom: 24px;
	color: var(--coral);
	font-family: "Space Grotesk", sans-serif;
	font-size: 12px;
	font-weight: 600;
}

.interest-item h3 {
	margin: 0 0 8px;
	font-size: 16px;
	font-weight: 700;
}

.interest-item p {
	max-width: 270px;
	margin: 0;
	color: var(--muted);
	font-size: 13px;
	line-height: 1.7;
}

.project-list {
	margin-top: 28px;
}

.project-row {
	display: grid;
	grid-template-columns: 64px 1fr auto;
	align-items: center;
	gap: 20px;
	min-height: 88px;
	border-top: 1px solid var(--line);
}

.project-row:last-child {
	border-bottom: 1px solid var(--line);
}

.project-number {
	color: var(--coral);
	font-family: "Space Grotesk", sans-serif;
	font-size: 13px;
}

.project-row h3 {
	margin: 0 0 5px;
	font-size: 17px;
	font-weight: 600;
}

.project-row p {
	margin: 0;
	color: var(--muted);
	font-size: 13px;
}

.project-meta {
	color: var(--muted);
	text-align: right;
}

.contact-band {
	display: grid;
	grid-template-columns: 1fr auto;
	align-items: end;
	gap: 32px;
	padding: 38px 42px;
	background: var(--green);
	color: white;
	scroll-margin-top: 24px;
}

.contact-label {
	margin: 0 0 16px;
	color: var(--lime);
	text-transform: uppercase;
}

.contact-band h2 {
	max-width: 600px;
	margin: 0;
	font-family: "Space Grotesk", sans-serif;
	font-size: 38px;
	font-weight: 500;
	line-height: 1.2;
	letter-spacing: 0;
}

.contact-link {
	display: inline-flex;
	align-items: center;
	gap: 12px;
	min-height: 46px;
	padding: 0 16px;
	background: var(--lime);
	color: var(--ink);
	font-size: 14px;
	font-weight: 700;
	white-space: nowrap;
}

.contact-link::after {
	content: "↗";
	font-size: 17px;
}

.intro-footer {
	display: flex;
	justify-content: space-between;
	gap: 16px;
	padding-top: 18px;
	color: var(--muted);
	font-size: 12px;
}

a:focus-visible {
	outline: 2px solid var(--coral);
	outline-offset: 4px;
}

@keyframes arrive {
	from { opacity: 0; transform: translateY(10px); }
	to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 800px) {
	.block-container {
		padding: 18px 22px 32px;
	}

	.intro-nav {
		margin-bottom: 34px;
	}

	.hero {
		grid-template-columns: 1fr;
		gap: 32px;
		padding-bottom: 58px;
	}

	.hero h1 {
		font-size: 48px;
	}

	.hero-visual {
		max-width: 600px;
	}

	.about-grid {
		grid-template-columns: 1fr;
		gap: 20px;
	}

	.intro-section {
		padding-bottom: 52px;
	}

	.contact-band {
		grid-template-columns: 1fr;
		justify-items: start;
		padding: 30px 24px;
	}
}

@media (max-width: 520px) {
	.intro-nav-links {
		gap: 14px;
		font-size: 11px;
	}

	.hero h1 {
		font-size: 40px;
	}

	.hero-copy {
		font-size: 15px;
	}

	.interest-list {
		grid-template-columns: 1fr;
	}

	.interest-item {
		display: grid;
		grid-template-columns: 38px 1fr;
		column-gap: 10px;
		padding: 18px 0;
		border-bottom: 1px solid var(--line);
	}

	.interest-number {
		grid-row: span 2;
		margin: 2px 0 0;
	}

	.project-row {
		grid-template-columns: 34px 1fr;
		gap: 12px;
		padding: 14px 0;
	}

	.project-meta {
		grid-column: 2;
		text-align: left;
	}

	.contact-band h2 {
		font-size: 30px;
	}

	.intro-footer {
		flex-direction: column;
	}
}

@media (prefers-reduced-motion: reduce) {
	.intro-page {
		animation: none;
	}

	*, *::before, *::after {
		scroll-behavior: auto !important;
		transition-duration: 0.01ms !important;
	}
}
</style>

<div class="intro-page">
  <header class="intro-nav">
	<div class="intro-mark">[YOUR NAME] <span style="color:#dc6a4e">/</span> PORTFOLIO</div>
	<nav class="intro-nav-links" aria-label="페이지 메뉴">
	  <a href="#about">소개</a>
	  <a href="#work">작업물</a>
	  <a href="#contact">연락</a>
	</nav>
  </header>

  <main>
	<section class="hero" aria-labelledby="intro-title">
	  <div class="hero-text">
		<p class="eyebrow">A LITTLE INTRODUCTION</p>
		<h1 id="intro-title">안녕하세요,<br /><span>[이름]</span>입니다.</h1>
		<p class="hero-copy">[관심 분야]를 탐구하는 [직무 또는 역할]. 새로운 것을 배우고 직접 만들며, 일상의 문제를 더 나은 경험으로 바꿉니다.</p>
		<div class="intro-actions">
		  <a class="action-primary" href="#work">작업물 보기</a>
		  <a class="action-secondary" href="#about">나에 대해</a>
		</div>
	  </div>
	  <div class="hero-visual">
		<img class="hero-photo" src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&amp;fit=crop&amp;w=1200&amp;q=85" alt="따뜻한 빛이 비치는 창작자의 작업 공간" />
		<div class="hero-index">01 <span></span> CURIOUS BY NATURE</div>
	  </div>
	</section>

	<section class="intro-section" id="about" aria-labelledby="about-title">
	  <div class="about-grid">
		<p class="section-kicker">01 / ABOUT</p>
		<div class="about-copy">
		  <h2 id="about-title">호기심을 관찰하고,<br />작은 시도로 답을 찾습니다.</h2>
		  <p>[어떤 일을 좋아하고 어떻게 일하는지 소개해 보세요.] 관심을 가진 계기, 중요하게 생각하는 가치, 요즘 집중하고 있는 일을 두세 문장으로 적으면 나만의 소개가 완성됩니다.</p>
		</div>
	  </div>

	  <div class="interest-list">
		<article class="interest-item">
		  <span class="interest-number">01</span>
		  <h3>[관심 분야 하나]</h3>
		  <p>요즘 깊이 들여다보고 있는 주제와 그 이유를 적어보세요.</p>
		</article>
		<article class="interest-item">
		  <span class="interest-number">02</span>
		  <h3>[관심 분야 둘]</h3>
		  <p>좋아하는 도구나 분야에서 어떤 가능성을 찾는지 소개해 보세요.</p>
		</article>
		<article class="interest-item">
		  <span class="interest-number">03</span>
		  <h3>[관심 분야 셋]</h3>
		  <p>계속 배우고 싶은 것, 다음에 시도해 보고 싶은 것을 적어보세요.</p>
		</article>
	  </div>
	</section>

	<section class="intro-section" id="work" aria-labelledby="work-title">
	  <p class="section-kicker">02 / SELECTED WORK</p>
	  <h2 class="section-heading" id="work-title">작업물</h2>
	  <p class="section-intro">기억에 남는 프로젝트를 골라 역할과 결과를 짧게 덧붙여 보세요.</p>
	  <div class="project-list">
		<article class="project-row">
		  <span class="project-number">01</span>
		  <div><h3>[프로젝트 이름]</h3><p>무엇을 만들었고 어떤 문제를 해결했는지 한 줄로 소개합니다.</p></div>
		  <span class="project-meta">[분야] &middot; [연도]</span>
		</article>
		<article class="project-row">
		  <span class="project-number">02</span>
		  <div><h3>[프로젝트 이름]</h3><p>나의 역할과 작업을 통해 배운 점을 간결하게 적어보세요.</p></div>
		  <span class="project-meta">[분야] &middot; [연도]</span>
		</article>
		<article class="project-row">
		  <span class="project-number">03</span>
		  <div><h3>[프로젝트 이름]</h3><p>결과나 변화를 숫자 또는 구체적인 문장으로 보여주세요.</p></div>
		  <span class="project-meta">[분야] &middot; [연도]</span>
		</article>
	  </div>
	</section>

	<section class="contact-band" id="contact" aria-labelledby="contact-title">
	  <div>
		<p class="contact-label">03 / SAY HELLO</p>
		<h2 id="contact-title">좋은 질문과 새로운 만남은 언제나 환영합니다.</h2>
	  </div>
	  <a class="contact-link" href="mailto:hello@example.com">hello@example.com</a>
	</section>
  </main>

  <footer class="intro-footer">
	<span>[이름] &middot; PERSONAL PORTFOLIO</span>
	<span>MADE WITH CURIOSITY &copy; 2026</span>
  </footer>
</div>

<script>
if (!document.documentElement.dataset.introNavigationReady) {
	document.documentElement.dataset.introNavigationReady = "true";
	document.addEventListener("click", (event) => {
		const link = event.target.closest(".intro-page a[href^='#']");
		if (!link) return;

		const section = document.getElementById(link.hash.slice(1));
		if (!section) return;

		event.preventDefault();
		section.scrollIntoView({ behavior: "smooth", block: "start" });
		window.history.replaceState(null, "", link.hash);
	});
}
</script>
"""

st.html(PAGE, unsafe_allow_javascript=True)
