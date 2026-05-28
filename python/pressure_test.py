from pymodbus.client import ModbusTcpClient
import pymodbus
import sys

# --- CONFIGURATION ---
IP_ADDRESS = '192.168.0.10'
PORT = 5020
SLAVE_ID = 1 
ADDR_ACTUAL = 25 
ADDR_TARGET = 26 

def run_pressure_test():
    # Print version info for debugging
    print(f"DEBUG: Pymodbus Version: {pymodbus.__version__}")
    
    client = ModbusTcpClient(IP_ADDRESS, port=PORT)
    
    if not client.connect():
        print(f"? Connection Failed to {IP_ADDRESS}:{PORT}")
        return

    print(f"? Connected to {IP_ADDRESS}:{PORT}")
    print("-" * 60)

    try:
        while True:
            # TRY READ: We will try the three most common ways to call this
            result = None
            try:
                # Attempt 1: Modern 3.x style
                result = client.read_holding_registers(ADDR_ACTUAL, count=2, slave=SLAVE_ID)
            except TypeError:
                try:
                    # Attempt 2: Legacy 2.x style
                    result = client.read_holding_registers(ADDR_ACTUAL, count=2, unit=SLAVE_ID)
                except TypeError:
                    # Attempt 3: No slave ID (some TCP bridges ignore it)
                    result = client.read_holding_registers(ADDR_ACTUAL, count=2)

            if result and not result.isError():
                actual_val = result.registers[0]
                target_val = result.registers[1]
                sys.stdout.write(f"\rLIVE | Actual: {actual_val} mBar | Target: {target_val} mBar | Set New: ")
                sys.stdout.flush()
            else:
                print(f"\n?? Modbus Error: {result}")

            user_input = input().lower()
            if user_input == 'q': break
            elif user_input in ['r', '']: continue
            else:
                try:
                    new_p = int(user_input)
                    # TRY WRITE: Same logic as read
                    try:
                        client.write_register(ADDR_TARGET, new_p, slave=SLAVE_ID)
                    except TypeError:
                        try:
                            client.write_register(ADDR_TARGET, new_p, unit=SLAVE_ID)
                        except TypeError:
                            client.write_register(ADDR_TARGET, new_p)
                    print(f"?? Target Sent: {new_p}")
                except ValueError:
                    print("Invalid Number")

    except Exception as e:
        print(f"\nInternal Script Error: {e}")
    finally:
        client.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    run_pressure_test()
