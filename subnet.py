from math import log2, ceil


ip_class = "a"

ip_address = "10.0.0.0"
octet_list = [10, 0, 0 ,0]

networks = 1
network_list = []
cidr = 8
default_cidr = 8
max_networks = 4194304

cidr_calculated = False
mask_calculated = False

save_to_file = False
custom_range = False
print_lines = True

#First input: Class of IP, and Input Validation
while True:

    try:
        ip_class = input("Enter IP Class (A, B, or C): ").lower()
    except KeyboardInterrupt:
        exit()

    if not ip_class:
        continue
    
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
   
        if octet_list[0] == 172 and 15 < octet_list[1] < 32:
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
    
    elif inp.count(".") == 0: # Number

        try:
            networks = int(inp)
        except ValueError:
            print("Enter a valid number.")
            continue

        # AI-enhanced clause
        if 0 < networks <= max_networks: # Acceptable range is [0 through max_networks]
            
            tmp = log2(networks) # This is used to determine if network input is possible
            
            if tmp % 1 != 0: # If this is true, then the networks are not a power of 2, so they are not an acceptable network range
                networks = 2 ** ceil(tmp) # In such case, it is adjusted to the next power of 2
                print(f"Networks updated to {networks}")
            break
        else:
            print(f"Out of bounds. Number of networks for this class are [1 to {max_networks}]")
            continue
    
    else: # IP address
        
        # Sanitizing input
        # It is likely that user might put more periods than needed, so we fix it for convenience
        inp = inp.rstrip(".")
        
        # Completing user input
        if inp.count(".") < 3:
            inp += ((3 - inp.count(".")) * ".0")
            print("Subnet mask fixed to", inp)

        try:
            inp = [int(i) for i in inp.split(".")]
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
                print(f"It's not practical to have the last octet as {inp[3]}")
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

    try:
        inp = input("Would you like to save to file? (y/n): ").lower()
    except KeyboardInterrupt:
        exit()

    if inp == "": # If user just presses enter, by default it will not save
        save_to_file = False
    elif inp[0] == "y" or inp == "1":
        save_to_file = True
    else:
        save_to_file = False

if save_to_file:
    while True:
        try:
            inp = input("Enter file name: ") + ".txt"
        except KeyboardInterrupt:
            exit()
        
        try:
            f = open(inp, 'x')
        except FileExistsError:
            print("File already exists. Try a different name.")
            continue
        
        break

# Program asks if all networks are displayed or saved, if not, a different way to get to the answer is used.
if not custom_range and networks > 1:

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

# Engine 1: Prints networks based on a custom range
if custom_range:
    while True: # ask for the range, and input validate. This should return a list with all networks to process
        
        try:
            inp = input("Enter range | Format [34-40] or [12, 14-18] >> ")
        except KeyboardInterrupt:
            if save_to_file:
                f.close()
            exit()

        if inp == "":
            print(f"Enter any range or number between 1 and {networks}")
            continue
        
        inp = inp.strip().replace("," , " ").replace(".", "")

        inp = inp.split()

        for i in inp:

            if "-" in i:
                try:
                    values = [int(x) for x in i.split("-") if x]
                except ValueError:
                    print(f"{i} should be a range numbers. Format \"1-4\"")
                    break

                if len(values) < 2:
                    print(f"{i} is incorrect")
                    break

                if values[0] > values[1]:
                    tmp = values[0]
                    values[0] = values[1]
                    values[1] = tmp

                if values[0] < 1 or values[1] > networks:
                    print(f"{i} is out of bounds. Range is [1 - {networks}]")
                    break

                for i in range(values[0] - 1, values[1]):

                    if i not in network_list:
                        network_list.append(i)
            else:
                try:
                    tmp = int(i) - 1
                except ValueError:
                    print(f"{i} must be a number")
                    break

                if tmp < 0 or tmp >= networks:
                    print(f"{i} is out of bounds. Enter any number between [1 - {networks}]")
                    break

                if tmp not in network_list: # remove duplicates
                    network_list.append(tmp)
        else: # (FOR/ELSE) FOR LOOP FINISHED NORMALLY
            if len(network_list) <= 1024:
                break
            else: # Too many networks to display
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
            for i in network_list:
                line = f"Network {i+1}) 10.{increment * i}.0.0 - 10.{increment * i + tmp}.255.255"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line)
                    f.write("\n")
        elif networks <= 65536:
            increment = int(65536 / networks)
            tmp = increment - 1
            for i in network_list:
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
            for i in network_list:
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
            for i in network_list:
                line = f"Network {i+1}) 172.{octet_list[1]}.{increment*i}.0 - 172.{octet_list[1]}.{increment * i + tmp}.255"
                if print_lines:
                    print(line)
                if save_to_file:
                    f.write(line)
                    f.write("\n")
        else:
            increment = int(65536 / networks)
            tmp = increment - 1
            for i in network_list:
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
        for i in network_list:
            line = f"Network {i+1}) 192.168.{octet_list[2]}.{increment * i} - 192.168.{octet_list[2]}.{increment * i + tmp}"
            if print_lines:
                print(line)
            if save_to_file:
                f.write(line)
                f.write("\n")
else: # Engine 2, "Regular subnetting:" Prints or saves everything using a different method
    print()

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