import subprocess
import os
import sys
import time
import threading

def run_java_backend():
    print("[INFO] Starting Java Backend...")
    # Assumes Maven is installed. Alternatively, run the built JAR.
    # Adjust path if necessary.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cwd = os.path.join(base_dir, "backend-java")
    # Using 'mvn clean spring-boot:run' for kgBuilder-pro which is the web module
    # We need to target the kgBuilder-pro module
    cmd = ["mvn", "clean", "spring-boot:run", "-pl", "kgBuilder-pro", "-am"]
    
    # On Windows, shell=True might be needed for mvn
    try:
        subprocess.run(cmd, cwd=cwd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Java Backend failed: {e}")

def run_python_backend():
    print("[INFO] Starting Python Backend...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cwd = os.path.join(base_dir, "backend-python")
    cmd = [sys.executable, "app.py"]
    try:
        subprocess.run(cmd, cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Python Backend failed: {e}")

def run_frontend():
    print("[INFO] Starting Frontend...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cwd = os.path.join(base_dir, "frontend")
    # Assumes npm is installed
    cmd = ["npm", "run", "serve"]
    try:
        subprocess.run(cmd, cwd=cwd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Frontend failed: {e}")

def main():
    print("=== Starting Merged KG Platform ===")
    
    threads = []
    
    t_java = threading.Thread(target=run_java_backend)
    t_java.start()
    threads.append(t_java)
    
    t_python = threading.Thread(target=run_python_backend)
    t_python.start()
    threads.append(t_python)
    
    t_front = threading.Thread(target=run_frontend)
    t_front.start()
    threads.append(t_front)
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
