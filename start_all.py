import subprocess
import os
import sys
import time
import signal
import platform
import urllib.request
import urllib.error

# Try to import stop_all module to clean up ports before starting
try:
    import stop_all
except ImportError:
    stop_all = None

processes = []
log_files = []

def signal_handler(sig, frame):
    print("\n[INFO] Signal received. Shutting down all services...")
    cleanup()
    sys.exit(0)

def cleanup():
    """Terminate all started subprocesses."""
    for p, name in processes:
        if p.poll() is None:  # If process is still running
            print(f"[INFO] Terminating {name}...")
            p.terminate()
            # Give it a moment to terminate gracefully
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"[WARN] {name} did not terminate gracefully, killing...")
                p.kill()
    
    # Close log files
    for f in log_files:
        try:
            f.close()
        except:
            pass
            
    print("[INFO] Cleanup complete.")

def run_java_build(cwd):
    """Builds the Java project synchronously."""
    print("[INFO] Building Java dependencies (skipping tests)...")
    print("[INFO] This might take a while...")
    # Use shell=True on Windows for mvn
    cmd = ["mvn", "install", "-DskipTests", "-pl", "kgBuilder-pro", "-am"]
    try:
        subprocess.run(cmd, cwd=cwd, shell=True, check=True)
        print("[INFO] Java Build Successful.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Java Build failed: {e}")
        return False

def start_service(cmd, cwd, name, log_path, env=None):
    """Starts a service asynchronously and returns the Popen object."""
    print(f"[INFO] Starting {name}...")
    print(f"[INFO] Logging to {log_path}")
    
    try:
        # Open log file
        f = open(log_path, "w", encoding="utf-8")
        log_files.append(f)
        
        use_shell = False
        if platform.system() == "Windows":
            # mvn and npm are usually .cmd files on Windows
            if cmd[0] in ["mvn", "npm"]:
                use_shell = True
            # If we are running node directly, we might not need shell
            if cmd[0] == "node":
                use_shell = False
                
        p = subprocess.Popen(cmd, cwd=cwd, shell=use_shell, env=env, stdout=f, stderr=subprocess.STDOUT)
        processes.append((p, name))
        return p
    except Exception as e:
        print(f"[ERROR] Failed to start {name}: {e}")
        return None

def wait_for_service(url, name, timeout=60):
    """Waits for a service to become available."""
    print(f"[INFO] Waiting for {name} to be ready at {url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    print(f"[INFO] {name} is READY!")
                    return True
        except urllib.error.HTTPError as e:
            # 404 or 401/403 means the server is up and responding
            print(f"[INFO] {name} is READY (responded with {e.code})!")
            return True
        except (urllib.error.URLError, ConnectionResetError):
            pass
        except Exception as e:
            # Ignore other errors during startup
            pass
        
        # Check if process is still alive
        for p, p_name in processes:
            if p_name == name and p.poll() is not None:
                print(f"[ERROR] {name} process died while waiting for startup.")
                return False
                
        time.sleep(2)
        print(".", end="", flush=True)
    
    print(f"\n[ERROR] Timed out waiting for {name}.")
    return False

def main():
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("=== Starting Merged KG Platform ===")
    
    # 1. Clean up old processes
    if stop_all:
        print("[INFO] Cleaning up occupied ports...")
        stop_all.main()
    else:
        print("[WARN] stop_all.py not found, skipping port cleanup.")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create logs directory
    logs_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # 2. Build Java (Synchronous)
    java_cwd = os.path.join(base_dir, "backend-java")
    if not run_java_build(java_cwd):
        print("[ERROR] Aborting due to build failure.")
        return

    # 3. Start Java Backend
    # Run only the pro module
    java_cmd = ["mvn", "spring-boot:run", "-pl", "kgBuilder-pro", "-Dspring-boot.run.main-class=com.warmer.Application"]
    java_log = os.path.join(logs_dir, "java_backend.log")
    start_service(java_cmd, java_cwd, "Java Backend", java_log)

    # 4. Start Python Backend
    python_cwd = os.path.join(base_dir, "backend-python")
    python_cmd = [sys.executable, "app.py"]
    # Ensure Python output is flushed immediately
    py_env = os.environ.copy()
    py_env["PYTHONUNBUFFERED"] = "1"
    python_log = os.path.join(logs_dir, "python_backend.log")
    start_service(python_cmd, python_cwd, "Python Backend", python_log, env=py_env)

    # 5. Start Frontend
    frontend_cwd = os.path.join(base_dir, "frontend")
    
    # Try to find local vue-cli-service for better reliability
    vue_cli_service = os.path.join(frontend_cwd, "node_modules", "@vue", "cli-service", "bin", "vue-cli-service.js")
    
    if os.path.exists(vue_cli_service):
        print(f"[INFO] Using direct vue-cli-service path.")
        front_cmd = ["node", vue_cli_service, "serve"]
    else:
        print("[WARN] vue-cli-service.js not found, falling back to 'npm run serve'")
        front_cmd = ["npm", "run", "serve"]
        
    frontend_log = os.path.join(logs_dir, "frontend.log")
    start_service(front_cmd, frontend_cwd, "Frontend", frontend_log)

    print("\n[INFO] Services started. Waiting for health checks...")
    
    # Check services
    # Note: Java usually takes the longest
    java_ready = wait_for_service("http://localhost:8081", "Java Backend", timeout=120)
    python_ready = wait_for_service("http://localhost:5000", "Python Backend", timeout=30)
    frontend_ready = wait_for_service("http://localhost:8080", "Frontend", timeout=60)

    if java_ready and python_ready and frontend_ready:
        print("\n\n[SUCCESS] All systems operational!")
        print("[INFO] Access the application at: http://localhost:8080")
    else:
        print("\n\n[WARN] Some services failed to become ready. Check logs in 'logs/' directory.")

    # 6. Monitor loop
    try:
        while True:
            time.sleep(1)
            # Check if any process has died unexpectedly
            for p, name in processes:
                ret = p.poll()
                if ret is not None:
                    print(f"\n[WARN] {name} stopped unexpectedly with exit code {ret}.")
                    # Optional: decide whether to kill everything if one fails
                    # cleanup()
                    # sys.exit(1)
                    # For now, just remove it from the list so we don't try to kill it again
                    processes.remove((p, name))
            
            if not processes:
                print("[INFO] All services stopped.")
                break
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
