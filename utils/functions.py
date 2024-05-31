import os
def acquire_lock(lock_file):
    if os.path.exists(lock_file):
        try:
            with open(lock_file, 'r') as f:
                pid = int(f.read())
                if pid_exists(pid):
                    print(another_instance_running_str)
                    sys.exit(1)
                else:
                    os.remove(lock_file)
        except Exception:
            pass
    with open(lock_file, 'w') as f:
        f.write(str(os.getpid()))

def release_lock(lock_file):
    if os.path.exists(lock_file):
        os.remove(lock_file)

def pid_exists(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False