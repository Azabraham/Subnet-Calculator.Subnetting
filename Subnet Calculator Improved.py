from math import log2

IPClass = "a"
IP = "10.0.0.0"
networks = 1
CIDR = 8
defaultCIDR = 8
maxNetworks = 4194304
gotCIDR = False
gotMask = False
saveToFile = False
customRange = False
printVal = True

#First input: Class of IP, and Input Validation
while True:

    try:
        IPClass = input("Enter IP Class (A, B, or C): ")
    except KeyboardInterrupt:
        exit()
    
    IPClass = IPClass.lower()
    
    if IPClass in ["a", "b", "c"]:
        break
    else:
        print("Calculator only support classes A, B, or C")

#Second input (in applicable): IP address, and input validation depending on the class
if IPClass=="a":

    print("IP used: 10.0.0.0")
    IPsplit = [10, 0, 0, 0]

elif IPClass=="b":

    defaultCIDR = 16
    maxNetworks = 16384

    while True:
        
        try:
            IP = input("Enter IP: ")
            IPsplit = IP.split(".")
            IPsplit = list(map(int, IPsplit))
        except ValueError:
            print("IP addresses have dots and numbers 0-255 [#.#.#.#]")
            continue
        except KeyboardInterrupt:
            exit()
        
        if IPsplit[0]==172 and IPsplit[1]>15 and IPsplit[1]<32:
            IPsplit[2] = 0
            IPsplit[3] = 0
            break
        else:
            print("Incorrect IP, try again [range is 172.16.0.0 to 172.31.0.0]")

elif IPClass=="c":

    defaultCIDR = 24
    maxNetworks = 64

    while True:

        try:
            IP = input("Enter IP: ")
            IPsplit = IP.split(".")
            IPsplit = list(map(int, IPsplit))
        except ValueError:
            print("IP addresses have dots and numbers 0-255 [#.#.#.#]")
            continue
        except KeyboardInterrupt:
            exit()

        if IPsplit[0]==192 and IPsplit[1]==168 and IPsplit[2]>=0 and IPsplit[2]<256:
            IPsplit[3] = 0
            break
        else:
            print("Incorrect IP, try again [range is 192.168.0.0 to 192.168.255.0]")

#Third input: number of networks, and input validation
while True:
    inp = input("Enter number of networks or subnet mask [\"12\", \"/22\" or \"255.255.255.128\"]: ")

    if len(inp)==0:
        print("Enter how many networks [Ex: 16], or subnet mask as CIDR or IP [Ex: /24 or 255.255.0.0]")
        continue
    
    # Input sanitation
    inp = inp.replace(",", ".")
        
    if '"' in inp:
        inp = inp.replace('"', "")

    #CIDR
    if inp[0]=="/":
        inp2 = ""
        for i in inp:
            if i.isdigit():
                inp2+=i
        try:
            inp = int(inp2)
        except:
            print("Incorrect CIDR");continue
        if inp>=defaultCIDR and inp<31:
            networks = 2**(inp-defaultCIDR)
            gotCIDR = True
            CIDR = inp
            # break
        else:
            print(f"Out of bounds. CIDR for this class is [{defaultCIDR} to 30]");continue
    elif inp.count(".")==0: # num
        try:
            networks = int(inp)
        except:
            print("Enter a valid number.");continue
        if networks > 0 and networks <= maxNetworks:
            holder = log2(networks) # This is used to determine if network input is possible
            if holder!=holder//1: # if it is not possible, then holder would be a decimal, and it would need to be adjusted
                networks = 2**((holder//1)+1)
                networks = int(networks)
                print(f"Networks updated to {networks}")
        else:
            print(f"Out of bounds. Number of networks for this class are [1 to {maxNetworks}]") ; continue
    else: # IP
        #Sanitizing input
        while True:
            if inp[-1]!=".":
                break
            inp = inp[:-1:]
        
        #Completing user input
        if inp.count(".") < 3:
            inp += ((3 - inp.count(".")) * ".0")

        try:
            inp = inp.split(".")
        except:
            print("Enter a valid subnet mask: ") ; continue
        
        if len(inp)!=4:
            print("You entered more than 4 octets.") ; continue

    
        if inp[0]!="255":
            print("Subnet masks regardless of class have the first 1st octet = 255")
            continue
        
        if IPClass=="b" and inp.count("255")<2:
            print("The first 2 octets for a Class B subnet mask are 255")
            continue
        elif IPClass=="c" and inp.count("255")<3:
            print("The first 3 octets of a class C subnet mask are 255")
            continue

        try:
            inp = list(map(int, inp))
        except:
            print("Enter valid numbers") ; continue
        CIDR = 255
        h2 = False
        for i in range(len(inp)-1):
            if h2:
                print(f"Invalid Subnet Mask: {inp[i]} is not a valid octet")
                break
            if inp[i+1] > 255:
                h2 = True
                continue
            CIDR+=inp[i+1]
            holder = log2(256 - inp[i+1])
            if inp[i+1]>inp[i] or holder != (holder//1) or inp[i]!=255 and inp[i+1]!=0:
                h2 = True
                continue

        if h2:
            continue
        else:
            if inp[-1]<=252:
                if CIDR / 255 != CIDR // 255:
                    CIDR=log2(256/(256-(CIDR%255)))
                else:
                    CIDR = 0
                CIDR += (inp.count(255) * 8)
                CIDR = int(CIDR)
                networks = 2**(CIDR - defaultCIDR)
                IP = inp
                gotCIDR = True
                gotMask = True
                # break
            else:
                print(f"It's not practical to have the last octet as {inp[-1]}") ; continue
    
    if networks>1024: # if input says we have to print more than 1024, it could cause issues in some terminals,
        # so we give two options
        while True:
            try:
                inp = int(input("Too many networks to display. 2 options:\nType 1) Save to file\nType 2) Display custom range\n Your answer >> "))
            except:
                print("Enter a number") ; continue
            if inp==1:
                saveToFile = True
                printVal = False
                break
            elif inp==2:
                customRange = True
                break
            else:
                print("No such option")
        break
    else:
        break
            
# User is prompted to save to file
if not saveToFile:
    inp = input("Would you like to save to file? (y/n): ")
    inp = inp.lower()
    if inp == "": # If user just presses enter, by default it will not save
        saveToFile = False
    elif inp[0]=="y" or inp == "yes" or inp == "1":
        saveToFile = True
    else:
        saveToFile = False

if saveToFile:
    inp = input("Enter file name: ") + ".txt"
    f = open(inp, 'w') # This could be improved by checking if file already exists

# Program asks if all networks are displayed or saved, if not, a different way to get to the answer is used.
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
            print(f"Enter any range or number between 1 and {networks}")
            continue
        if not inp[len(inp)-1].isdigit():
            print(f"Try again. Range does not end in '{inp[len(inp)-1]}'")
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
                        inp.append(x-1) #-1 because formula for custom range engine processes numbers as index: starting at 0 
                else:
                    for y in range(m, k+1):
                        inp.append(y-1)#-1 because ^
            else:
                inp.append(i-1)#-1 because ^
        inp = sorted(inp)
        if len(inp)<=1024: # if we have more than 1024 total networks to display...
            if inp[len(inp)-1]<networks and inp[0] >= 0:
                break
            else:
                print(f"One of your networks is outside the range [1 - {networks}]")
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
        IPsplit = [10, 0, 0, 0]
        usersPerNetwork = int(16777216 / networks)

        if networks <= 256:
            increment = int(256 / networks)
            h2 = increment - 1
            for i in inp:
                string1 = f"Network {i+1}) 10.{increment * i}.0.0 - 10.{increment * i + h2}.255.255"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
        elif networks <= 65536:
            increment = int(65536 / networks)
            h2 = increment - 1
            for i in inp:
                IPsplit[1] = (increment * i)//256
                IPsplit[2] = (increment * i)%256
                string1 = f"Network {i+1}) 10.{IPsplit[1]}.{IPsplit[2]}.0 - 10.{IPsplit[1]}.{IPsplit[2] + h2}.255"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
        elif networks <=4194304:
            increment = int(16777216 / networks)
            h2 = increment - 1
            for i in inp:
                value = i * increment
                IPsplit[3] = value%256
                value = value//256
                IPsplit[1] = value//256
                IPsplit[2] = value%256
                string1 = f"Network {i+1}) 10.{IPsplit[1]}.{IPsplit[2]}.{IPsplit[3]} - 10.{IPsplit[1]}.{IPsplit[2]}.{IPsplit[3]+h2}"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
        else:
            print("Error, invalid network") # why did I put this...
    elif IPClass=="b":
        usersPerNetwork = int(65536 / networks)
        if networks<=256:
            increment = int(256 / networks)
            h2 = increment - 1
            for i in inp:
                string1 = f"Network {i+1}) 172.{IPsplit[1]}.{increment*i}.0 - 172.{IPsplit[1]}.{increment * i + h2}.255"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
        else:
            increment = int(65536 / networks)
            h2 = increment - 1
            for i in inp:
                IPsplit[3] = (increment*i) % 256
                IPsplit[2] = (increment*i) // 256
                string1 = f"Network {i+1}) 172.{IPsplit[1]}.{IPsplit[2]}.{IPsplit[3]} - 172.{IPsplit[1]}.{IPsplit[2]}.{IPsplit[3]+h2}"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")     
    elif IPClass=="c":
        increment = int(256 / networks)
        usersPerNetwork = increment
        h2 = increment - 1
        for i in inp:
            string1 = f"Network {i+1}) 192.168.{IPsplit[2]}.{increment * i} - 192.168.{IPsplit[2]}.{increment * i + h2}"
            if printVal:
                print(string1)
            if saveToFile:
                f.write(string1)
                f.write("\n")
else: # Engine 2, "Regular subnetting:" Prints or saves everything using a different method
    print()
    if IPClass == "a":
        usersPerNetwork = int(16777216 / networks)
        if networks <= 256:
            increment = int(256 / networks)
            h2 = increment - 1
            for i in range(networks):
                string1 = f"Network {i+1}) 10.{IPsplit[1]}.0.0 - 10.{h2}.255.255"
                if printVal:
                    print(string1)
                IPsplit[1]+=increment
                h2+=increment
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
        elif networks <= 65536:
            increment = int(65536 / networks)
            h2 = increment - 1
            for i in range(networks):
                string1 = f"Network {i+1}) 10.{IPsplit[1]}.{IPsplit[2]}.0 - 10.{IPsplit[1]}.{IPsplit[2]+h2}.255"
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
            increment = int(16777216 / networks)
            h2 = increment - 1
            for i in range(networks):
                string1 = f"Network {i+1}) 10.{IPsplit[1]}.{IPsplit[2]}.{IPsplit[3]} - 10.{IPsplit[1]}.{IPsplit[2]}.{IPsplit[3] + h2}"
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
            increment = int(256 / networks)
            h2 = increment - 1
            for i in range(networks):
                string1 = f"Network {i+1}) 172.{IPsplit[1]}.{IPsplit[2]}.0 - 172.{IPsplit[1]}.{h2}.255"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
                IPsplit[2]+=increment
                h2+=increment
        else:
            increment = int(65536 / networks)
            h2 = increment - 1
            for i in range(networks):
                string1 = f"Network {i+1}) 172.{IPsplit[1]}.{IPsplit[2]}.{IPsplit[3]} - 172.{IPsplit[1]}.{IPsplit[2]}.{IPsplit[3] + h2}"
                if printVal:
                    print(string1)
                if saveToFile:
                    f.write(string1)
                    f.write("\n")
                IPsplit[3]+=increment
                if IPsplit[3]==256:
                    IPsplit[3]=0
                    IPsplit[2]+=1 
    elif IPClass=="c":
        increment = int(256 / networks)
        usersPerNetwork = increment
        h2 = increment - 1
        for i in range(networks):
            string1 = f"Network {i+1}) 192.168.{IPsplit[2]}.{IPsplit[3]} - 192.168.{IPsplit[2]}.{h2}"
            if printVal:
                print(string1)
            if saveToFile:
                f.write(string1)
                f.write("\n")
            IPsplit[3]+=increment
            h2+=increment

# Subnet Mask: This part generates the subnet mask as an IP address and as CIDR and prints it or saves it

if not gotCIDR:
    CIDR = log2(networks) + defaultCIDR

    CIDR = int(CIDR)

if not gotMask:
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

string1 = f"\nSubnet mask: {IP[0]}.{IP[1]}.{IP[2]}.{IP[3]} | / {CIDR}\n"
if networks > 1:
    defaultCIDR = f"{networks} networks with {usersPerNetwork} users per network"
else:
    defaultCIDR = f"{networks} network with {usersPerNetwork} users"
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