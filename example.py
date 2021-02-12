from PlaneShift import PlaneShift

port_of_local_website = 20020
socks_port_for_TORic_to_use = 20000

planeshift = PlaneShift(socks_port=socks_port_for_TORic_to_use, port=port_of_local_website)
planeshift.run_ephemeral_hidden_service(printer=True)