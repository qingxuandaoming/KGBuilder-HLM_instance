import subprocess
import os
import sys
import time
import platform

def start_service(command, cwd, name):
    print(f"Starting {name}...")
    try:
        # On Windows, we need shell=True to run batch files (mvn, npm)
        is_windows = platform.system() == "Windows"
        process = subprocess.Popen(command, cwd=cwd, shell=is_windows)
        return process
    except Exception as e:
        print(f"Failed to start {name}: {e}")
        return None

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Paths
    java_dir = os.path.join(root_dir, "backend-java", "kgBuilder-pro")
    python_dir = os.path.join(root_dir, "backend-python")
    frontend_dir = os.path.join(root_dir, "frontend")

    processes = []

    print(f"Root dir: {root_dir}")

    # 1. Start Python Backend
    # Ensure dependencies are installed: pip install -r requirements.txt
    p_py = start_service("python app.py", python_dir, "Python Backend")
    if p_py: processes.append(p_py)

    # 2. Start Java Backend
    # Ensure Maven is installed
    # Note: On first run this might take time to download dependencies
    p_java = start_service("mvn spring-boot:run", java_dir, "Java Backend")
    if p_java: processes.append(p_java)

    # 3. Start Frontend
    # Ensure npm install has been run
    p_front = start_service("npm run serve", frontend_dir, "Frontend")
    if p_front: processes.append(p_front)

    print("All services start commands issued. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        # Note: terminate() might not kill the entire process tree on Windows with shell=True
        # A more robust solution would involve psutil or taskkill
        for p in processes:
            p.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
