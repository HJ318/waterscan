from flask import Flask, render_template_string, request
import datetime
import os

app = Flask(__name__)

# 색상 정의
COD_COLORS = ["#E6FF99", "#FFFF66", "#FFCC33", "#FF9933", "#FF6600", "#FF3300"]
TP_COLORS = ["#F3F5FF", "#B3E5FC", "#81D4FA", "#4FC3F7", "#0288D1"]
TN_COLORS = ["#FFF3F3", "#F8BBD0", "#F48FB1", "#F06292", "#EC407A", "#E91E63", "#AD1457"]
PH_COLORS = [
    "#FF0000", "#FF3300", "#FF6600", "#FF9900", "#FFCC00", "#FFFF00", "#CCFF00",
    "#99FF00", "#00FF66", "#00CCFF", "#0066FF", "#0000FF", "#6600FF", "#9900CC"
]

# 기록 저장 리스트
history = []

# 등급 계산 함수
def calculate_grade(cod_idx, tp_idx, tn_idx, ph_idx):
    score = 0
    if cod_idx <= 1:
        score += 1
    if tp_idx <= 1:
        score += 1
    if tn_idx <= 2:
        score += 1
    if 6 <= ph_idx <= 8:
        score += 1

    if score == 4:
        return "✅ 1급수 (매우 깨끗함)"
    elif score == 3:
        return "✅ 2급수 (좋음)"
    elif score == 2:
        return "⚠️ 3급수 (주의 필요)"
    else:
        return "❌ 4급수 (오염됨)"

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>💧 Water Scan</title>
    <style>
        body {
            font-family: "Pretendard", Arial, sans-serif;
            background: linear-gradient(to bottom, #e0f7fa, #ffffff);
            text-align: center;
            padding: 30px;
        }
        h1 {
            color: #0288d1;
            font-size: 2.2em;
            margin-bottom: 20px;
        }
        form {
            background: white;
            padding: 25px 40px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            display: inline-block;
            text-align: center;
        }
        .section {
            margin-bottom: 20px;
        }
        .color-option {
            display: inline-block;
            width: 30px;
            height: 30px;
            border-radius: 6px;
            margin: 4px;
            cursor: pointer;
            border: 2px solid transparent;
        }
        input[type="radio"] {
            display: none;
        }
        input[type="radio"]:checked + label .color-option {
            border: 2px solid #0288d1;
            box-shadow: 0 0 5px #0288d1;
        }
        button {
            background: #0288d1;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background: #0277bd;
        }
        .result {
            margin-top: 25px;
            font-size: 1.3em;
            font-weight: bold;
        }
        .history {
            background: #f1f8e9;
            padding: 15px;
            margin-top: 30px;
            border-radius: 12px;
            width: 80%;
            margin-left: auto;
            margin-right: auto;
            text-align: left;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .history h3 {
            margin-top: 0;
            color: #388e3c;
        }
    </style>
</head>
<body>
    <h1>💧 Water Scan — 수질 측정 시스템</h1>

    <form method="post">
        <div class="section">
            <h3>COD (화학적 산소 요구량)</h3>
            {% for c in cod_colors %}
                <input type="radio" id="cod{{loop.index0}}" name="cod" value="{{loop.index0}}" required>
                <label for="cod{{loop.index0}}">
                    <div class="color-option" style="background: {{c}};"></div>
                </label>
            {% endfor %}
        </div>

        <div class="section">
            <h3>T-P (총인)</h3>
            {% for c in tp_colors %}
                <input type="radio" id="tp{{loop.index0}}" name="tp" value="{{loop.index0}}" required>
                <label for="tp{{loop.index0}}">
                    <div class="color-option" style="background: {{c}};"></div>
                </label>
            {% endfor %}
        </div>

        <div class="section">
            <h3>T-N (총질소)</h3>
            {% for c in tn_colors %}
                <input type="radio" id="tn{{loop.index0}}" name="tn" value="{{loop.index0}}" required>
                <label for="tn{{loop.index0}}">
                    <div class="color-option" style="background: {{c}};"></div>
                </label>
            {% endfor %}
        </div>

        <div class="section">
            <h3>pH (수소 이온 농도)</h3>
            {% for i in range(1,14) %}
                <input type="radio" id="ph{{i}}" name="ph" value="{{i}}" required>
                <label for="ph{{i}}">
                    <div class="color-option" style="background:hsl({{i * 25}}, 80%, 60%);"></div>
                </label>
            {% endfor %}
        </div>

        <button type="submit">🔍 결과 확인</button>
    </form>

    {% if result %}
        <div class="result">💧 결과: {{ result }}</div>
    {% endif %}

    <div class="history">
        <h3>📜 최근 기록</h3>
        {% if history %}
            {% for h in history %}
                <div>📅 {{ h.date }} — COD:{{ h.cod }} | T-P:{{ h.tp }} | T-N:{{ h.tn }} | pH:{{ h.ph }} → {{ h.grade }}</div>
            {% endfor %}
        {% else %}
            <p>📭 기록이 없습니다.</p>
        {% endif %}
    </div>
</body>
</html>
"""


# 라우트 설정
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        cod = int(request.form["cod"])
        tp = int(request.form["tp"])
        tn = int(request.form["tn"])
        ph = int(request.form["ph"])
        result = calculate_grade(cod, tp, tn, ph)
        history.append({
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cod": cod, "tp": tp, "tn": tn, "ph": ph, "grade": result
        })
    return render_template_string(
        HTML_TEMPLATE,
        cod_colors=COD_COLORS,
        tp_colors=TP_COLORS,
        tn_colors=TN_COLORS,
        result=result,
        history=reversed(history)
    )

# Render 배포용
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
