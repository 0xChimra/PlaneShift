import stem
from stem.control import Controller
from stem import Signal
import stem.process
import sys
import os
import random
import string
import subprocess
import time
import requests
from threading import Thread

class TORic(object):
    def __init__(self, socks_port="", control_port="", verbose=True, password="", allow_admin=False, tor_path=None):
        try:

            if sys.platform == "linux" or sys.platform == "linux2":
                self.os_type = "linux"
            elif sys.platform == "win32":
                self.os_type = "windows"


            if allow_admin == False:
                if not self.os_type == "windows":
                    if int(os.getuid()) == 0:
                        if verbose == True:
                            print("Do Not Launch a Tor Handler as a superuser or root")
                        sys.exit(1)

            

            if self.os_type == "windows":
                if tor_path == None:
                    if verbose == True:
                        print("Defaulting to TORic Windows binary")
                    work_dir = os.getcwd()
                    tor_binary = work_dir + "\\WindowsTor\\Tor\\tor.exe"
                    self.tor_path = str(tor_binary)
                else:
                    self.tor_path = str(tor_path)

            if socks_port == "":
                if verbose == True:
                    print("No Socks Port Selected")
                sys.exit(1)
            else:
                socks_port = int(socks_port)
            
            if control_port == "":
                if verbose == True:
                    print("Calculating a Control Port ( socks_port + 1)")
                control_port = int(socks_port) + 1

            else:
                control_port = int(control_port)
            
            if socks_port == control_port:
                if verbose == True:
                    print("The Socks Port and the Control Port are on the same Port")
                sys.exit(1)

            if password == "":
                self.password = self.gen_torpassword()
                self.hashed_password = self.hash_passwd()
            else:
                self.password = str(password)
                self.hashed_password = self.hash_passwd()
        except Exception as ex:
            if verbose == True:
                print("Error in TORic Configuration : ", ex)
            sys.exit(1)

        self.version = "TORic Construct v0.6"
        self.verbose = verbose
        self.socks_port = int(socks_port)
        self.control_port = int(control_port)      

    def gen_torpassword(self):
        #vars
        length = 20
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation
        combo = lower + upper + num + symbols
        #generation
        x = random.sample(combo, length)
        allocated_pass = "".join(x)
        return str(allocated_pass)

    def hash_passwd(self):
        if self.os_type == "linux":
            x = subprocess.check_output(['tor', "--quiet", '--hash-password', self.password])
            y = str(x.decode("utf-8"))
            return y
        elif self.os_type == "windows":
            x = subprocess.check_output([self.tor_path, "--quiet", '--hash-password', self.password])
            y = str(x.decode("utf-8"))
            return y


    def constuct_controller(self):
        try:
            controller = Controller.from_port(port=self.control_port)
            controller.authenticate(password=self.password)
            self.controller = controller
        except Exception as ex:
            if self.verbose == True:
                print("Error in controller construction : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
    
    def deconstruct_controller(self):
        try:
            self.controller.close()
        except Exception as ex:
            if self.verbose == True:
                print("Error in controller deconstruction : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
    
    def construct_torprocess(self, torrc=False, torrc_path=None, daemon=False):

        def bootstrapped(line):
            if "Bootstrapped" in line:
                print(line)

        try:
            if daemon == False:
                daemon = str(0)
            elif daemon == True:
                daemon = str(1)
            else:
                if self.verbose == True:
                    print("Unknow input in the parameter 'daemon'")
                sys.exit(1)

            if torrc == True:
                if torrc_path == None:
                    with open("torrc", "w") as f:
                        f.write("SOCKSPort " + str(self.socks_port) + "\nControlPort " + str(self.control_port) + "\nRunAsDaemon " + daemon + "\nHashedControlPassword " + self.hashed_password)
                else:
                    if not torrc_path[-1] == "/":
                        torrc_path = torrc_path + "/"
                    path_to_torrc = str(torrc_path + "torrc")
                    with open(path_to_torrc, "w") as f:
                        f.write("SOCKSPort " + str(self.socks_port) + "\nControlPort " + str(self.control_port) + "\nRunAsDaemon " + daemon + "\nHashedControlPassword " + self.hashed_password)
                
                if not torrc_path == None:
                    if not torrc_path[-1] == "/":
                        torrc_path = str(torrc_path + "/")
                    path_to_torrc = str(torrc_path + "torrc")
                else:
                    path_to_torrc = str("torrc")

                if self.os_type == "linux":
                    if self.verbose == True:
                        self.tor_process = stem.process.launch_tor(torrc_path=path_to_torrc, init_msg_handler = bootstrapped)
                    else:
                        self.tor_process = stem.process.launch_tor(torrc_path=path_to_torrc)
                elif self.os_type == "windows":
                    if self.verbose == True:
                        self.tor_process = stem.process.launch_tor(tor_cmd=self.tor_path, torrc_path=path_to_torrc, init_msg_handler = bootstrapped)
                    else:
                        self.tor_process = stem.process.launch_tor(tor_cmd=self.tor_path, torrc_path=path_to_torrc)
                    
            elif torrc == False:
                torrc_config = {"SOCKSPort": str(self.socks_port), "ControlPort": str(self.control_port), "RunAsDaemon": daemon, "HashedControlPassword": self.hashed_password}
                if self.os_type == "linux":
                    if self.verbose == True:
                        self.tor_process = stem.process.launch_tor_with_config(config = torrc_config, init_msg_handler = bootstrapped)
                    else:
                        self.tor_process = stem.process.launch_tor_with_config(config = torrc_config)
                if self.os_type == "windows":
                    if self.verbose == True:
                        self.tor_process = stem.process.launch_tor_with_config(tor_cmd=self.tor_path, config = torrc_config, init_msg_handler = bootstrapped)
                    else:
                        self.tor_process = stem.process.launch_tor_with_config(tor_cmd=self.tor_path, config = torrc_config)
        except Exception as ex:
            if self.verbose == True:
                print("Error in tor process construction : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
    
    def deconstruct_torprocess(self):
        try:
            self.tor_process.kill()
        except Exception as ex:
            if self.verbose == True:
                print("Error in tor process deconstruction : ", ex)
            sys.exit(1)


    def set_exitnodes(self, exitnodes=None):
        try:
            self.controller.set_options({"ExitNodes": exitnodes})
        except Exception as ex:
            if self.verbose == True:
                print("Error in setting the exit nodes : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)

    def get_ip(self, website="https://ipinfo.io/ip"):
        try:
            http = "socks5h://localhost:" + str(self.socks_port)
            https = "socks5h://localhost:" + str(self.socks_port)

            proxies = {
                "http"  : http,
                "https" : https,
                }
            ip = requests.get(website, proxies=proxies, timeout=20).text
            return ip
        except Exception as ex:
            if self.verbose == True:
                print("Error in getting the ip : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
    
    def get_EXITlist(self, path=None):
        try:
            if path == None:
                x = requests.get("https://check.torproject.org/torbulkexitlist").text
                y = x.splitlines()
                exit_list = []
                for item in y:
                    exit_list.append(item)
                return exit_list

            else:
                with open(path, "w") as exits:
                    x = requests.get("https://check.torproject.org/torbulkexitlist").text
                    exits.write(x)
        except Exception as ex:
            if self.verbose == True:
                print("Error in getting the tor exitnode list : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
        
    def new_Ciruit(self, wait=10):
        try:
            #Waiting for New Ciruits
            time.sleep(int(wait))
            self.controller.signal(Signal.NEWNYM)
        except Exception as ex:
            if self.verbose == True:
                print("Error in getting the tor exitnode list : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
    
    def get_Bandwidth(self, printer=False, sentinel=False):
        
        def band_function(controller):
            try:
                bytes_read = self.controller.get_info("traffic/read")
                bytes_written = self.controller.get_info("traffic/written")

                if sentinel == True:
                    if printer == True:
                        print("Bandwidth Read : ", str(bytes_read) + " Bandwidth Written : ", str(bytes_written))
                
                self.bytes_read = bytes_read
                self.bytes_written = bytes_written
            except Exception as ex:
                if self.verbose == True:
                    print("BandWidth function error : ", ex)
                try:
                    self.tor_process.kill()
                except:
                    pass
        try:

            if sentinel == True:
                x = Thread(target=band_function, args=(self.controller))
                x.start()
            else:
                band_function(self.controller)

        except Exception as ex:
            if self.verbose == True:
                print("Error in getting the bandwidth usage : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
    
    def get_ACTIVEciruits(self, printer=False):
        try:

            ciruits = self.controller.get_circuits()
            if printer == True:
                for ciruit in ciruits:
                    print(ciruit, "\n")
            
            return ciruits

        except Exception as ex:
            if self.verbose == True:
                print("Error in getting active ciruits : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
    
    def get_ACTIVEstreams(self, printer=False):
        try:
            streams = self.controller.get_streams()
            if printer == True:
                for stream in streams:
                    print(stream, "\n")
            
            return streams

        except Exception as ex:
            if self.verbose == True:
                print("Error in getting active streams : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
    
    def close_ACTIVEciruit(self, circuit_id, printer=False):
        try:
            self.controller.close_circuit(str(circuit_id))
            if printer == True:
                print("TORic force-closed the Tor Ciruit", str(circuit_id))
        
        except Exception as ex:
            if self.verbose == True:
                print("Error in closing a tor ciruits : ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
    
    def get_allNetStatRelays(self, printer=False):
        try:
            net_stat = self.controller.get_network_statuses()
            if printer == True:
                for nets in net_stat:
                    print(nets)
            return net_stat
        except Exception as ex:
            if self.verbose == True:
                print("Error in getting all Relays: ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)

    def get_latestHeartBeat(self, printer=False):
        try:
            last_HeartBeat = self.controller.get_latest_heartbeat()
            if printer == True:
                print(last_HeartBeat)
            return last_HeartBeat
        except Exception as ex:
            if self.verbose == True:
                print("Error in getting last tor heart beat: ", ex)
            try:
                self.tor_process.kill()
            except:
                pass
            sys.exit(1)
