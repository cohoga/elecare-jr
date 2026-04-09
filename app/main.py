from flask import Flask, render_template

app = Flask(__name__)

# Core Constants
ML_TO_OZ = 29.57353

def get_pump_payload():
    durations = [14, 15, 16, 17, 18]
    densities = [30, 31, 32, 33]
    rates = list(range(55, 81))
    
    data = {"durations": durations, "data_by_density": {}}
    for d in densities:
        rows = []
        for rate in rates:
            schedules = []
            for hrs in durations:
                oz = (rate * hrs) / ML_TO_OZ
                cal = oz * d
                schedules.append({"hrs": hrs, "oz": round(oz, 2), "cal": int(cal)})
            rows.append({"rate": rate, "schedules": schedules})
        data["data_by_density"][d] = rows
    return data

def get_mixing_rows():
    rows = []
    for w_oz in [x * 0.5 for x in range(50, 71)]:
        w_g = w_oz * ML_TO_OZ
        p_data = {}
        for d in [30, 31, 32, 33]:
            # Powder (g) = (Water Oz * Density) / (4.92788 - (Density * 0.025198))
            p_g = (d * w_oz) / (4.92788 - (d * 0.025198))
            yield_oz = w_oz + (p_g * 0.025198)  # Total yield in oz
            p_data[d] = {"grams": round(p_g, 2), "yield": round(yield_oz, 2)}
        rows.append({"water_oz": f"{w_oz:.1f}", "water_g": round(w_g, 2), "powders": p_data})
    return rows

@app.route('/')
def index():
    return render_template('index.html', 
                           pump_payload=get_pump_payload(), 
                           mixing_rows=get_mixing_rows())

if __name__ == '__main__':
    # Use port 5005 to avoid MacOS AirPlay conflicts on 5000
    app.run(host='0.0.0.0', port=5005)