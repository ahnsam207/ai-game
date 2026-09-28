import base64
import csv
import io
import json
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="영단어 맞추기 게임", page_icon="🎯", layout="wide")


def parse_word_csv(file_bytes):
	for encoding in ("utf-8-sig", "cp949"):
		try:
			text = file_bytes.decode(encoding)
			break
		except UnicodeDecodeError:
			continue
	else:
		raise ValueError("CSV 인코딩을 읽을 수 없습니다. UTF-8 또는 CP949 파일을 사용해 주세요.")

	words = []
	seen = set()
	reader = csv.reader(io.StringIO(text))
	for row_number, row in enumerate(reader):
		if len(row) < 2:
			continue
		word = row[0].strip()
		meanings = [meaning.strip() for meaning in row[1:] if meaning.strip()]
		if not word or not meanings:
			continue
		if row_number == 0 and word.lower() in {"word", "english", "영단어", "영어단어", "단어"}:
			continue
		if word.casefold() in seen:
			continue
		seen.add(word.casefold())
		words.append({"word": word, "meanings": meanings})

	if not words:
		raise ValueError("영단어와 한글 뜻이 들어 있는 행을 찾지 못했습니다.")
	if len(words) < 5:
		raise ValueError("게임을 하려면 중복되지 않는 영단어가 5개 이상 필요합니다.")
	return words


def build_game_html(words):
	word_data = json.dumps(words, ensure_ascii=False).replace("<", "\\u003c")
	return r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root { color-scheme: light; font-family: "Noto Sans KR", "Malgun Gothic", sans-serif; }
* { box-sizing: border-box; }
body { margin: 0; color: #202720; background: transparent; }
.game { --sky: #eaf4ee; --accent: #205947; max-width: 960px; margin: 0 auto; }
.topline { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; }
.stats { display: flex; flex-wrap: wrap; gap: 8px; }
.stat { min-width: 104px; padding: 8px 12px; border: 1px solid #d5dfd6; border-radius: 8px; background: #fff; font-size: 14px; }
.stat strong { color: var(--accent); }
.music-toggle { min-height: 38px; padding: 0 12px; border: 1px solid #b7c9bc; border-radius: 6px; background: #fff; color: #202720; font: inherit; font-size: 13px; font-weight: 700; cursor: pointer; }
.music-toggle:hover { border-color: var(--accent); }
.meaning { min-height: 72px; display: flex; align-items: center; gap: 12px; margin-bottom: 10px; padding: 12px 16px; border-left: 4px solid var(--accent); border-radius: 6px; background: #fff; }
.meaning-label { flex: 0 0 auto; color: #657268; font-size: 13px; }
#meaning { font-size: 20px; font-weight: 700; overflow-wrap: anywhere; }
.arena { position: relative; height: 560px; overflow: hidden; border: 1px solid #cbd8ce; border-radius: 8px; background: var(--sky); transition: background-color 450ms ease; }
.arena::before { content: ""; position: absolute; inset: 0 0 auto; height: 5px; background: var(--accent); }
.floor { position: absolute; right: 0; bottom: 0; left: 0; height: 5px; background: #526659; opacity: .45; }
.falling-word { position: absolute; z-index: 1; width: min(18%, 160px); min-height: 44px; padding: 8px 6px; border: 1px solid #b7c9bc; border-radius: 8px; background: #fff; color: #202720; font-size: 15px; font-weight: 700; cursor: pointer; box-shadow: 0 2px 6px #26372a18; overflow-wrap: anywhere; transform: translateX(-50%); }
.falling-word:hover { border-color: var(--accent); background: #f7fbf8; }
.falling-word.correct { border-color: #176b48; background: #d9f2e4; }
.falling-word.wrong { border-color: #b44732; background: #f9dfd9; }
.message { min-height: 44px; display: flex; align-items: center; margin: 9px 0 0; padding: 8px 12px; border: 1px solid transparent; border-radius: 6px; color: #526157; font-size: 15px; font-weight: 700; }
.message.correct { border-color: #9bc9a9; background: #e5f5e9; color: #176b48; }
.message.wrong { border-color: #e0a49a; background: #fff0ed; color: #a2382c; }
.overlay { position: absolute; z-index: 3; inset: 0; display: grid; place-items: center; padding: 20px; background: #f5f8f1eF; text-align: center; }
.panel { max-width: 480px; }
.panel h2 { margin: 0 0 8px; color: #205947; font-size: 28px; }
.panel p { margin: 8px 0 18px; color: #526157; line-height: 1.6; }
.menu-actions { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.count-setting { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin: 16px 0; text-align: left; font-weight: 700; }
.count-setting input { width: 110px; min-height: 42px; padding: 6px 10px; border: 1px solid #b7c9bc; border-radius: 6px; color: #202720; font: inherit; }
button.action { min-height: 44px; padding: 0 20px; border: 0; border-radius: 6px; background: #205947; color: #fff; font: inherit; font-weight: 700; cursor: pointer; }
button.action:hover { background: #174533; }
.menu-notice { min-height: 22px; color: #a2382c !important; font-weight: 700; }
@media (max-width: 560px) {
	.arena { height: 500px; }
	.stat { min-width: auto; }
	.meaning { align-items: flex-start; flex-direction: column; gap: 4px; }
	#meaning { font-size: 18px; }
	.falling-word { width: 18%; padding: 7px 2px; font-size: 12px; }
	.menu-actions { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<main class="game" id="game">
	<div class="topline">
		<div class="stats" aria-live="polite">
			<div class="stat">점수 <strong id="score">0</strong></div>
			<div class="stat">생명 <strong id="lives">3 / 3</strong></div>
			<div class="stat">스테이지 <strong id="stage">1</strong></div>
			<div class="stat">진행 <strong id="progress">0</strong></div>
		</div>
		<button class="music-toggle" id="musicToggle" type="button">♫ 배경음악 끄기</button>
	</div>
	<div class="meaning"><span class="meaning-label">이 뜻에 맞는 영어 단어를 누르세요</span><span id="meaning">게임을 시작해 주세요</span></div>
	<section class="arena" id="arena" aria-label="영단어 낙하 스테이지"><div class="floor"></div></section>
	<p class="message" id="message" aria-live="assertive">게임을 시작하면 영어 단어 5개가 내려옵니다.</p>
</main>
<input id="newFileInput" type="file" accept=".csv,text/csv" hidden>
<script>
let WORDS = __WORD_DATA__;
let wordBook = WORDS;
const palettes = [
	["#eaf4ee", "#205947"], ["#edf2fa", "#345b8c"], ["#fff1e8", "#a65332"],
	["#f4eff8", "#714b83"], ["#fff6d9", "#806318"], ["#e8f4f2", "#286d68"]
];
const arena = document.getElementById("arena");
const meaningEl = document.getElementById("meaning");
const scoreEl = document.getElementById("score");
const livesEl = document.getElementById("lives");
const stageEl = document.getElementById("stage");
const progressEl = document.getElementById("progress");
const messageEl = document.getElementById("message");
const musicToggle = document.getElementById("musicToggle");
let score = 0;
let lives = 3;
let round = 0;
let gameWordCount = 20;
let active = false;
let resolving = false;
let target = null;
let falling = [];
let previousTime = 0;
let audioContext = null;
let musicGain = null;
let musicTimer = null;
let musicStep = 0;
let musicEnabled = true;
let wordBag = [];
let wrongWordMap = new Map();
let gameOverOverlay = null;
let gameMode = "normal";
const newFileInput = document.getElementById("newFileInput");

function prepareAudio() {
	try {
		const Audio = window.AudioContext || window.webkitAudioContext;
		if (!Audio) return;
		audioContext = audioContext || new Audio();
		if (!musicGain) {
			musicGain = audioContext.createGain();
			musicGain.gain.value = 0.22;
			musicGain.connect(audioContext.destination);
		}
		if (audioContext.state === "suspended") audioContext.resume();
	} catch (_) {}
}

function sound(notes, type = "sine") {
	try {
		prepareAudio();
		if (!audioContext) return;
		const start = audioContext.currentTime;
		notes.forEach(([frequency, duration], index) => {
			const oscillator = audioContext.createOscillator();
			const volume = audioContext.createGain();
			const at = start + index * 0.12;
			oscillator.type = type;
			oscillator.frequency.value = frequency;
			volume.gain.setValueAtTime(0.001, at);
			volume.gain.exponentialRampToValueAtTime(0.12, at + 0.02);
			volume.gain.exponentialRampToValueAtTime(0.001, at + duration);
			oscillator.connect(volume);
			volume.connect(audioContext.destination);
			oscillator.start(at);
			oscillator.stop(at + duration + 0.02);
		});
	} catch (_) {}
}

function playMusicTone(frequency, duration, wave, volume) {
	if (!audioContext || !musicGain) return;
	const now = audioContext.currentTime;
	const oscillator = audioContext.createOscillator();
	const envelope = audioContext.createGain();
	oscillator.type = wave;
	oscillator.frequency.setValueAtTime(frequency, now);
	envelope.gain.setValueAtTime(0.001, now);
	envelope.gain.exponentialRampToValueAtTime(volume, now + 0.015);
	envelope.gain.exponentialRampToValueAtTime(0.001, now + duration);
	oscillator.connect(envelope);
	envelope.connect(musicGain);
	oscillator.start(now);
	oscillator.stop(now + duration + 0.02);
}

function playKick() {
	if (!audioContext || !musicGain) return;
	const now = audioContext.currentTime;
	const oscillator = audioContext.createOscillator();
	const envelope = audioContext.createGain();
	oscillator.type = "sine";
	oscillator.frequency.setValueAtTime(145, now);
	oscillator.frequency.exponentialRampToValueAtTime(48, now + 0.14);
	envelope.gain.setValueAtTime(0.18, now);
	envelope.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
	oscillator.connect(envelope);
	envelope.connect(musicGain);
	oscillator.start(now);
	oscillator.stop(now + 0.18);
}

function playMusicBeat() {
	const step = musicStep % 8;
	const roots = [110, 130.81, 98, 146.83];
	const melody = [440, 523.25, 659.25, 783.99, 659.25, 587.33, 523.25, 659.25];
	const root = roots[Math.floor(musicStep / 8) % roots.length];
	playMusicTone(melody[step], 0.15, "sawtooth", 0.12);
	if (step % 2 === 0) {
		playMusicTone(root, 0.19, "triangle", 0.16);
		playKick();
	} else {
		playMusicTone(root * 2, 0.12, "square", 0.035);
	}
	if (step === 4) playMusicTone(190, 0.09, "triangle", 0.08);
	musicStep += 1;
}

function startMusic() {
	if (!musicEnabled || musicTimer) return;
	prepareAudio();
	if (!audioContext || !musicGain) return;
	musicStep = 0;
	playMusicBeat();
	musicTimer = setInterval(playMusicBeat, (60000 / 146) / 2);
}

function stopMusic() {
	if (musicTimer) clearInterval(musicTimer);
	musicTimer = null;
}

function parseCsvRows(text) {
	const rows = [];
	let row = [];
	let field = "";
	let quoted = false;
	for (let index = 0; index < text.length; index += 1) {
		const character = text[index];
		if (quoted) {
			if (character === '"' && text[index + 1] === '"') {
				field += '"';
				index += 1;
			} else if (character === '"') {
				quoted = false;
			} else {
				field += character;
			}
		} else if (character === '"' && field === "") {
			quoted = true;
		} else if (character === ",") {
			row.push(field);
			field = "";
		} else if (character === "\n" || character === "\r") {
			if (character === "\r" && text[index + 1] === "\n") index += 1;
			row.push(field);
			rows.push(row);
			row = [];
			field = "";
		} else {
			field += character;
		}
	}
	if (field.length || row.length) {
		row.push(field);
		rows.push(row);
	}
	return rows;
}

function parseWordFile(text) {
	const words = [];
	const seen = new Set();
	parseCsvRows(text.replace(/^\uFEFF/, "")).forEach((row, index) => {
		const word = (row[0] || "").trim();
		const meanings = row.slice(1).map(meaning => meaning.trim()).filter(Boolean);
		if (!word || !meanings.length) return;
		if (index === 0 && ["word", "english", "영단어", "영어단어", "단어"].includes(word.toLowerCase())) return;
		const key = word.toLocaleLowerCase();
		if (seen.has(key)) return;
		seen.add(key);
		words.push({ word, meanings });
	});
	if (words.length < 5) throw new Error("새 단어장에는 서로 다른 영단어가 5개 이상 필요합니다.");
	return words;
}

function updateMusicButton() {
	musicToggle.textContent = musicEnabled ? "♫ 배경음악 끄기" : "♫ 배경음악 켜기";
}

musicToggle.addEventListener("click", () => {
	musicEnabled = !musicEnabled;
	updateMusicButton();
	if (musicEnabled && active) startMusic();
	else stopMusic();
});

function updateStats() {
	scoreEl.textContent = String(score);
	livesEl.textContent = `${lives} / 3`;
	stageEl.textContent = String(Math.floor(round / 5) + 1);
	progressEl.textContent = `${round} / ${gameWordCount}`;
	const [sky, accent] = palettes[Math.floor(round / 5) % palettes.length];
	arena.style.setProperty("--sky", sky);
	arena.style.setProperty("--accent", accent);
}

function shuffled(items) {
	const result = [...items];
	for (let index = result.length - 1; index > 0; index--) {
		const other = Math.floor(Math.random() * (index + 1));
		[result[index], result[other]] = [result[other], result[index]];
	}
	return result;
}

function nextWord() {
	if (wordBag.length === 0) wordBag = shuffled(WORDS);
	return wordBag.pop();
}

function showOverlay(title, detail, buttonText, callback) {
	const overlay = document.createElement("div");
	overlay.className = "overlay";
	const panel = document.createElement("div");
	panel.className = "panel";
	const heading = document.createElement("h2");
	heading.textContent = title;
	const paragraph = document.createElement("p");
	paragraph.textContent = detail;
	const button = document.createElement("button");
	button.className = "action";
	button.textContent = buttonText;
	button.addEventListener("click", () => { overlay.remove(); callback(); });
	panel.append(heading, paragraph, button);
	overlay.append(panel);
	arena.append(overlay);
}

function endGame(completed = false) {
	active = false;
	stopMusic();
	musicEnabled = false;
	updateMusicButton();
	falling.forEach(item => item.element.remove());
	falling = [];
	meaningEl.textContent = "세 번의 기회를 모두 사용했어요.";
	messageEl.textContent = `최종 점수 ${score}점 · ${round}개 도전`;
	sound([[392, 0.22], [330, 0.24], [262, 0.48]], "triangle");
	showGameOverMenu(completed);
}

function nextRound() {
	if (!active) return;
	round += 1;
	updateStats();
	resolving = false;
	falling.forEach(item => item.element.remove());
	falling = [];
	target = nextWord();
	meaningEl.textContent = target.meanings[Math.floor(Math.random() * target.meanings.length)];
	messageEl.className = "message";
	messageEl.textContent = "내려오는 단어 중 뜻에 맞는 영어 단어를 누르세요.";
	const distractorPool = shuffled(WORDS.filter(item => item.word.toLocaleLowerCase() !== target.word.toLocaleLowerCase()));
	const distractors = [];
	while (distractors.length < 4) {
		distractors.push(distractorPool.length ? distractorPool[distractors.length % distractorPool.length] : target);
	}
	const choices = shuffled([target, ...distractors]);
	const lanes = choices.map((_, index) => 10 + (80 * index / (choices.length - 1)));
	const speed = Math.min(120 + Math.floor((round - 1) / 5) * 22, 350);
	choices.forEach((choice, index) => {
		const button = document.createElement("button");
		button.className = "falling-word";
		button.type = "button";
		button.textContent = choice.word;
		button.style.left = `${lanes[index]}%`;
		button.style.top = `${-48 - (index % 2) * 24}px`;
		button.addEventListener("click", () => answer(choice, button));
		arena.append(button);
		falling.push({ choice, element: button, y: -48 - (index % 2) * 24, speed: speed * (0.92 + Math.random() * 0.16) });
	});
	previousTime = 0;
	requestAnimationFrame(animate);
}

function finishRound(correct, timedOut = false, selectedButton = null) {
	if (resolving || !active) return;
	resolving = true;
	if (correct) {
		score += 10;
		messageEl.className = "message correct";
		messageEl.textContent = `정답! ${target.word} · +10점`;
		sound([[660, 0.12], [880, 0.18]]);
	} else {
		score -= 10;
		lives -= 1;
		wrongWordMap.set(target.word.toLocaleLowerCase(), target);
		messageEl.className = "message wrong";
		messageEl.textContent = `${timedOut ? "시간 초과" : "오답"}! 정답은 ${target.word} · -10점 · 남은 생명 ${lives}개`;
		sound([[220, 0.22]], "square");
	}
	updateStats();
	falling.forEach(item => {
		if (item.element !== selectedButton) item.element.remove();
	});
	falling = selectedButton ? falling.filter(item => item.element === selectedButton) : [];
	if (lives <= 0) {
		setTimeout(endGame, 1200);
	} else if (round >= gameWordCount) {
		setTimeout(() => endGame(true), 1200);
	} else {
		setTimeout(nextRound, 1100);
	}
}

function answer(choice, button) {
	if (!active || resolving) return;
	const correct = choice.word.toLocaleLowerCase() === target.word.toLocaleLowerCase();
	button.classList.add(correct ? "correct" : "wrong");
	finishRound(correct, false, button);
}

function animate(time) {
	if (!active || resolving) return;
	if (previousTime === 0) previousTime = time;
	const elapsed = Math.min((time - previousTime) / 1000, 0.05);
	previousTime = time;
	const floor = arena.clientHeight - 48;
	for (const item of falling) {
		item.y += item.speed * elapsed;
		item.element.style.top = `${item.y}px`;
		if (item.choice === target && item.y >= floor) {
			finishRound(false, true);
			return;
		}
		if (item.choice !== target && item.y >= floor) item.element.hidden = true;
	}
	requestAnimationFrame(animate);
}

function startGame(words = wordBook, mode = "normal", count = 20) {
	WORDS = words;
	gameMode = mode;
	gameWordCount = count;
	prepareAudio();
	score = 0;
	lives = 3;
	round = 0;
	wordBag = [];
	wrongWordMap = new Map();
	active = true;
	musicEnabled = true;
	updateMusicButton();
	updateStats();
	startMusic();
	nextRound();
}

function showGameSetup(words, mode = "normal", title = "게임 설정") {
	if (gameOverOverlay) gameOverOverlay.remove();
	const overlay = document.createElement("div");
	overlay.className = "overlay";
	const panel = document.createElement("div");
	panel.className = "panel";
	const heading = document.createElement("h2");
	heading.textContent = title;
	const detail = document.createElement("p");
	detail.textContent = `게임에 등장할 단어 수를 입력하세요. 단어장 ${words.length}개에서 무작위로 출제합니다.`;
	const countLabel = document.createElement("label");
	countLabel.className = "count-setting";
	countLabel.textContent = "출제 단어 수";
	const countInput = document.createElement("input");
	countInput.type = "number";
	countInput.min = "1";
	countInput.max = "1000";
	countInput.step = "1";
	countInput.value = String(Math.min(20, Math.max(1, words.length)));
	countInput.setAttribute("aria-label", "게임에 등장할 단어 수");
	countLabel.append(countInput);
	const notice = document.createElement("p");
	notice.className = "menu-notice";
	const startButton = document.createElement("button");
	startButton.className = "action";
	startButton.type = "button";
	startButton.textContent = "게임 시작";
	startButton.addEventListener("click", () => {
		const count = Number(countInput.value);
		if (!Number.isInteger(count) || count < 1 || count > 1000) {
			notice.textContent = "1에서 1000 사이의 정수를 입력해 주세요.";
			countInput.focus();
			return;
		}
		overlay.remove();
		gameOverOverlay = null;
		startGame(words, mode, count);
	});
	panel.append(heading, detail, countLabel, notice, startButton);
	overlay.append(panel);
	arena.append(overlay);
	gameOverOverlay = overlay;
}

function showGameOverMenu(completed = false) {
	const overlay = document.createElement("div");
	overlay.className = "overlay";
	const panel = document.createElement("div");
	panel.className = "panel";
	const heading = document.createElement("h2");
	heading.textContent = completed ? "게임 완료" : "Game Over";
	const detail = document.createElement("p");
	detail.textContent = `최종 점수 ${score}점 · ${round} / ${gameWordCount}개 출제 · 틀린 단어 ${wrongWordMap.size}개`;
	const actions = document.createElement("div");
	actions.className = "menu-actions";
	const notice = document.createElement("p");
	notice.className = "menu-notice";
	notice.setAttribute("aria-live", "polite");
	const addAction = (label, callback) => {
		const button = document.createElement("button");
		button.className = "action";
		button.type = "button";
		button.textContent = label;
		button.addEventListener("click", callback);
		actions.append(button);
	};
	addAction("재시작", () => {
		overlay.remove();
		startGame(WORDS, gameMode, gameWordCount);
	});
	addAction("새로운 게임", () => newFileInput.click());
	addAction("틀린 단어 게임", () => {
		if (wrongWordMap.size === 0) {
			notice.textContent = "복습할 틀린 단어가 없습니다.";
			return;
		}
		const missedWords = [...wrongWordMap.values()];
		showGameSetup(missedWords, "wrong", "틀린 단어 게임 설정");
	});
	addAction("종료", () => {
		overlay.remove();
		active = false;
		stopMusic();
		falling.forEach(item => item.element.remove());
		falling = [];
		meaningEl.textContent = "게임이 종료되었습니다.";
		messageEl.className = "message";
		messageEl.textContent = "게임을 종료했습니다. 새 게임은 페이지에서 단어장을 다시 올려 시작하세요.";
	});
	panel.append(heading, detail, actions, notice);
	overlay.append(panel);
	arena.append(overlay);
	gameOverOverlay = overlay;
}

newFileInput.addEventListener("change", async () => {
	const file = newFileInput.files[0];
	if (!file) return;
	try {
		const bytes = await file.arrayBuffer();
		let text;
		try {
			text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
		} catch (_) {
			text = new TextDecoder("euc-kr").decode(bytes);
		}
		const newWords = parseWordFile(text);
		wordBook = newWords;
		showGameSetup(wordBook, "normal", "새 게임 설정");
	} catch (error) {
		const notice = gameOverOverlay && gameOverOverlay.querySelector(".menu-notice");
		if (notice) notice.textContent = error.message || "CSV 파일을 읽지 못했습니다.";
	} finally {
		newFileInput.value = "";
	}
});

showGameSetup(wordBook);
</script>
</body>
</html>'''.replace("__WORD_DATA__", word_data)


st.title("🎯 영단어 맞추기 게임")
st.caption("한글 뜻을 보고 내려오는 영어 단어를 클릭해 보세요.")
sample_csv_path = Path(__file__).resolve().parent.parent / "sample.csv"
st.download_button(
	"샘플 영단어 다운로드",
	sample_csv_path.read_bytes(),
	file_name="sample.csv",
	mime="text/csv",
)

uploaded_file = st.file_uploader("영단어 CSV 업로드", type=["csv"])
if uploaded_file is None:
	st.info("CSV 파일을 업로드하면 게임이 준비됩니다.")
else:
	try:
		word_list = parse_word_csv(uploaded_file.getvalue())
		st.success(f"영단어 {len(word_list)}개를 불러왔습니다.")
		game_data = base64.b64encode(build_game_html(word_list).encode("utf-8")).decode("ascii")
		st.iframe(f"data:text/html;base64,{game_data}", height=820)
	except (UnicodeDecodeError, csv.Error, ValueError) as error:
		st.error(str(error))
