from flask import Flask, render_template_string, request
import datetime

app = Flask(__name__)

# 색상 정의
COD_COLORS = ["#E6FF99", "#FFFF66", "#FFCC33", "#FF9933", "#FF6600", "#FF3300"]
TP_COLORS = ["#FFFFFF", "#B3E5FC", "#81D4FA", "#4FC3F7", "#0288D1"]
TN_COLORS = ["#FFFFFF", "#F8BBD0", "#F48FB1", "#F06292", "#EC407A", "#E91E63", "#AD1457"]
PH_COLORS = [
    "#FF0000", "#FF3300", "#FF6600", "#FF9900", "#FFCC00", "#FFFF00", "#CCFF00",
    "#99FF00", "#00FF66", "#00CCFF", "#0066FF", "#0000FF", "#6600FF", "#9900CC"
]

history = []

def calculate_grade(cod_idx, tp_idx, tn_idx, ph_idx):
    score = 0
    if cod_idx <= 1: score += 1
    if tp_idx <= 1: score += 1
    if tn_idx <= 2: score += 1
    if 6 <= ph_idx <= 8: score += 1

    if score == 4:
        return "✅ 1급수 (매우 깨끗함)"
    elif score == 3:
        return "✅ 2급수 (좋음)"
    elif score == 2:
        return "⚠️ 3급수 (주의 필요)"
    else:
        return "❌ 4급수 (오염됨)"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>💧 Water Scan</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f7fcff; text-align: center; padding: 20px; }
        h1 { color: #0288d1; }
        form { background: white; padding: 20px; border-radius: 15px; display: inline-block; }
        select, button { margin: 10px; padding: 5px 10px; }
        .history { background: #e3f2fd; padding: 10px; margin-top: 20px; border-radius: 10px; width: 80%; margin-left:auto; margin-right:auto; text-align:left; }
    </style>
</head>
<body>
    <h1>💧 Water Scan — 수질 측정 시스템</h1>
    <form method="post">
        <label>COD:</label>
        <select name="cod">
            {% for c in cod_colors %}
            <option value="{{ loop.index0 }}">{{ c }}</option>
            {% endfor %}
        </select><br>

        <label>T-P:</label>
        <select name="tp">
            {% for c in tp_colors %}
            <option value="{{ loop.index0 }}">{{ c }}</option>
            {% endfor %}
        </select><br>

        <label>T-N:</label>
        <select name="tn">
            {% for c in tn_colors %}
            <option value="{{ loop.index0 }}">{{ c }}</option>
            {% endfor %}
        </select><br>

        <label>pH:</label>
        <select name="ph">
            {% for i in range(0,14) %}
            <option value="{{ i }}">{{ i }}</option>
            {% endfor %}
        </select><br>

        <button type="submit">🔍 결과 확인</button>
    </form>

    {% if result %}
        <h2>결과: {{ result }}</h2>
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
    return render_template_string(HTML_TEMPLATE, cod_colors=COD_COLORS, tp_colors=TP_COLORS,
                                  tn_colors=TN_COLORS, result=result, history=reversed(history))

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
