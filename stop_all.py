import os
import subprocess
import platform

def kill_process_by_port(port):
    """Kills the process listening on the specified port."""
    print(f"[INFO] Checking port {port}...")
    try:
        if platform.system() == "Windows":
            # Find PID
            cmd_find = f"netstat -ano | findstr :{port}"
            result = subprocess.run(cmd_find, shell=True, capture_output=True, text=True)
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    parts = line.split()
                    # Check if it's actually listening or established on that port
                    # parts[1] is Local Address
                    if f":{port}" in parts[1]:
                        pid = parts[-1]
                        print(f"[INFO] Killing PID {pid} on port {port}...")
                        subprocess.run(f"taskkill /F /PID {pid}", shell=True)
            else:
                print(f"[INFO] No process found on port {port}.")
        else:
            # Linux/Mac (lsof or netstat)
            # Simplified for now, assuming Windows environment based on context
            pass
    except Exception as e:
        print(f"[ERROR] Failed to kill process on port {port}: {e}")

def main():
    print("=== Stopping Unified Platform Services ===")
    ports = [8081, 5000, 8082] # Updated ports: Java(8081), Python(5000), Frontend(8082)
    for port in ports:
        kill_process_by_port(port)
    print("=== All Services Stopped ===")

if __name__ == "__main__":
    main()
