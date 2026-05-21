from math import log2, ceil


ip_class = "a"

ip_address = "10.0.0.0"
octet_list = [10, 0, 0 ,0]

networks = 1
cidr = 8
default_cidr = 8
max_networks = 4194304

cidr_calculated = False
mask_calculated = False

save_to_file = False
custom_range = False
print_lines = True #<TO-DO> Print answers? Display answers?

#First input: Class of IP, and Input Validation
while True:

    try:
        ip_class = input("Enter IP Class (A, B, or C): ")
    except KeyboardInterrupt:
        exit()

    if not ip_class:
        continue
    
    ip_class = ip_class.lower() #<TO-DO> Move this up?
    
    if ip_class in ("a", "b", "c"):
        break
    else:
        print("Calculator only supports classes A, B, or C")

#Second input (in applicable): IP address, and input validation depending on the class
if ip_class == "a":

    print("IP address used: 10.0.0.0")

elif ip_class == "b":

    default_cidr = 16
    max_networks = 16384

    while True:
        
        try:
            ip_address = input("Enter IP address: ")
            octet_list = ip_address.split(".")
            octet_list = list(map(int, octet_list))
        except ValueError:
            print("IP addresses have dots and numbers 0-255 [#.#.#.#]")
            continue
        except KeyboardInterrupt:
            exit()
   
        if octet_list[0] == 172 and octet_list[1] > 15 and octet_list[1] < 32: #<TO-DO> use a range 15 < octet_list[1] < 32
            octet_list[2] = 0
            octet_list[3] = 0
            break
        else:
            print("Incorrect IP address. Try again [range is 172.16.0.0 to 172.31.0.0]")

elif ip_class == "c":

    default_cidr = 24
    max_networks = 64

    while True:

        try:
            ip_address = input("Enter IP address: ")
            octet_list = ip_address.split(".")
            octet_list = list(map(int, octet_list))
        except ValueError:
            print("IP addresses have dots and numbers 0-255 [#.#.#.#]")
            continue
        except KeyboardInterrupt:
            exit()

        if octet_list[0] == 192 and octet_list[1] == 168 and octet_list[2] >= 0 and octet_list[2] < 256:
            octet_list[3] = 0
            break
        else:
            print("Incorrect IP, try again [range is 192.168.0.0 to 192.168.255.0]")

#Third input: number of networks, and input validation
while True:

    try:
        inp = input("Enter number of networks or subnet mask [\"12\", \"/22\" or \"255.255.255.128\"]: ")
    except KeyboardInterrupt:
        exit()

    if not inp:
        print("Enter how many networks [Ex: 16], or subnet mask as CIDR or IP [Ex: /24 or 255.255.0.0]")
        continue
    
    # Input sanitation
    inp = inp.replace(",", ".")
        
    if '"' in inp:
        inp = inp.replace('"', "")

    #CIDR
    if inp[0] == "/":

        if inp[1:].isnumeric():
            inp = int(inp[1:])
        else:
            print("Incorrect CIDR")
            continue
        
        if inp >= default_cidr and inp < 31:
            networks = 2 ** (inp - default_cidr)
            cidr_calculated = True
            cidr = inp
            break # (Not break?)
        else:
            print(f"Out of bounds. CIDR for this class is [{default_cidr} to 30]")
            continue
    
    elif inp.count(".") == 0: # num

        try:
            networks = int(inp)
        except ValueError:
            print("Enter a valid number.")
            continue

        # AI-enhanced clause
        if 0 < networks <= max_networks: # Acceptable range is [0 through maxNetworks]
            
            tmp = log2(networks) # This is used to determine if network input is possible
            
            if tmp % 1 != 0: # If this is true, then the networks are not a power of 2, so they are not an acceptable network range
                networks = 2 ** ceil(tmp) # In such case, it is adjusted to the next power of 2
                print(f"Networks updated to {networks}")
            break
        else:
            print(f"Out of bounds. Number of networks for this class are [1 to {max_networks}]")
            continue
    
    else: # IP
        # Sanitizing input
        
        # It is likely that user might put more periods than needed, so we fix it for convenience
        inp = inp.rstrip(".")
        
        # Completing user input
        if inp.count(".") < 3: # <TO-DO> Is this realistic? What if input is 255. OR 3. [NUMPAD]
            inp += ((3 - inp.count(".")) * ".0")
            print("Subnet mask fixed to", inp)

        try:
            inp = [int(i) for i in inp.split(".")] # <TO-DO> Does this cause any other error than ValueError
        except ValueError:
            print("Enter a valid subnet mask.")
            continue

        if len(inp) != 4:
            print("Subnet masks are 4 octets.")
            continue

        if inp[0] != 255:
            print("Subnet masks regardless of class have the first 1st octet = 255")
            continue

        if ip_class == "b" and inp.count(255) < 2:
            print("The first 2 octets of a Class B subnet mask are 255")
            continue
        elif ip_class == "c" and inp.count(255) < 3:
            print("The first 3 octets of a class C subnet mask are 255")
            continue

        cidr = 255

        # Checking each octet for correctness
        for i in range(1, 4):
            tmp = log2(256 - inp[i])

            if inp[i] > inp[i - 1] or tmp % 1 != 0:
                print(f"The octet '{inp[i]}' is incorrect.")
                break

            cidr += inp[i]
        else:
            if inp[3] > 252:
                print(f"It's not practical to have the last octet as {inp[3]}") # <TO-DO> Should we restrict user?
                continue
            
            if cidr % 255 != 0:
                cidr = log2(256 / (256 - (cidr % 255) ) )
            else:
                cidr = 0

            cidr += (inp.count(255) * 8)
            cidr = int(cidr)

            networks = 2 ** (cidr - default_cidr)

            ip_address = inp
            cidr_calculated = True
            mask_calculated = True
            break
        
if networks > 1024: 
# if input says we have to print more than 1024, it could cause issues in some terminals,
# so we give two options
    while True:
        try:
            inp = int(input("Too many networks to display. 2 options:\nType 1) Save to file\nType 2) Display custom range\n Your answer >> "))
        except ValueError:
            print("Enter a number (1 or 2)")
            continue
        except KeyboardInterrupt:
            exit()

        if inp == 1:
            save_to_file = True
            print_lines = False
            break
        elif inp == 2:
            custom_range = True
            break
        else:
            print("No such option")
            
# User is prompted to save to file
if not save_to_file:
    # <TO-DO> BOTH? ONLY ONE? WHICH ONE?
    try:
        inp = input("Would you like to save to file? (y/n): ")
    except KeyboardInterrupt:
        exit()

    inp = inp.lower()

    if inp == "": # If user just presses enter, by default it will not save
        save_to_file = False
    elif inp[0] == "y" or inp == "1":
        save_to_file = True
    else:
        save_to_file = False

if save_to_file:
    try:
        inp = input("Enter file name: ") + ".txt"
    except KeyboardInterrupt:
        exit()
    f = open(inp, 'w') # <TO-DO> This could be improved by checking if file already exists

# Program asks if all networks are displayed or saved, if not, a different way to get to the answer is used.
if not custom_range and networks > 1:# <TO-DO> rewrite comment above

    if save_to_file:

        try:
            inp = input("Save all networks to file? (y/n): ")
        except KeyboardInterrupt:
            f.close()
            exit()

    else:

        try:
            inp = input("Display all networks? (y/n): ")
        except KeyboardInterrupt:
            exit()

    inp = inp.lower()

    if inp == "": # By default, answer will be yes
        custom_range = False
    elif inp[0] == "n" or inp == "0":
        custom_range = True
    else:
        custom_range = False

# Engine 1: Prints networks based on a custom range <TO-DO> refactor below
if custom_range:
    while True: # ask for the range, and input validate. This should return a list with all networks to process
        
        try:
            inp = input("Enter range | Format [34-40] or [12, 14-18] >> ")
        except KeyboardInterrupt:
            if save_to_file: # <TO-DO> Is file open?
                f.close()
            exit()

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
            if save_to_file:
                print("Saving to file only because the range is too long")
                print_lines = False
                break
            else:
                print("Too many networks to display. Try smaller, or save to file instead.")
    print()
    #Depending on the network, we print the selected networks that are stored in inp
    if ip_class=="a":
        octet_list = [10, 0, 0, 0]
        users_per_network = int(16777216 / networks)

        if networks <= 256:
            increment = int(256 / networks)
            tmp = increment - 1
            for i in inp:
                line = f"Network {i+1}) 10.{increment * i}.0.0 - 10.{increment * i + tmp}.255.255"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line)
                    f.write("\n")
        elif networks <= 65536:
            increment = int(65536 / networks)
            tmp = increment - 1
            for i in inp:
                octet_list[1] = (increment * i)//256
                octet_list[2] = (increment * i)%256
                line = f"Network {i+1}) 10.{octet_list[1]}.{octet_list[2]}.0 - 10.{octet_list[1]}.{octet_list[2] + tmp}.255"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line)
                    f.write("\n")
        elif networks <=4194304:
            increment = int(16777216 / networks)
            tmp = increment - 1
            for i in inp:
                value = i * increment
                octet_list[3] = value%256
                value = value//256
                octet_list[1] = value//256
                octet_list[2] = value%256
                line = f"Network {i+1}) 10.{octet_list[1]}.{octet_list[2]}.{octet_list[3]} - 10.{octet_list[1]}.{octet_list[2]}.{octet_list[3]+tmp}"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line)
                    f.write("\n")
        else:
            print("Error, invalid network") # why did I put this...
    elif ip_class=="b":
        users_per_network = int(65536 / networks)
        if networks<=256:
            increment = int(256 / networks)
            tmp = increment - 1
            for i in inp:
                line = f"Network {i+1}) 172.{octet_list[1]}.{increment*i}.0 - 172.{octet_list[1]}.{increment * i + tmp}.255"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line)
                    f.write("\n")
        else:
            increment = int(65536 / networks)
            tmp = increment - 1
            for i in inp:
                octet_list[3] = (increment*i) % 256
                octet_list[2] = (increment*i) // 256
                line = f"Network {i+1}) 172.{octet_list[1]}.{octet_list[2]}.{octet_list[3]} - 172.{octet_list[1]}.{octet_list[2]}.{octet_list[3]+tmp}"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line)
                    f.write("\n")     
    elif ip_class=="c":
        increment = int(256 / networks)
        users_per_network = increment
        tmp = increment - 1
        for i in inp:
            line = f"Network {i+1}) 192.168.{octet_list[2]}.{increment * i} - 192.168.{octet_list[2]}.{increment * i + tmp}"
            if print_lines:
                print(line)
            if save_to_file:
                f.write(line)
                f.write("\n")
else: # Engine 2, "Regular subnetting:" Prints or saves everything using a different method
    print() # <TO-DO> Replace?

    # [A] Display all class A networks
    if ip_class == "a":

        users_per_network = int(16777216 / networks) 
        
        if networks <= 256:
            increment = int(256 / networks)
            tmp = increment - 1
            for i in range(networks):
                line = f"Network {i+1}) 10.{octet_list[1]}.0.0 - 10.{tmp}.255.255"
                
                if print_lines:
                    print(line)
                
                octet_list[1] += increment
                
                tmp += increment

                if save_to_file:
                    f.write(line + "\n")

        elif networks <= 65536:
            increment = int(65536 / networks)
            tmp = increment - 1
            for i in range(networks):
                line = f"Network {i+1}) 10.{octet_list[1]}.{octet_list[2]}.0 - 10.{octet_list[1]}.{octet_list[2]+tmp}.255"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line + "\n")

                octet_list[2] += increment
                if octet_list[2] == 256:
                    octet_list[1] += 1
                    octet_list[2] = 0

        elif networks <= 4194304:
            increment = int(16777216 / networks)
            tmp = increment - 1
            for i in range(networks):
                line = f"Network {i+1}) 10.{octet_list[1]}.{octet_list[2]}.{octet_list[3]} - 10.{octet_list[1]}.{octet_list[2]}.{octet_list[3] + tmp}"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line + "\n")

                octet_list[3] += increment
                if octet_list[3] == 256:
                    octet_list[2] += 1
                    octet_list[3] = 0
                    if octet_list[2] == 256:
                        octet_list[1] += 1
                        octet_list[2] = 0
    # [B] Display all class B networks
    elif ip_class == "b":
        
        users_per_network = int(65536 / networks)

        if networks <= 256:
            increment = int(256 / networks)
            tmp = increment - 1
            for i in range(networks):
                line = f"Network {i+1}) 172.{octet_list[1]}.{octet_list[2]}.0 - 172.{octet_list[1]}.{tmp}.255"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line + "\n")

                octet_list[2] += increment
                tmp += increment
        else:
            increment = int(65536 / networks)
            tmp = increment - 1
            for i in range(networks):
                line = f"Network {i+1}) 172.{octet_list[1]}.{octet_list[2]}.{octet_list[3]} - 172.{octet_list[1]}.{octet_list[2]}.{octet_list[3] + tmp}"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line + "\n")

                octet_list[3] += increment
                if octet_list[3] == 256:
                    octet_list[3] = 0
                    octet_list[2] += 1 
    # [C] Display all class C networks
    elif ip_class == "c":
        
        increment = int(256 / networks)

        users_per_network = increment
        
        tmp = increment - 1
        
        for i in range(networks):
            line = f"Network {i+1}) 192.168.{octet_list[2]}.{octet_list[3]} - 192.168.{octet_list[2]}.{tmp}"
            if print_lines:
                print(line)
            if save_to_file:
                f.write(line + "\n")

            octet_list[3] += increment
            tmp += increment

# Subnet Mask: This part generates the subnet mask as an IP address and as CIDR and prints it or saves it

if not cidr_calculated:
    
    cidr = log2(networks) + default_cidr

    cidr = int(cidr)

if not mask_calculated:

    tmp = cidr // 8 # This is how many 255 octets we will have

    ip_address = [255] * tmp

    tmp = cidr % 8 # This is to determine what the non-255, non-0 octet equals

    if tmp > 0:
        ip_address += [256 - 2 ** (8 - tmp)]

    ip_address += [0] * (4 - len(ip_address)) # Any remaining 0 octets are added

line = f"\nSubnet mask: {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]} | /{cidr}\n"

if networks > 1:
    tmp = f"{networks} networks with {users_per_network} users per network"
else:
    tmp = f"{networks} network with {users_per_network} users"
if print_lines:
    print(line)
    print(tmp)

if save_to_file:
    f.write(line + "\n")
    f.write(tmp + "\n")
    f.close()

input("\n[ Press ENTER 2 times to exit ] ")
input(  "[ Press ENTER 1 time to exit ] ")