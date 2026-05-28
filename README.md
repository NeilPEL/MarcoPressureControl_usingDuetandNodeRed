# Marco Pressure Control via Duet3D & Node-RED

Integration of an industrial Marco Systems Pressure Controller with a Duet3D 6HC ecosystem. This project uses a Raspberry Pi (SBC mode) as an intelligence bridge to translate between Duet Global Variables and Modbus TCP.

## 🚀 The Successful Stack
* **Motion Control:** Duet3D 6HC (RepRapFirmware).
* **Logic Engine:** Raspberry Pi 4/5 running Node-RED.
* **Hardware Interface:** Modbus TCP (Marco HMI).
* **UI:** Duet Web Control (DWC) with `BtnCmd` plugin.

---

## 🛠️ Key Project Elements

### 1. Networking (The Dual-IP Bridge)
Industrial controllers often exist on private subnets. To maintain a connection to both the Controller and the Lab network, we implemented a multi-homed static IP setup on the Pi.

**The Solution:** Assigning two IP addresses to the same physical Ethernet interface:
* `192.168.50.X`: Primary Lab Network (SSH/DWC access).
* `192.168.0.250`: Private Marco Network (Modbus access).

### 2. Python Validation
Before full automation, we used a custom Python script to verify the Modbus mapping. 
* **Note:** Marco uses 1-based indexing (e.g., Register 26), while `pymodbus` and Node-RED use 0-based indexing (Address 25).

### 3. Node-RED Logic & Sanitization
The Node-RED flow handles bidirectional data.
* **Sanitization:** Filters out `65535` (0xFFFF) error states caused by network drops or sensor initialization.
* **Optimization:** Uses an **RBE (Report-By-Exception)** node to ensure Modbus writes only occur when the Duet global variable actually changes, preventing network flooding.
* **Diagnostics:** Includes a live Ping-Test to monitor HMI latency.

### 4. UI Integration (BtnCmd "Remote Source")
Standard Duet charts are restricted to temperature sensors. To display pressure:
1.  Install the **BtnCmd** plugin for DWC.
2.  Add a **"Remote Source"** widget (this is an Iframe).
3.  Point the source to your Node-RED UI (`http://<pi-ip>:1880/ui`).
4.  This allows the Node-RED gauges and history charts to appear natively inside the Duet interface.

---

## 📂 Source Code
* **Node-RED Flow:** See `nodered/ModBus_MarcoPressureControl.json` for the full dashboard and Modbus logic.
* **Python Test:** See `/python/pressure_test.py` for hardware debugging.
* **Networking:** See `/scripts/network_setup.sh` for the IP bridging command.
