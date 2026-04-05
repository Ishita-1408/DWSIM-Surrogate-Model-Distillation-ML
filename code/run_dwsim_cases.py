import clr
import pandas as pd
import os

# ==============================
# STEP 1: Load DWSIM Automation
# ==============================
dwsim_path = r"C:\Program Files\DWSIM"
clr.AddReference(os.path.join(dwsim_path, "DWSIM.Automation.dll"))

from DWSIM.Automation import Automation3

# ==============================
# STEP 2: Load Input Data
# ==============================
inputs = pd.read_csv("../Dataset/lhs_input_cases.csv")

# ==============================
# STEP 3: Initialize DWSIM
# ==============================
sim = Automation3()

flowsheet_path = r"C:\Users\Ishit\OneDrive\Desktop\DWSIM_Surrogate_Project\DWSIM_Flowsheet\dwsim(ben-tol).dwxml"

# ==============================
# STEP 4: Storage
# ==============================
results = []
failed = []

# ==============================
# STEP 5: Loop through cases
# ==============================
for i, row in inputs.iterrows():
    try:
        print(f"Running case {i}")

        # Load flowsheet
        fs = sim.LoadFlowsheet(flowsheet_path)

        # ==============================
        # STEP 6: Set INPUTS
        # ==============================
        feed = fs.GetFlowsheetSimulationObject("Feed").GetAsObject()

        feed.Temperature = float(row["T_feed"])
        feed.Pressure = float(row["P_feed"])

        # ==============================
        # SET COMPOSITION (SAFE)
        # ==============================
        compounds = list(feed.Phases[0].Compounds.keys())

        for comp in compounds:
            if "benzene" in comp.lower():
                feed.Phases[0].Compounds[comp].MoleFraction = float(row["z_benzene"])
            else:
                feed.Phases[0].Compounds[comp].MoleFraction = 1 - float(row["z_benzene"])

        # ==============================
        # STEP 7: Solve flowsheet
        # ==============================
        sim.CalculateFlowsheet2(fs)

        # ==============================
        # STEP 8: Extract outputs
        # ==============================
        distillate = fs.GetFlowsheetSimulationObject("Distillate").GetAsObject()
        bottoms = fs.GetFlowsheetSimulationObject("Bottoms").GetAsObject()

        xD = distillate.GetOverallComposition()[0]
        xB = bottoms.GetOverallComposition()[0]

        column = fs.GetFlowsheetSimulationObject("Column").GetAsObject()

        QC = column.CondenserDuty
        QR = column.ReboilerDuty

        # ==============================
        # SAVE RESULT
        # ==============================
        results.append({
            "T_feed": row["T_feed"],
            "P_feed": row["P_feed"],
            "z_benzene": row["z_benzene"],
            "reflux_ratio": row["reflux_ratio"],
            "stages": row["stages"],
            "feed_stage": row["feed_stage"],
            "bottoms_flow": row["bottoms_flow"],
    
            "xD": xD,
            "xB": xB,
            "QC": QC,
            "QR": QR
        })

        print(f"✅ Case {i} completed")

    except Exception as e:
        import traceback
        print(f"\n❌ Failed case {i}")
        traceback.print_exc()

        failed.append({
            "case": i,
            "error": str(e)
        })

# ==============================
# STEP 9: Save outputs
# ==============================
os.makedirs("../Dataset", exist_ok=True)

pd.DataFrame(results).to_csv("../Dataset/raw_simulation_data.csv", index=False)
pd.DataFrame(failed).to_csv("../Dataset/failed_runs.csv", index=False)

print("✅ Simulation batch completed!")
print(f"✔ Successful runs: {len(results)}")
print(f"❌ Failed runs: {len(failed)}")