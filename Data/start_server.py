import subprocess
import sys
import _Host_Snake_client
import time
import socket


# Programe qui lance le server et le client du server
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def main(username='Host', color='blue'):
    IP = get_ip()
    # username='Host'
    # color='blue'
    communication_server = subprocess.Popen([sys.executable, "server.py"])
    Game_server = subprocess.Popen([sys.executable, "_Snake_server.py"])
    time.sleep(2)
    _Host_Snake_client.main(IP, username, color)
    communication_server.kill()
    Game_server.kill()

# main()
