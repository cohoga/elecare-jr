const ML_TO_OZ = 29.57;
const DISP = 0.027; // Displacement (oz/g)
const CAL_G = 4.93; // Powder Caloric Density
const BUFFER_ML = 120; // Hardcoded Safety Buffer

function updateDashboard() {
    const rate = parseFloat(document.getElementById('rate-in').value) || 0;
    const density = parseFloat(document.getElementById('den-in').value);

    // 1. Calculate Required Yield (16h + 120ml)
    const runOz = (rate * 16) / ML_TO_OZ;
    const targetDailyYieldOz = ((rate * 16) + BUFFER_ML) / ML_TO_OZ;
    const pYieldOz = targetDailyYieldOz / 2;

    // 2. Solve for Precise Ingredients (Minimized Waste)
    const pPowderG = (pYieldOz * density) / CAL_G;
    const pWaterOz = pYieldOz - (pPowderG * DISP);
    const pWaterG = pWaterOz * ML_TO_OZ;

    // 3. UI Updates - Header
    setVal('raw-need-oz', runOz.toFixed(1) + " oz");
    setVal('target-yield-oz', targetDailyYieldOz.toFixed(1) + " oz");

    // 4. UI Updates - Portions
    for (let i = 1; i <= 2; i++) {
        setVal(`pw-oz${i}`, pWaterOz.toFixed(2) + " oz");
        setVal(`pw-g${i}`, pWaterG.toFixed(1) + "g Water");
        setVal(`pp${i}`, pPowderG.toFixed(1) + "g");
        setVal(`py${i}`, "Yield: " + pYieldOz.toFixed(1) + " oz");
        
        // Adjust Cylinder Heights (Max capacity 600g for scale)
        const wPct = (pWaterG / 600) * 100;
        const pPct = (pPowderG / 600) * 100;
        const fw = document.getElementById(`fw${i}`);
        const fp = document.getElementById(`fp${i}`);
        if(fw) fw.style.height = wPct + "%";
        if(fp) {
            fp.style.height = pPct + "%";
            fp.style.bottom = wPct + "%";
        }
    }

    // 5. UI Updates - Batch Summary
    setVal('tot-w-g', (pWaterG * 2).toFixed(1) + "g");
    setVal('tot-p-g', (pPowderG * 2).toFixed(1) + "g");
    setVal('tot-y-oz', targetDailyYieldOz.toFixed(1) + " oz");

    // 6. Table Sync
    syncTables(density, rate);
}

function setVal(id, val) {
    const el = document.getElementById(id);
    if(el) el.textContent = val;
}

function syncTables(density, rate) {
    document.querySelectorAll('.p-view').forEach(t => t.classList.add('d-none'));
    const activeTable = document.getElementById('pt-' + density);
    if(activeTable) activeTable.classList.remove('d-none');
    
    document.querySelectorAll('.pump-rate-row').forEach(r => r.classList.remove('highlight-row'));
    const activeRow = document.getElementById('pump-row-' + rate);
    if(activeRow) activeRow.classList.add('highlight-row');
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('rate-in').addEventListener('input', updateDashboard);
    document.getElementById('den-in').addEventListener('change', updateDashboard);
    updateDashboard();
});