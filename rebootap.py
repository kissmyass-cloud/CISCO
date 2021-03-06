import os 
from netmiko import ConnectHandler
#File location for the list of IP adderss
AP_List = open("C:\\Users\\adityavarma.tupakula\\Desktop\\AirWave01.txt")
#Tries SSH,Telnet and if both fail prints unable to connect.
for IP in AP_List:
    try:
        ssh = {
            'device_type': 'cisco_ios',
            'ip':   IP,
            'username': 'cisco',
            'password': 'Cisco',
            }
        net_connect = ConnectHandler(**ssh)
        print("ssh Connection established for " + IP)
    except:
        try:
            telnet = {
                'device_type': 'cisco_ios_telnet',
                'ip':   IP,
                'username': 'cisco',
                'password': 'Cisco',
            }
            net_connect = ConnectHandler(**telnet)
            print("Telnet Connection established for " + IP)
        except:
            print ("unable to connect AP " + IP)
            continue
    # sends int br to the AP     
    run_cmd = net_connect.send_command("sh ip int br | include Dot11Radio0")
    #saves the above output to a file
    print(run_cmd, file=open("C:\\AP\\output.txt", "w"))
    #Opens the file locally and looks for name reset 
    r_output = open("C:\\AP\\output.txt", "r")
    
    rl_output = r_output.readlines()

    find_line = str(rl_output[1])
    #shows the line it is seeing on the device
    print(find_line)

    find_word = find_line.rfind("reset")

    # if it does not find reset it will move-on to next ap and if it does it will reboot the ap.
    if find_word == -1:
        print("Radio interface is up " + IP)
        net_connect.disconnect()
    else:
        print("rebooting " + IP)
        net_connect.send_command("reload", expect_string="[confirm]")
        net_connect.disconnect()