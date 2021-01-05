from toolbox import TORic
import sys

class PlaneShift(object):
    def __init__(self, socks_port="", local_port="", verbose=True):
        try:
            if local_port == "":
                if verbose == True:
                    print("No localhost port for PlaneShift selected")
                sys.exit(1)

            if socks_port == "":
                if verbose == True:
                    print("No socks port for PlaneShift selected")
                sys.exit(1)

            #TORic
            toric = TORic(socks_port=socks_port, verbose=verbose)
            print(toric)
            #Variables

        except:
            pass