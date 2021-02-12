from toolbox import TORic
from toolbox import color
import sys
import os
import shutil
import stem
import socket
from threading import Thread
import time

class PlaneShift(object):
    def __init__(self, text_color=True, socks_port="", host="127.0.0.1", port="", verbose=True, hidden_service_dir="/tmp", hidden_service_name="PlaneShift", keep_hidden_service=False):
        try:
            if port == "":
                if verbose == True:
                    if text_color == True:
                        print(color.ERROR + "No localhost port for PlaneShift selected")
                    else:
                        print("No localhost port for PlaneShift selected")
                sys.exit(1)

            if socks_port == "":
                if verbose == True:
                    if text_color == True:
                        print(color.ERROR + "No socks port for PlaneShift selected")
                    else:
                        print("No socks port for PlaneShift selected")
                sys.exit(1)

            #TORic
            toric = TORic.TORic(socks_port=socks_port, verbose=verbose)
            toric.construct_torprocess()
            toric.constuct_controller()
            self.toric = toric
            #Variables
            self.text_color = text_color
            self.verbose = verbose
            self.local_port = int(port)
            self.host = str(host)
            self.socks_port = int(socks_port)
            self.hidden_service_dir = hidden_service_dir
            self.hidden_service_name = hidden_service_name
            self.keep_hidden_service = keep_hidden_service
            self.version = "PlaneShift Router v0.5"
            
        except Exception as ex:
            if self.verbose == True:
                print("Error in PlaneShift Pre Setup : ", ex)
            try:
                self.toric.deconstruct_torprocess()
                self.toric.deconstruct_controller()
            except:
                pass
            sys.exit(1)

    
    def run_default_hidden_service(self, printer=True, alive_check="auto", alive_check_timer=3):

        def alive_checker(host, port, timer):
            x = True
            try:
                while x == True:
                    time.sleep(int(timer))
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((str(host), int(port)))
                    bad_res = 0
                    if int(result) == bad_res:
                        pass
                    else:
                        if self.verbose == True:
                            if self.text_color == True:
                                print(color.ERROR + "Alive Check recorded the target server dead!")
                            else:
                                print("Alive Check recorded the target server dead!")
                        sock.close()
                        self.toric.deconstruct_torprocess()
                        self.toric.deconstruct_controller()
                        if not self.keep_hidden_service == True:
                            shutil.rmtree(self.hsd)
                            self.toric.controller.remove_hidden_service(self.hsd)
                        sys.exit(1)
            except:
                pass
                    



        try:
            self.hidden_service_name = self.hidden_service_name + ".default:" + str(self.socks_port)
            
            self.hsd = os.path.join(self.toric.controller.get_conf('DataDirectory', self.hidden_service_dir), self.hidden_service_name)
            self.hidden_service = self.toric.controller.create_hidden_service(self.hsd, 80, target_port=self.local_port)
            self.onion_address = self.hidden_service.hostname

            if printer == True:
                if self.text_color == True:
                    print("Hidden Service Address : "+ color.MAGENTA, self.onion_address + color.GREEN + ".onion")
                else:
                    print("Hidden Service Address : ", self.onion_address + ".onion")
            if alive_check == "auto":
                x = Thread(target=alive_checker, args=(self.host, self.local_port, alive_check_timer))
                x.start()
            elif alive_check == "manual":
                if self.text_color == True:
                    print("Press Enter if you want to shutdown the " + color.GREEN + "hidden service" + color.WHITE + " : ", end="")
                else:
                    print("Press Enter if you want to shutdown the hidden service : ", end="")
                input("")

                self.toric.deconstruct_torprocess()
                self.toric.deconstruct_controller()
                if not self.keep_hidden_service == True:
                    shutil.rmtree(self.hsd)
                    self.toric.controller.remove_hidden_service(self.hsd)
            else:
                if self.verbose == True:
                    if self.text_color == True:
                        print(color.ERROR + "Unknown Alive Check Parameter found")
                    else:
                        print("Unknown Alive Check Parameter found")
                
                self.toric.deconstruct_torprocess()
                self.toric.deconstruct_controller()
                if not self.keep_hidden_service == True:
                    shutil.rmtree(self.hsd)
                    self.toric.controller.remove_hidden_service(self.hsd)
                sys.exit(1)
                

        except Exception as ex:
            if self.verbose == True:
                if self.text_color == True:
                    print(color.ERROR + "Error in PlaneShift's default Hidden Service Creator : " + color.RED, ex, color.WHITE)
                else:
                    print("Error in PlaneShift's default Hidden Service Creator : ", ex)
            try:
                if not self.keep_hidden_service == True:
                    shutil.rmtree(self.hsd)
                    self.toric.controller.remove_hidden_service(self.hsd)
                self.toric.deconstruct_torprocess()
                self.toric.deconstruct_controller()
            except:
                pass
            sys.exit(1)

    def run_ephemeral_hidden_service(self, printer=True, alive_check="auto", alive_check_timer=3, await_publication=True):
        
        def alive_checker(host, port, timer, key_path):
            x = True
            try:
                while x == True:
                    time.sleep(int(timer))
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((str(host), int(port)))
                    bad_res = 0
                    if int(result) == bad_res:
                        pass
                    else:
                        if self.verbose == True:
                            if self.text_color == True:
                                if self.text_color == True:
                                    print(color.ERROR + "Alive Check recorded the target server dead!")
                                else:
                                    print("Alive Check recorded the target server dead!")
                        sock.close()
                        self.toric.deconstruct_torprocess()
                        self.toric.deconstruct_controller()
                        if not self.keep_hidden_service == True:
                            os.remove(key_path)
                            self.toric.controller.remove_ephemeral_hidden_service(self.onion_address)
                        sys.exit(1)
            except:
                pass
        try:
            self.hidden_service_name = self.hidden_service_name + ".ephemeral:" + str(self.socks_port)
            if not self.hidden_service_dir[-1] == "/":
                self.hidden_service_dir = self.hidden_service_dir + "/"
            key_path = str(self.hidden_service_dir + self.hidden_service_name + ".txt")

            if self.keep_hidden_service == True:      
                if not os.path.isfile(key_path):
                    self.hidden_service = self.toric.controller.create_ephemeral_hidden_service({80: int(self.local_port)}, await_publication = await_publication)
                    with open(key_path, 'w') as key_file:
                        key_file.write('%s:%s' % (self.hidden_service.private_key_type, self.hidden_service.private_key))
                else:
                    with open(key_path, "r") as key_file:
                        key_type, key_content = key_file.read().split(':', 1)
                    self.hidden_service = self.toric.controller.create_ephemeral_hidden_service({80: int(self.local_port)}, key_type = key_type, key_content = key_content, await_publication = await_publication)

            else:
                try:
                    os.remove(key_path)
                except:
                    pass
                self.hidden_service = self.toric.controller.create_ephemeral_hidden_service({80: int(self.local_port)}, await_publication = await_publication)
                
            self.onion_address = self.hidden_service.service_id

            if printer == True:
                if self.text_color == True:
                    print("Hidden Service Address : "+ color.MAGENTA, self.onion_address + color.GREEN + ".onion")
                else:
                    print("Hidden Service Address : ", self.onion_address + ".onion")

            if alive_check == "auto":
                x = Thread(target=alive_checker, args=(self.host, self.local_port, alive_check_timer, key_path))
                x.start()
            elif alive_check == "manual":
                if self.text_color == True:
                    print("Press Enter if you want to shutdown the " + color.GREEN + "hidden service" + color.WHITE + " : ", end="")
                else:
                    print("Press Enter if you want to shutdown the hidden service : ", end="")
                input("")

                self.toric.deconstruct_torprocess()
                self.toric.deconstruct_controller()
                if not self.keep_hidden_service == True:
                    os.remove(key_path)
                    self.toric.controller.remove_ephemeral_hidden_service(self.onion_address)
            else:
                if self.verbose == True:
                    if self.text_color == True:
                        print(color.ERROR + "Unknown Alive Check Parameter found")
                    else:
                        print("Unknown Alive Check Parameter found")

                if not self.keep_hidden_service == True:
                    os.remove(key_path)
                    self.toric.controller.remove_hidden_service(self.hsd)
                self.toric.deconstruct_torprocess()
                self.toric.deconstruct_controller()
                sys.exit(1)
                
        except Exception as ex:
            if self.verbose == True:
                if self.text_color == True:
                    print(color.ERROR + "Error in PlaneShift's ephemeral Hidden Service Creator : ", ex)
                else:
                    print("Error in PlaneShift's ephemeral Hidden Service Creator : ", ex)
            try:
                if not self.keep_hidden_service == True:
                    os.remove(key_path)
                    self.toric.controller.remove_hidden_service(self.hsd)
                self.toric.deconstruct_torprocess()
                self.toric.deconstruct_controller()
            except:
                pass
            sys.exit(1)
