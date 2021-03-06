from pyghmi.ipmi import command
from model.ServerConnection import ServerConnection
import time
import thread
import threading


class Poller (threading.Thread):
    def __init__(self, host_list, interval):
        threading.Thread.__init__(self)
        self.interval = interval  # Polling interval in seconds
        self.server_connection_list = []
        self.failed_connection_list = []
        self.stopped = False
        for host in host_list:
            try:
                ipmi = command.Command(bmc=host.hostname, userid=host.userid, password=host.password)
                server_connection = ServerConnection(ipmi, host.unique_id)
                self.server_connection_list.append(server_connection)
                print (host.hostname + " - ipmi connection established")
            except:
                self.failed_connection_list.append(host.unique_id)
                print (host.hostname + " - ipmi connection failed")

    def run(self):
        self.poll_servers()

    def poll_servers(self):
        while not self.stopped:
            t_start = time.time()
            for server_connection in self.server_connection_list:
                server_connection.start()
                print (str(t_start) + ": scan @ " + server_connection.unique_id +
                       " (" + server_connection.ipmi.bmc + ")")
                if self.stopped:
                    break
            t_end = time.time()
            t_delta = t_end - t_start
            # Wait until end of polling interval (unless polling took longer than interval)
            if t_delta < self.interval:
                for i in range(int(self.interval - t_delta)):
                    time.sleep(1)
                    if self.stopped:
                        break

    def kill(self):
        self.stopped = True
