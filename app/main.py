from flask import Flask, render_template

app = Flask(__name__)

# Core Constants
ML_TO_OZ = 29.57

def get_pump_payload():
    durations = [8, 12, 16, 20, 24]
    densities = [30, 31, 32, 33]
    rates = list(range(40, 81))
    
    data = {"durations": durations, "data_by_density": {}}
    for d in densities:
        rows = []
        for rate in rates:
            schedules = []
            for hrs in durations:
                oz = (rate * hrs) / ML_TO_OZ
                cal = oz * d
                schedules.append({"hrs": hrs, "oz": round(oz, 1), "cal": int(cal)})
            rows.append({"rate": rate, "schedules": schedules})
        data["data_by_density"][d] = rows
    return data

def get_mixing_rows():
    rows = []
    for w_oz in [x * 0.5 for x in range(50, 71)]:
        w_g = w_oz * ML_TO_OZ
        p_data = {}
        for d in [30, 31, 32, 33]:
            # Powder (g) = (Water Oz * Density) / (4.93 - (Density * 0.027))
            p_g = (d * w_oz) / (4.93 - (d * 0.027))
            yield_oz = w_oz + (p_g * 0.027)
            p_data[d] = {"grams": round(p_g, 1), "yield": round(yield_oz, 1)}
        rows.append({"water_oz": f"{w_oz:.1f}", "water_g": int(w_g), "powders": p_data})
    return rows

@app.route('/')
def index():
    return render_template('index.html', 
                           pump_payload=get_pump_payload(), 
                           mixing_rows=get_mixing_rows())

if __name__ == '__main__':
    # Use port 5005 to avoid MacOS AirPlay conflicts on 5000
    app.run(host='0.0.0.0', port=5005, debug=True)