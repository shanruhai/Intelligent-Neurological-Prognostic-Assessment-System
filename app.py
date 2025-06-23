import os
import random
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__, template_folder='templates', static_folder='static')

# 数据存储文件
DATA_FILE = "model_data.json"

# 初始化数据文件
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('skin_model.html')

@app.route('/skin_model')
def skin_model_page():
    return render_template('skin_model.html')

@app.route('/lymph_predict')
def lymph_predict_page():
    return render_template('lymph_predict.html')

@app.route('/fluid_model')
def fluid_model_page():
    return render_template('fluid_model.html')

@app.route('/skin_model', methods=['POST'])
def skin_model():
    try:
        params = request.get_json()
        result = {
            "status": "normal" if random.random() < 0.8 else "abnormal",
            "epidermis": random.uniform(50, 200),
            "dermis": random.uniform(100, 300),
            "subcutaneous": random.uniform(200, 400)
        }
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data.append({
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "module": "skin_model",
            "params": params,
            "result": result
        })
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return jsonify(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@app.route('/lymph_predict', methods=['POST'])
def lymph_predict():
    try:
        params = request.get_json()
        diffusion_rate = float(params['diffusionRate'])
        initial_concentration = float(params['initialConcentration'])
        time_step = float(params['timeStep'])
        # 生成3D路径，约束在管网范围内
        path = []
        x, y, z = 0, 0, 0
        for _ in range(20):
            x += random.uniform(-diffusion_rate, diffusion_rate) * 0.5  # 缩小范围以适应管网
            y += random.uniform(-diffusion_rate, diffusion_rate) * 0.5
            z += random.uniform(-diffusion_rate, diffusion_rate) * 0.5
            path.append({"x": x, "y": y, "z": z})
        result = {
            "risk": "high" if random.random() < 0.3 else "low",
            "probability": random.uniform(0.1, 0.9),
            "path": path
        }
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data.append({
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "module": "lymph_predict",
            "params": params,
            "result": result
        })
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return jsonify(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@app.route('/fluid_model', methods=['POST'])
def fluid_model():
    try:
        params = request.get_json()
        blood_speed = float(params['bloodSpeed'])
        vessel_diameter = float(params['vesselDiameter'])
        infection_severity = float(params['infectionSeverity'])
        # 模拟血栓和缺血风险
        thrombosis_risk = min(100, (infection_severity * 10) * (50 / vessel_diameter) * (1 / blood_speed))
        ischemic_risk = min(100, (infection_severity * 8) * (50 / vessel_diameter) * (1 / blood_speed))
        # 血管亲水开放性
        vessel_openness = max(0, 100 - (infection_severity * 5 + (50 / vessel_diameter) * 10))
        # 流体湍流程度（0-1）
        turbulence = min(1, infection_severity / 10 + (50 / vessel_diameter) / 50)
        result = {
            "status": "abnormal" if thrombosis_risk > 50 or ischemic_risk > 50 else "normal",
            "thrombosisRisk": thrombosis_risk,
            "ischemicRisk": ischemic_risk,
            "vesselOpenness": vessel_openness,
            "bloodSpeed": blood_speed,
            "vesselDiameter": vessel_diameter,
            "turbulence": turbulence
        }
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data.append({
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "module": "blood_flow",
            "params": params,
            "result": result
        })
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return jsonify(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
