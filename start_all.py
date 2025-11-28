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
    # First, build dependencies to avoid reactor issues with spring-boot:run
    print("[INFO] Building Java dependencies (skipping tests)...")
    build_cmd = ["mvn", "install", "-DskipTests", "-pl", "kgBuilder-pro", "-am"]
    try:
        subprocess.run(build_cmd, cwd=cwd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Java Build failed: {e}")
        return

    print("[INFO] Running Java Backend...")
    # Run only the pro module without -am to avoid running goal on parent
    cmd = ["mvn", "spring-boot:run", "-pl", "kgBuilder-pro", "-Dspring-boot.run.main-class=com.warmer.Application"]
    
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
    
    # Robust command for Windows with special chars in path
    # We directly call vue-cli-service.js using node
    # Use quotes for path in case of spaces, but subprocess list args handle this better
    vue_cli_service = os.path.join(cwd, "node_modules", "@vue", "cli-service", "bin", "vue-cli-service.js")
    
    use_shell = False
    if os.path.exists(vue_cli_service):
        print(f"[INFO] Using direct vue-cli-service path: {vue_cli_service}")
        cmd = ["node", vue_cli_service, "serve"]
        use_shell = False
    else:
        print("[WARN] vue-cli-service.js not found, falling back to 'npm run serve'")
        cmd = ["npm", "run", "serve"]
        use_shell = True

    try:
        # shell=False is safer for paths with special characters like '&' when calling executables directly
        subprocess.run(cmd, cwd=cwd, shell=use_shell, check=True)
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
