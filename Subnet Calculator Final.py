from math import log2

IPClass = "a"
IP = "10.0.0.0"
networks = 1
CIDR = 8
defaultCIDR = 8
maxNetworks = 4194304
saveToFile = False
customRange = False
printVal = True
#First input: Class of IP, and Input Validation
while True:
    IPClass = input("Enter IP Class (A, B, or C): ")
    IPClass = IPClass.lower()
    if IPClass=="a" or IPClass=="b" or IPClass=="c":
        break
    else:
        print("Wrong IP Class [A, B, or C only]")
#Second input (in applicable): IP address, and input validation depending on the class
if IPClass=="a":
    print("IP used: 10.0.0.0")
    IPsplit = [10, 0, 0, 0]
elif IPClass=="b":
    defaultCIDR = 16
    maxNetworks = 16384
    while True:
        IP = input("Enter IP: ")
        try:
            IPsplit = IP.split(".")
            IPsplit = list(map(int, IPsplit))
        except:
            print("IP addresses have dots and numbers 0-255 [#.#.#.#]")
            continue
        
        if IPsplit[0]==172 and IPsplit[1]>15 and IPsplit[1]<32 and IPsplit[2]==0 and IPsplit[3]==0:
            break
        else:
            print("Incorrect IP, try again [range is 172.16.0.0 to 172.31.0.0]")
elif IPClass=="c":
    defaultCIDR = 24
    maxNetworks = 64
    while True:
        IP = input("Enter IP: ")
        IPsplit = IP.split(".")
        IPsplit = list(map(int, IPsplit))
        if IPsplit[0]==192 and IPsplit[1]==168 and IPsplit[2]>=0 and IPsplit[2]<256  and IPsplit[3]==0:
            break
        else:
            print("Incorrect IP, try again [range is 192.168.0.0 to 192.168.255.0]")

#Third input: number of networks, and input validation
while True:
    try:
        networks = int(input("Enter number of networks: "))
    except:
        print("Enter a number from 0 -", maxNetworks)
        continue

    if networks>0 and networks <= maxNetworks:
        holder = log2(networks) # This is used to determine if network input is possible
        if holder!=holder//1: # if it is not possible, then holder would be a decimal, and it would need to be adjusted
            networks = 2**((holder//1)+1)
            networks = int(networks)
            print("Networks updated to ", networks)

        if networks>1024: # if input says we have to print more than 1024, it could cause issues in some terminals,
            # so we give two options
            while True:
                inp = int(input("Too many networks to display. 2 options:\nType 1) Save to file\nType 2) Display custom range\n Your answer >> "))
                if inp==1:
                    saveToFile = True
                    printVal = False
                    break
                elif inp==2:
                    customRange = True
                    break
                else:
                    print("Incorrect option")
            break
        else:
            break
    else:
        print("Network range for this class is 1 to",maxNetworks,". Try again")

# User is prompted to save to file
if not saveToFile:
    inp = input("Would you like to save to file? (y/n): ")
    inp = inp.lower()
    if inp == "": # If user just presses enter, by default it will not print
        saveToFile = False
    elif inp[0]=="y" or inp == "yes" or inp == "1":
        saveToFile = True
    else:
        saveToFile = False

if saveToFile:
    inp = input("Enter file name: ") + ".txt"
    f = open(inp, 'w') # This could be improved by checking if file already exists

# Program asks if all networks are displayed or saved, if not, a different way to come to the answer is used.
if not customRange and networks > 1:
    if saveToFile:
        inp = input("Save all networks to file? (y/n): ")
    else:
        inp = input("Display all networks? (y/n): ")
    inp = inp.lower()
    if inp == "": # By default, answer will be yes
        customRange = False
    elif inp[0]=="n" or inp == "no" or inp == "0":
        customRange = True
    else:
        customRange = False

# Engine 1: Prints networks based on a custom range
if customRange:
    while True: # ask for the range, and input validate. This should return a list with all networks to process
        inp = input("Enter range | Format [34-40] or [12, 14-18] >> ")
        if inp == "":
            print("Enter any range or number between 1 and",networks)
            continue
        if not inp[len(inp)-1].isdigit():
            print("Try again. Range does not end in", inp[len(inp)-1])
            continue
        inp = inp.replace(" ", "")
        inp = inp.split(",")
        customList = []
        inp2 = []
        k = " "
        m = " "
        for i in inp:
            if "-" in i:
                k = i.split("-")
                if k[0].isdigit() and k[1].isdigit():
                    customList = [int(k[0]), int(k[1])]
                    inp2.append(customList)
            else:
                if i.isdigit():
                    inp2.append(int(i))
        if inp2==[]:
            print("Incorrect Range. Format is \"1, 4, 8-10\" or just a number")
            continue
        inp = []
        for i in inp2:
            if type(i)==list:
                k = i[0]
                m = i[1]
                if k < m:
                    for x in range(k, m+1):
                        inp.append(x-1) #-1 becase formula for custom range engine processes numbers as index: starting at 0 
                else:
                    for y in range(m, k+1):
                        inp.append(y-1)#-1 because ^
            else:
                inp.append(i-1)#-1 because ^
        inp = sorted(inp)
        if len(inp)<=1024: # if we have more than 1024 networks total to display...
            if inp[len(inp)-1]<networks and inp[0] > 0:
                break
            else:
                print("One of your networks is outside the range [1 -", networks, "]")
                continue
        else:
            if saveToFile:
                print("Saving to file only because the range is too long")
                printVal = False
                break
            else:
                print("Too many networks to display. Try smaller, or save to file instead.")
    print()
    #Depending on the network, we print the selected networks that are stored in inp
    if IPClass=="a":
        for i in inp:
            IPsplit = [10, 0, 0, 0]
            usersPerNetwork = int(16777216 / networks)
            if networks <= 256:
                increment = 256 / networks
                increment = int(increment)
                h2 = increment - 1
                network = i
                Oct2 = increment * network
                string1 = "Network "+str(network+1)+") 10."+str(Oct2)+".0.0 - 10."+str(Oct2+h2)+".255.255"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
            elif networks <= 65536:
                increment = 65536 / networks
                increment = int(increment)
                h2 = increment - 1
                network = i
                value = increment * network
                Oct2 = value//256
                Oct3 = value%256
                string1 = "Network "+ str(network+1)+") 10."+str(Oct2)+"."+str(Oct3)+".0 - 10."+str(Oct2)+"."+str(Oct3+h2)+".255"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
            elif networks <=4194304:
                increment = 16777216 / networks
                increment = int(increment)
                h2 = increment - 1
                network = i
                value = network * increment
                Oct4 = value%256
                value2 = value//256
                Oct2 = value2//256
                Oct3 = value2%256
                string1 = "Network "+str(network+1)+") 10."+str(Oct2)+"."+str(Oct3)+"."+str(Oct4)+ " - 10."+str(Oct2)+"."+str(Oct3)+"."+str(Oct4+h2)
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
            else:
                print("Error, invalid network")
    elif IPClass=="b":
        for i in inp:
            usersPerNetwork = int(65536 / networks)
            network = i
            if networks<=256:
                increment = 256 / networks
                increment = int(increment)
            else:
                increment = 65536 / networks
                increment = int(increment)

            h2 = increment - 1
            base = network * increment
            # print(base)
            if networks<=256:
                Oct3 = increment * network
                string1 = "Network "+str(network+1)+") 172.16."+str(Oct3)+".0 - 172.16."+str(Oct3+h2)+".255"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
            else:
                if base<256:
                    Oct4 = base
                    Oct3 = 0
                else:
                    Oct4 = base % 256
                    Oct3 = base // 256
                string1 = "Network "+str(network+1)+") 172.16."+str(Oct3)+"."+str(Oct4)+ " - 172.16."+str(Oct3)+"."+str(Oct4+h2)
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
    elif IPClass=="c":
        for i in inp:
            increment = 256 / networks
            increment = int(increment)
            usersPerNetwork = increment
            h2 = increment - 1
            network = i
            Oct2 = increment * network
            string1 = "Network "+str(network+1)+") 192.168.22."+str(Oct2) + " - 192.168.22."+str(Oct2+h2)
            if printVal:
                print(string1)
            if saveToFile:
                f.write(string1)
                f.write("\n")
else: # Engine 2, "Regular subnetting:" Prints or saves everything using different method
    print()
    if IPClass == "a":
        usersPerNetwork = int(16777216 / networks)
        if networks <= 256:
            increment = 256 / networks
            increment = int(increment)
            h2 = increment - 1
            for i in range(networks):
                net=str(IPsplit[0]) + "." + str(IPsplit[1]) + "." + str(IPsplit[2]) + "." + str(IPsplit[3])
                net1 = str(IPsplit[0]) + "." + str(h2) + ".255.255"
                string1 = "Network " + str(i+1)+ ") " + str(net) + " - " + str(net1)
                if printVal:
                    print(string1)
                IPsplit[1]+=increment
                h2+=increment
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
        elif networks <= 65536:
            increment = 16777216 / (networks * 256)
            increment = int(increment)
            h2 = increment - 1
            for i in range(networks):
                string1 = "Network " + str(i+1) +") " + "10."+str(IPsplit[1]) +"."+ str(IPsplit[2]) + "."+str(IPsplit[3]) + " - 10."+str(IPsplit[1])+"."+str(IPsplit[2]+h2) +".255"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
                IPsplit[2]+=increment
                if IPsplit[2]==256:
                    IPsplit[1]+=1
                    IPsplit[2]=0
        elif networks <=4194304:
            increment = 16777216 / networks
            increment = int(increment)
            h2 = increment - 1
            for i in range(networks):
                string1 = "Network "+str(i+1)+ ") " + "10."+str(IPsplit[1]) +"."+ str(IPsplit[2]) + "."+str(IPsplit[3]) + " - "+ "10."+str(IPsplit[1])+"."+str(IPsplit[2]) +"."+str(IPsplit[3]+h2)
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
                IPsplit[3]+=increment
                if IPsplit[3]==256:
                    IPsplit[2]+=1
                    IPsplit[3]=0
                    if IPsplit[2]==256:
                        IPsplit[1]+=1
                        IPsplit[2]=0
    elif IPClass=="b":
        usersPerNetwork = int(65536 / networks)
        if networks <= 256:
            increment = 256 / networks
            increment = int(increment)
            h2 = increment - 1
            for i in range(networks):
                net=str(IPsplit[0]) + "." + str(IPsplit[1]) + "." + str(IPsplit[2]) + "." + str(IPsplit[3])
                net1 = str(IPsplit[0]) + "." + str(IPsplit[1]) + "." + str(h2) + ".255"
                string1 = "Network " + str(i+1) + ") " + str(net) + " - " + str(net1)
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
                IPsplit[2]+=increment
                h2+=increment
        else:
            increment = 65536 / networks
            increment = int(increment)
            h2 = increment - 1
            for i in range(networks):
                net=str(IPsplit[0]) + "." + str(IPsplit[1]) + "." + str(IPsplit[2]) + "." + str(IPsplit[3])
                net1 = str(IPsplit[0]) + "." + str(IPsplit[1]) + "." + str(IPsplit[2]) + "." + str(h2)
                string1 = "Network " + str(i+1)  + ") "+ str(net) +  " - " + str(net1)
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
                IPsplit[3]+=increment
                h2+=increment
                if IPsplit[3]==256:
                    IPsplit[3]*=0
                    IPsplit[2]+=1
                    h2 = increment - 1  
    elif IPClass=="c":
        increment = 256 / networks
        increment = int(increment)
        usersPerNetwork = increment
        h2 = increment - 1
        for i in range(networks):
            net=str(IPsplit[0]) + "." + str(IPsplit[1]) + "." + str(IPsplit[2]) + "." + str(IPsplit[3])
            net1 = str(IPsplit[0]) + "." + str(IPsplit[1]) + "." + str(IPsplit[2]) + "." + str(h2)
            print("Network "+ str(i+1)+ ") "+ net+ " - "+ net1)
            IPsplit[3]+=increment
            h2+=increment

# Subnet Mask: This part generates the subnet mask as an IP address and as CIDR and prints it or saves it

CIDR = log2(networks) + defaultCIDR

CIDR = int(CIDR)


inp = 0
IPString = ""
inp += 255*(CIDR//8)

IPString="255 "*(inp//255)
if CIDR%8>0:
    IPString+= str(256 - 2**(8 - (CIDR%8)))
    IPString+= " 0"*(3-(inp//255))
else:
    IPString+= "0 "*(4-(inp//255))
IP = list(map(int, IPString.split()))

string1 = "\nSubnet mask: " + str(IP[0])+"."+str(IP[1])+"."+str(IP[2])+"."+str(IP[3]) + " | /" +str(CIDR) + "\n"
if networks > 1:
    defaultCIDR = str(networks)+" networks with "+str(usersPerNetwork)+" users per network"#reusig this var to save memory
else:
    defaultCIDR = str(networks)+" network with "+str(usersPerNetwork)+" users"#reusig this var to save memory
if printVal:
    print(string1)
    print(defaultCIDR)

print()

if saveToFile:
    f.write(string1)
    f.write(defaultCIDR)
    f.write("\n")
    f.close()

# input("[ Press 2 times to exit ] ")
# input("[ Press 1 time to exit ] ")