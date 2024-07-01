import os
import re
# Read in netlist
# Parse netlist for reference designators

CONNECTOR_LOOKUP_TABLE = {"A" : "L",
                          "B" : "K",
                          "C" : "J",
                          "D" : "H",
                          "E" : "G",
                          "F" : "F",
                          "G" : "E",
                          "H" : "D",
                          "J" : "C",
                          "K" : "B",
                          "L" : "A"}

EAM_NETLIST_FILE = "dialcnet_EAM.dat"
ABB_NETLIST_FILE = "dialcnet_ABB.dat"

EAM_REFERENCE_DESIGNATOR = "CONN0"
ABB_REFERENCE_DESIGNATOR = "GPU0_0"
OUTPUT_CSV_FILE = EAM_REFERENCE_DESIGNATOR + "_MATING_CHECK.csv"

# Delete previous output files
if os.path.isfile(OUTPUT_CSV_FILE) == True:
    os.remove(OUTPUT_CSV_FILE)

# Create a list of all nets connected to EAM_REFERENCE_DESIGNATOR
EAMConnectivity = {}
EAMNetlistFile = open(EAM_NETLIST_FILE, "r")
FirstLine = True
for line in EAMNetlistFile:
    if FirstLine == True:
        FirstLine = False
        continue
    if line.strip() == "END CONCISE NET LIST":
        continue
    net = line.split()[0]
    reference_designator = line.split()[1]
    pin = line.split()[2]
    if EAM_REFERENCE_DESIGNATOR == reference_designator:
        EAMConnectivity[pin] = net

# Create a list of all nets connected to ABB_REFERENCE_DESIGNATOR
ABBConnectivity = {}
ABBNetlistFile = open(ABB_NETLIST_FILE, "r")
FirstLine = True
for line in ABBNetlistFile:
    if FirstLine == True:
        FirstLine = False
        continue
    if line.strip() == "END CONCISE NET LIST":
        continue
    net = line.split()[0]
    reference_designator = line.split()[1]
    pin = line.split()[2]
    if ABB_REFERENCE_DESIGNATOR == reference_designator:
        ABBConnectivity[pin] = net

# Create output files
OutputCSVFile = open(OUTPUT_CSV_FILE, "w")
OutputCSVFile.write("EAM Pin,EAM Net Name,ABB Pin,ABB Net Name\n")
for pin in EAMConnectivity:
    ABBpin = CONNECTOR_LOOKUP_TABLE[pin[0]] + pin[1:]
    OutputCSVFile.write(pin + "," + EAMConnectivity[pin] + "," + ABBpin + "," + ABBConnectivity[ABBpin] + "\n")
OutputCSVFile.close()

EAMNetlistFile.close()
ABBNetlistFile.close()