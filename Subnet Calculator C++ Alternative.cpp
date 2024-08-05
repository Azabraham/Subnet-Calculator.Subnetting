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
	vector<string> ran;
	int currentIndex = 0;
	if (what[what.length() - 1] != condition) {
		what += condition;
		// EXPAND THIS SECTIONto handle 192...0 or 192... as inputs?
	}
	for (int i = 0; i < what.length(); i++) {
		if ((isdigit(what[i]) != 0 || what[i] == '-') && what[i] != condition) {
			val += what[i];
		}
		else if (val.length() > 0) {
			ran.push_back(val);
			currentIndex++;
			val = "";
		}
	}
	return ran;

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
int customFunction(string a) {
	int val1 = stoi(a);
	return val1;
}
vector<int> customFormat(string what) {
	string one = "";
	vector<string> two;
	vector<string> three;
	vector<int> returned;
	for (char c : what) {
		if (isdigit(c) != 0 || c == ' ' || c == '-') {
			one += c;
		}
	}
	one = popnondigitconsecutives(one); // just in case
	two = customSplit_vector(one, ' ');

	int val1; //= stoi(a[0]);
	int val2; //= stoi(a[1]);
	for (string c : two) {
		if (custom_isdigit(c)) {
			returned.push_back(stoi(c));
		}
		else {
			three = customSplit_vector(c, '-');
			//four = customFunction(three);
			val1 = customFunction(three[0]);
			val2 = customFunction(three[1]);
			if (val1 <= val2) {
				for (int i = val1; i < val2 + 1; i++) {
					returned.push_back(i);
				}
			}
			else {
				for (int i = val2; i < val1 + 1; i++) {
					returned.push_back(i);
				}
			}

		}
	}
	return returned;
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
		// EXPAND THIS SECTIONto handle 192...0 or 192... as inputs?
	}
	for (int i = 0; i < what.length(); i++) {
		if (isdigit(what[i]) != 0 && what[i] != condition) {
			val += what[i];
		}
		else if (val.length() > 0) {
			IPSplit[currentIndex] = stoi(val); //handle exceptions
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


int main() {
	
	char IPClass = 'a';
	int defaultCIDR = 8;
	string IP = "10.0.0.0";
	int IPSplit[4] = { 10, 0, 0, 0 };
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
		customSplit(IP, '.', IPSplit);
		// Class A
		if (IPSplit[0] == 10) {
			if (IPSplit[1] != 0 || IPSplit[2] != 0 || IPSplit[3] != 0) {
				IPSplit[1] = 0; IPSplit[2] = 0; IPSplit[3] = 0;
			}
			break;
		}
		// Class B
		else if (IPSplit[0] == 172) {
			if (IPSplit[1] >= 16 && IPSplit[1] <= 31) {
				if (IPSplit[2] != 0 || IPSplit[3] != 0) {
					IPSplit[2] = 0; IPSplit[3] = 0;
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
		else if (IPSplit[0] == 192) {
			if (IPSplit[1] == 168) {
				if (IPSplit[3] != 0) {
					IPSplit[3] = 0;
				}
				if (IPSplit[2] > 255) {
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
		else if (IPSplit[0] == 255) {
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
			string inp2 = "";
			cin.ignore();
			cout << "Enter range [Ex: \"17, 19-22, 24\"]: ";
			getline(cin, inp2);

			inp = inp2;

			range = customFormat(inp);
			sort(range.begin(), range.end());

			if (range[0] == 0 || range[range.size() - 1] > maxNetworks) {
				cout << "Out of bounds. Range is 1 - "<<maxNetworks << endl;
				continue;
			}
			else {
				break;
			}

		}
	}

	cout << "\n";
	if (displayAll) {
		if (IPClass == 'a') {
			if (networks <= 256) {
				for (int i = 0; i < networks; i++) {
					cout << "Network " << i + 1 << ") 10." << IPSplit[1] << ".0.0 - 10." << IPSplit[1] + h2 << ".255.255\n";
					IPSplit[1] += increment;
				}
			}
			else if (networks <= 65536) {
				for (int i = 0; i < networks; i++) {
					cout << "Network " << i + 1 << ") 10." << IPSplit[1] << "." << IPSplit[2] << ".0 - 10." << IPSplit[1] << "." << IPSplit[2] + h2 << ".255\n";
					IPSplit[2] += increment;
					if (IPSplit[2] >= 256) {
						IPSplit[2] = 0;
						IPSplit[1] += 1;
					}
				}
			}
			else {
				for (int i = 0; i < networks; i++) {
					cout << "Network " << i + 1 << ") 10." << IPSplit[1] << "." << IPSplit[2] << "." << IPSplit[3] << " - 10." << IPSplit[1] << "." << IPSplit[2] << "." << IPSplit[3] + h2 << "\n";
					IPSplit[3] += increment;
					if (IPSplit[3] >= 256) {
						IPSplit[3] = 0;
						IPSplit[2] += 1;
						if (IPSplit[2] >= 256) {
							IPSplit[2] = 0;
							IPSplit[1] += 1;
						}
					}
				}
			}
			
		}
		else if (IPClass == 'b') {
			int val = IPSplit[1];
			if (networks <= 256) {
				for (int i = 0; i < networks; i++) {
					cout << "Network " << i + 1 << ") 172." << val << "." << IPSplit[2] << ".0 - 172." << val << "." << IPSplit[2] + h2 << ".255\n";
					IPSplit[2] += increment;
				}
			}
			else {
				for (int i = 0; i < networks; i++) {
					cout << "Network " << i + 1 << ") 172." << val << "." << IPSplit[2] << "." << IPSplit[3] << " - 172." << val << "." << IPSplit[2] << "." << IPSplit[3] + h2 << "\n";
					IPSplit[3] += increment;
					if (IPSplit[3] >= 256) {
						IPSplit[3] = 0;
						IPSplit[2] += 1;
					}
				}
			}
		}
		else { // Class C
			int val = 0;
			for (int i = 0; i < networks; i++) {
				cout << "Network " << i + 1 << ") 192.168." << IPSplit[2] << "." << IPSplit[3] << " - 192.168." << IPSplit[2] << "." << IPSplit[3] + h2 << "\n";
				IPSplit[3] += increment;
			}
			
		}
	}
	else {
		if (IPClass == 'a') {
			int holder = 0;
			if (networks <= 256) {
				for (int i : range) {
					IPSplit[1] = (i - 1) * increment;
					cout << "Network " << i << ") 10." << IPSplit[1] << ".0.0 - 10." << IPSplit[1] + h2 << ".255.255\n";
				}
			}
			else if (networks <= 65536) {
				for (int i : range) {
					IPSplit[1] = floor((i - 1) * increment / 256);
					IPSplit[2] = (i - 1) * increment % 256;
					cout << "Network " << i << ") 10." << IPSplit[1] << "." << IPSplit[2] << ".0 - 10." << IPSplit[1] << "." << IPSplit[2] + h2 << ".255\n";
				}
			}
			else {
				for (int i : range) {
					holder = floor((i - 1) * increment / 256);
					IPSplit[1] = floor(holder / 256);
					IPSplit[2] = holder % 256;
					IPSplit[3] = ((i-1) * increment) % 256;
					cout << "Network " << i + 1 << ") 10." << IPSplit[1] << "." << IPSplit[2] << "." << IPSplit[3] << " - 10." << IPSplit[1] << "." << IPSplit[2] << "." << IPSplit[3] + h2 << "\n";
				}
			}
		}
		else if (IPClass == 'b') {
			if (networks <= 256) {
				for (int i : range) {
					IPSplit[2] = (i - 1) * increment;
					cout << "Network " << i + 1 << ") 172." << IPSplit[1] << "." << IPSplit[2] << ".0 - 172." << IPSplit[1] << "." << IPSplit[2] + h2 << ".255\n";
				}
			}
			else {
				for (int i : range) {
					IPSplit[2] = floor((i - 1) * increment / 256);
					IPSplit[3] = (i - 1) * increment % 256;
					cout << "Network " << i + 1 << ") 172." << IPSplit[1] << "." << IPSplit[2] << "." << IPSplit[3] << " - 172." << IPSplit[1] << "." << IPSplit[2] << "." << IPSplit[3] + h2 << "\n";
				}
			}
		}
		else {
			for (int i : range) {
				IPSplit[3] = (i - 1) * increment;
				cout << "Network " << i << ") 192.168." << IPSplit[2] << "." << IPSplit[3] << " - 192.168." << IPSplit[2] << "."  << IPSplit[3] + h2 << "\n";
			}
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
			/*maske = customMul("255.", floor(CIDR / 4));
			(CIDR % 4)*/
			int value = 256 - pow (2, (8 - (CIDR % 8))); // simplify
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