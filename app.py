import gradio as gr
import datetime

# 색상 정의
COD_COLORS = ["#E6FF99", "#FFFF66", "#FFCC33", "#FF9933", "#FF6600", "#FF3300"]
TP_COLORS = ["#FFFFFF", "#B3E5FC", "#81D4FA", "#4FC3F7", "#0288D1"]
TN_COLORS = ["#FFFFFF", "#F8BBD0", "#F48FB1", "#F06292", "#EC407A", "#E91E63", "#AD1457"]
PH_COLORS = [
    "#FF0000", "#FF3300", "#FF6600", "#FF9900", "#FFCC00", "#FFFF00", "#CCFF00",
    "#99FF00", "#00FF66", "#00CCFF", "#0066FF", "#0000FF", "#6600FF", "#9900CC"
]

# 등급 계산 함수
def calculate_grade(cod_idx, tp_idx, tn_idx, ph_idx):
    score = 0
    if cod_idx <= 1: score += 1  # 낮을수록 좋음
    if tp_idx <= 1: score += 1
    if tn_idx <= 2: score += 1
    if 6 <= ph_idx <= 8: score += 1  # 중성 부근이 가장 좋음

    if score == 4:
        grade = "✅ 1급수 (매우 깨끗함)"
    elif score == 3:
        grade = "✅ 2급수 (좋음)"
    elif score == 2:
        grade = "⚠️ 3급수 (주의 필요)"
    else:
        grade = "❌ 4급수 (오염됨)"

    return grade

# 저장용
history = []

def analyze(cod, tp, tn, ph):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    grade = calculate_grade(COD_COLORS.index(cod), TP_COLORS.index(tp), TN_COLORS.index(tn), PH_COLORS.index(ph))
    history.append({"date": date, "COD": cod, "T-P": tp, "T-N": tn, "pH": ph, "등급": grade})
    return f"📅 날짜: {date}\n\n💧 수질 등급 결과: {grade}"

def show_history():
    if not history:
        return "📭 저장된 기록이 없습니다."
    text = "📜 입력 기록\n\n"
    for h in reversed(history[-10:]):
        text += f"{h['date']} — COD:{h['COD']} | T-P:{h['T-P']} | T-N:{h['T-N']} | pH:{h['pH']} → {h['등급']}\n"
    return text

with gr.Blocks(title="💧 Water Scan") as app:
    gr.Markdown("## 💧 Water Scan — 수질 측정 시스템\n항목별로 값을 선택하고 결과를 확인하세요.")

    with gr.Row():
        cod = gr.Radio(COD_COLORS, label="COD (화학적 산소 요구량)", interactive=True)
        tp = gr.Radio(TP_COLORS, label="T-P (총인)", interactive=True)
        tn = gr.Radio(TN_COLORS, label="T-N (총질소)", interactive=True)
        ph = gr.Radio(PH_COLORS, label="pH (수소 이온 농도)", interactive=True)

    with gr.Row():
        analyze_btn = gr.Button("🔍 결과 확인하기", variant="primary")
        history_btn = gr.Button("📄 기록 보기")

    result = gr.Textbox(label="결과", lines=3)
    logs = gr.Textbox(label="저장 기록", lines=8)

    analyze_btn.click(fn=analyze, inputs=[cod, tp, tn, ph], outputs=result)
    history_btn.click(fn=show_history, inputs=None, outputs=logs)

app.launch()
