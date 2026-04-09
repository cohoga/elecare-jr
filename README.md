### EleCare Jr. Precision Prep Dashboard

A specialized web utility designed to calculate precise infant formula mixing ratios for enterally-fed children. This application implements a **Minimized Waste** strategy, prioritizing an exact 120ml safety buffer over a 16-hour feeding cycle rather than rounding water volumes to the nearest half-ounce.

---

### 🚀 Core Features

* **Precision Displacement Logic:** Accounts for the volumetric displacement of EleCare Jr. powder ($0.025198 \text{ oz/g}$) to ensure final yield accuracy.
* **Zero-Waste Target:** Calculates the absolute minimum grams of formula needed to satisfy a 16-hour run plus a 100ml buffer.
* **Dual-Portion Splitter:** Automatically divides the daily requirement into two equal preparation containers.
* **Dynamic Reference Tables:** Synchronized lookup tables for pump schedules (40–80 ml/hr) and formula density (30–33 cal/oz).
* **Visual Feedback:** Real-time "liquid" cylinders represent the ratio of water to powder in each portion.

---

### 🛠 Tech Stack

* **Backend:** Python 3.11 / Flask
* **Frontend:** JavaScript (ES6+), Bootstrap 5, CSS3
* **Deployment:** Docker & Docker Compose

---

### 📂 Project Structure

```text
/my-project
│   Dockerfile              # Container definition
│   docker-compose.yml      # Orchestration and volume mapping
│   requirements.txt        # Python dependencies
└───app/
    │   main.py             # Flask Server & Data Engine
    ├───static/
    │   ├───css/style.css   # Custom Dashboard Styling
    │   └───js/calculator.js # Precision Logic & UI Sync
    └───templates/
        └───index.html      # Dashboard Structure
```

---

### ⚡ Installation & Setup

#### Prerequisites
* Docker and Docker Compose installed on your machine.

#### Running the Application
1.  **Clone the repository** to your local machine.
2.  **Navigate to the root directory** where the `docker-compose.yml` is located.
3.  **Start the container:**
    ```bash
    docker-compose up --build
    ```
4.  **Access the Dashboard:**
    Open your browser to `http://localhost:5005`.

---

### 🧪 Engineering Logic

The dashboard operates on the **Minimized Formula** principle. Instead of starting with a water volume (e.g., 14.5 oz) and finding the yield, it starts with the **Target Yield** and solves backward for the ingredients.

**The Math:**
1.  **Target Yield:** $((\text{Rate} \times 16) + 100\text{ml}) \div 29.57353 = \text{Total Oz}$
2.  **Powder ($P$):** $(\text{Portion Yield} \times \text{Density}) \div 4.92788 \text{ cal/g}$
3.  **Water ($W$):** $\text{Portion Yield} - (P \times 0.025198 \text{ displacement})$

This ensures that every gram of EleCare Jr. is utilized effectively, providing the exact caloric density required without over-preparing.

---

### ⚠️ Troubleshooting

* **ERR_EMPTY_RESPONSE:** Ensure `main.py` is set to `host='0.0.0.0'` to allow Docker to communicate with your browser.
* **File Not Found:** If Docker cannot find `main.py`, verify that the `CMD` in your `Dockerfile` points to the correct subfolder (`app/main.py`).
* **Port Conflict:** If port 5005 is in use, modify the port mapping in `docker-compose.yml` (e.g., `"5010:5005"`).