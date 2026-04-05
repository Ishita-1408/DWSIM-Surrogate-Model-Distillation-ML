import clr
import sys

# Add correct DWSIM paths
sys.path.append(r"C:\Program Files\DWSIM")
sys.path.append(r"C:\Program Files\DWSIM\bin")

# Load automation DLL
clr.AddReference("DWSIM.Automation")
from DWSIM.Automation import Automation3

# Start DWSIM automation
dwsim = Automation3()

# Load your flowsheet
file_path = r"C:\Users\Ishit\OneDrive\Desktop\DWSIM_Surrogate_Project\DWSIM_Flowsheet\dwsim(ben-tol).dwxml"
flowsheet = dwsim.LoadFlowsheet(file_path)

print("DWSIM file loaded successfully!")