#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
//
using namespace std;

bool custom_isdigit(string a) {
	bool val = true;
	for (char c : a) {
		if (isdigit(c) == 0) {
			val = false;
			break;
		}
	}
	return val;
}
vector<string> customSplit_vector(string what, char condition) {
	string val = "";
	vector<string> returned;
	int currentIndex = 0;
	if (what[what.length() - 1] != condition) {
		what += condition;
	}
	for (int i = 0; i < what.length(); i++) {
		if ((isdigit(what[i]) != 0 || what[i] == '-') && what[i] != condition) {
			val += what[i];
		}
		else if (val.length() > 0) {
			returned.push_back(val);
			currentIndex++;
			val = "";
		}
	}
	return returned;
}
string popnondigitconsecutives(string what) {
	for (int i = 0; i < what.length() - 1; i++) {
		if (what[i] == what[i + 1]) {
			if (isdigit(what[i]) == 0) // somehow I couldn't nest this with an AND because
				what.erase(what.begin() + i); // it gave wrong output :|
		}
	}
	return what;
}
void customFormat(string what, vector<int> &range) {
	
	string one = "";
	vector<string> two;
	vector<string> three;

	for (char c : what) {
		if (isdigit(c) != 0 || c == ' ' || c == '-') {
			one += c;
		}
	}

	one = popnondigitconsecutives(one); // just in case
	two = customSplit_vector(one, ' ');

	int val1;
	int val2;
	for (string c : two) {
		if (custom_isdigit(c)) {
			range.push_back(stoi(c));
		}
		else {
			three = customSplit_vector(c, '-');

			val1 = stoi(three[0]);
			val2 = stoi(three[1]);
			if (val1 <= val2) {
				for (int i = val1; i < val2 + 1; i++) {
					range.push_back(i);
				}
			}
			else {
				for (int i = val2; i < val1 + 1; i++) {
					range.push_back(i);
				}
			}
		}
	}
}
int customCount(int what[], int condition) {
	int count = 0;
	for (int i = 0; i < 4; i++) {
		if (what[i] == condition) {
			count++;
		}
	}
	return count;
}
string customMul(string what, int times) {
	string one = "";
	for (int i = 0; i < times; i++) {
		one += what;
	}
	return one;
}
string digitsreturner(string what) {
	string str1 = "";
	for (int i = 0; i < what.length(); i++) {
		if (isdigit(what[i]) != 0) {
			str1 += what[i];
		}
	}
	return str1;
}
int customCount(string what, char condition) {
	int count = 0;
	for (int i = 0; i < what.length(); i++) {
		if (what[i] == condition) {
			count++;
		}
	}
	return count;
}
void customSplit(string what, char condition, int IPSplit[]) {
	string val = "";
	int currentIndex = 0;
	if (what[what.length() - 1] != condition) {
		what += condition;
	}
	for (int i = 0; i < what.length(); i++) {
		if (isdigit(what[i]) != 0 && what[i] != condition) {
			val += what[i];
		}
		else if (val.length() > 0) {
			IPSplit[currentIndex] = stoi(val);
			currentIndex++;
			val = "";
		}
	}
}
string customReplace(string what, char replaced, char by) {
	string str1 = what;
	for (int i = 0; i < str1.length(); i++) {
		if (str1[i] == replaced) {
			str1[i] = by;
		}
	}
	return str1;
}
void prepareBroadcastIP(int netArray[], int broArray[], int howMany) {
	for (int i = 3; i >= 0; i--) {
		if (howMany == 0) {
			broArray[i] = netArray[i];
		}
		else {
			broArray[i] = 255;
			howMany--;
		}
		
	}
}

int main() {

	char IPClass = 'a';
	int defaultCIDR = 8;
	string IP = "10.0.0.0";
	int netIPSplit[4] = { 10, 0, 0, 0 };
	int broIPSplit[4] = { 10, 255, 255, 255 };
	int mask[4] = { 255, 0, 0, 0 };
	string inp = "";
	int networks = 1;
	int CIDR = 8;
	bool gotCIDR = false;
	bool gotMask = false;
	int maxNetworks = pow(2, 22);
	int increment = 0;
	vector<int> range;

	// First Inp
	while (true) {
		cout << "Enter network IP: ";
		cin >> IP;
		if (IP.length() < 1) {
			cout << "Enter a private IP address" << endl;
			continue;
		}
		if (IP[0] == 'a' || IP[0] == 'A') {
			break;
		}
		customSplit(IP, '.', netIPSplit);
		// Class A
		if (netIPSplit[0] == 10) {
			if (netIPSplit[1] != 0 || netIPSplit[2] != 0 || netIPSplit[3] != 0) {
				netIPSplit[1] = 0; netIPSplit[2] = 0; netIPSplit[3] = 0;
			}
			break;
		}
		// Class B
		else if (netIPSplit[0] == 172) {
			if (netIPSplit[1] >= 16 && netIPSplit[1] <= 31) {
				if (netIPSplit[2] != 0 || netIPSplit[3] != 0) {
					netIPSplit[2] = 0; netIPSplit[3] = 0;
				}
				IPClass = 'b';
				defaultCIDR = 16;
				maxNetworks = pow(2, 14);
				break;

			}
			else {
				cout << "Range for Class B private IP address is 172.16.0.0 to 172.31.0.0" << endl;
				continue;
			}
		}
		// Class C
		else if (netIPSplit[0] == 192) {
			if (netIPSplit[1] == 168) {
				if (netIPSplit[3] != 0) {
					netIPSplit[3] = 0;
				}
				if (netIPSplit[2] > 255) {
					cout << "Second octet can't be more than 255" << endl; continue;
				}
				IPClass = 'c';
				defaultCIDR = 24;
				maxNetworks = 64;
				break;
			}
			else {
				cout << "Range for Class C private IP address range is 192.168.0.0 to 192.168.255.0" << endl;
				continue;
			}
		}
		else if (netIPSplit[0] == 255) {
			cout << "Program is not asking for a subnet mask yet. Enter a private IP address" << endl;
			continue;
		}
		else {
			cout << "This program only supports private IP addresses at the moment" << endl;
			continue;
		}
	}

	// Second Inp
	while (true) {
		cout << "Enter number of networks, CIDR, or subnet mask [\"12\", \"/22\" or \"255.255.255.0\"]: ";
		cin >> inp;
		if (inp.length() < 1) {
			cout << "Enter something" << endl;
			continue;
		}
		string str1 = ""; // redundant?
		int var1 = 0;
		if (inp[0] == '/') {
			inp = digitsreturner(inp);
			try {
				var1 = stoi(inp);
			}
			catch (...) {
				cout << "Somehow it failed" << endl; continue;
			}
			if (var1 >= defaultCIDR && var1 < 31) {
				networks = pow(2, (var1 - defaultCIDR));
				gotCIDR = true;
				CIDR = var1;
				break;
			}
			else {
				if (var1 > 30 && var1 < 33) {
					cout << "It's not practical to use " << var1 << " as CIDR" << endl;
					continue; // redundant?
				}
				else {
					cout << "Invalid CIDR [Acceptable Range for this class: [" << defaultCIDR << " - 30]" << endl;
					continue; // reduntant?
				}

			}

		}
		else if (customCount(inp, '.') == 0) {
			inp = digitsreturner(inp);
			if (inp.length() > 0) {
				var1 = stoi(inp); // inp should be all integers, so no reason to try/catch
			}
			else {
				cout << "Enter a valid number" << endl;
				continue;
			}
			if (var1 > 0 && var1 <= maxNetworks) {
				if (log2(var1) == floor(log2(var1))) {
					networks = var1;
					break;
				}
				else {
					networks = pow(2, (floor(log2(var1)) + 1));
					cout << "Networks updated to " << networks << endl;
					break;
				}
			}
			else {
				cout << "Network range for this class is [1 - " << maxNetworks << "]" << endl;
				continue; // redundant?
			}
		}
		else {
			int lastVal = inp.length() - 1;
			while (inp[lastVal] == '.') {
				inp.erase(inp.begin() + lastVal);
				lastVal--;
			}
			if (customCount(inp, '.') < 3) {
				inp += customMul(".0", (3 - customCount(inp, '.')));
			}
			else if (customCount(inp, '.') > 3) {
				cout << "Too many octets... you can just put \"255.\" and it becomes \"255.0.0.0\"" << endl;
				continue;
			}
			try {
				customSplit(inp, '.', mask);
			}
			catch (...) {
				cout << "Enter a valid subnet mask [Ex: 255.255.255.0]" << endl;
				continue;
			}

			if (mask[0] != 255) {
				cout << "All Subnet Masks start with 255" << endl;
				continue;
			}
			else if (IPClass == 'c' && customCount(mask, 255) != 3) {
				cout << "Subnet mask for class c has the first 3 octets as 255 [255.255.255...]" << endl;
				continue;
			}
			else if (IPClass == 'b' && customCount(mask, 255) < 2) {
				cout << "Subnet mask for class b has the first 2 octets as 255 [255.255...]" << endl;
				continue;
			}
			else {
				if (customCount(mask, 0) == 3) {
					break;
				}
			}
			bool correct = true;
			double holder = 0.0;
			int sum = 255;
			for (int i = 0; i < 3; i++) {
				sum += mask[i + 1];
				holder = log2((256 - mask[i + 1]));
				if (mask[i + 1] > mask[i] || holder != floor(holder)) {
					correct = false;
					printf("%i is an invalid octet \n", mask[i + 1]);
					break;
				}
			}



			if (correct) {
				if (mask[3] > 252) {
					cout << "It's not practical to have the last octet as " << mask[3] << endl;
					continue;
				}
				// check depending on class
				double var = sum / 255.0;
				CIDR = 0;
				if (var != floor(var)) {
					CIDR = 8 - log2(256 - (sum % 255));
				}
				CIDR += customCount(mask, 255) * 8;
				gotCIDR = true;
				gotMask = true;
				networks = pow(2, (CIDR - defaultCIDR)); // problem
				break;
			}
			else {
				continue;
			}
		}
	}

	bool displayAll = true;
	if (networks > 1) { // redundant?
		cout << "Display custom range? (y/n): ";
		cin >> inp;
		if (inp[0] == 'y' || inp[0] == 'Y' || inp[0] == '1') {
			displayAll = false;
		}
		else {
			displayAll = true;
		}
	}
	// finding the increment regardless of class
	int h2 = 0;
	{
		double h3 = (defaultCIDR + log2(networks));

		if (h3 / 8.0 != floor(h3 / 8)) {
			increment = pow(2, (((floor(h3 / 8) + 1) * 8) - h3));
		}
		else {
			increment = 1;
			if (networks == 1) {
				increment = 256;
			}
		}

		h2 = increment - 1;
	}
	if (!displayAll) {
		while (true) {
			inp = "";
			cin.ignore();
			cout << "Enter range [Ex: \"17, 19-22, 24\"]: ";
			getline(cin, inp);

			customFormat(inp, range);
			sort(range.begin(), range.end());

			if (range[0] == 0 || range[range.size() - 1] > maxNetworks) {
				cout << "Out of bounds. Range is 1 - " << maxNetworks << endl;
				continue;
			}
			else {
				break;
			}

		}
	}

	if (networks>1)
		prepareBroadcastIP(netIPSplit ,broIPSplit, (4 - floor(log2(networks)*0.125+0.875)) - (defaultCIDR / 8));
	else
		prepareBroadcastIP(netIPSplit, broIPSplit, 4 - (defaultCIDR / 8));

	int OctetToModify = 0;
	int unacceptableOct = defaultCIDR / 8;
	
	if (networks > 1)
		OctetToModify = (log2(networks) - 1 + defaultCIDR) / 8;
	else
		OctetToModify = defaultCIDR / 8;
	
	cout << "\n";

	if (displayAll) {
		broIPSplit[OctetToModify] = h2;

		for (int i = 0; i < networks; i++) {
			printf("Network %1d) %1d.%1d.%1d.%1d - %1d.%1d.%1d.%1d\n", i + 1, netIPSplit[0], netIPSplit[1], netIPSplit[2], netIPSplit[3], broIPSplit[0], broIPSplit[1], broIPSplit[2], broIPSplit[3]);
			netIPSplit[OctetToModify] += increment;
			broIPSplit[OctetToModify] = netIPSplit[OctetToModify] + h2;
			if (netIPSplit[OctetToModify] == 256) {
				netIPSplit[OctetToModify] = 0;
				broIPSplit[OctetToModify] = h2;
				netIPSplit[OctetToModify - 1] += 1;
				broIPSplit[OctetToModify - 1] += 1;
				if (netIPSplit[OctetToModify - 1] == 256) {
					netIPSplit[OctetToModify - 2] += 1;
					broIPSplit[OctetToModify - 2] += 1;
					netIPSplit[OctetToModify - 1] = 0;
					broIPSplit[OctetToModify - 1] = 0;
				}
			}
		}
	} 
	else {
		for (int i : range) {
			netIPSplit[OctetToModify] = (i - 1) * increment;
			if (netIPSplit[OctetToModify] >= 256) {
				netIPSplit[OctetToModify - 1] = floor(netIPSplit[OctetToModify] / 256);
				broIPSplit[OctetToModify - 1] = netIPSplit[OctetToModify - 1];
				netIPSplit[OctetToModify] = netIPSplit[OctetToModify] % 256;
				if (netIPSplit[OctetToModify - 1] >= 256) {
					netIPSplit[OctetToModify - 2] = floor(netIPSplit[OctetToModify - 1] / 256);
					broIPSplit[OctetToModify - 2] = netIPSplit[OctetToModify - 2];
					netIPSplit[OctetToModify - 1] = netIPSplit[OctetToModify - 1] % 256;
					broIPSplit[OctetToModify - 1] = netIPSplit[OctetToModify - 1];
				}
			}
			broIPSplit[OctetToModify] = netIPSplit[OctetToModify] + h2;
			printf("Network %1d) %1d.%1d.%1d.%1d - %1d.%1d.%1d.%1d\n", i, netIPSplit[0], netIPSplit[1], netIPSplit[2], netIPSplit[3], broIPSplit[0], broIPSplit[1], broIPSplit[2], broIPSplit[3]);
		}
	}
	
	
	if (!gotCIDR) {
		CIDR = log2(networks) + defaultCIDR;
	}

	if (!gotMask) {
		string maske = "";
		maske = customMul("255.", CIDR / 8);
		if (CIDR / 8.0 == CIDR / 8) { // this is interesting
			maske += customMul("0.", (4 - customCount(maske, '.')));
			customSplit(maske, '.', mask);
		}
		else {
			int value = 256 - pow(2, (8 - (CIDR % 8))); // simplify
			maske += to_string(value) + ".";
			maske += customMul("0.", (4 - customCount(maske, '.')));
			customSplit(maske, '.', mask);
		}
	}
	cout << "\nSubnet mask: " << mask[0] << "." << mask[1] << "." << mask[2] << "." << mask[3] << " | /" << CIDR << endl;

	if (networks == 1)
		cout << endl << networks << " network with " << maxNetworks * 4 << " users." << endl;
	else
		cout << endl << networks << " networks with " << maxNetworks * 4 / networks << " users per network." << endl; // sometimes it's the increment.


	return 1;
}