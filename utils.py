import os


def has_server():
    import psutil
    pid = server_pid()
    if pid is not None:
        try:
            p = psutil.Process(int(pid))
            if "python" in p.name() and p.status() != psutil.STATUS_ZOMBIE:
                return pid
            else:
                return False
        except psutil.NoSuchProcess as e:
            return False


def server_pid():
    pid_file_path = os.path.join(os.path.dirname(__file__), "server",
                                 "server.pid")
    if not os.path.exists(pid_file_path):
        return None
    with open(pid_file_path, "r") as f:
        pid = f.read()
        if len(pid) == 0:
            return None
        return int(pid)