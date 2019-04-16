#include "Modular_Dynamixel.h"
#include <iostream>

Modular_Dynamixel::~Modular_Dynamixel(){
//	cout << endl << "DELETED MORPHOLOGY" << endl << endl; 
};

vector <Modular_Dynamixel::ModulePointer> Modular_Dynamixel::getCreatedModules() {
	vector<ModulePointer> nullVec;
	return nullVec;
}

int Modular_Dynamixel::getAmountBrokenModules()
{
	return 0;
}

void Modular_Dynamixel::closePort() {
	if (settings->portOpen == true) {
		portHandler->closePort();
	}
}

void Modular_Dynamixel::openPort() {
	if (settings->portOpen == false) {
		packetHandler1 = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION1);
		packetHandler2 = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION2);
		char *dev_name = (char*)DEVICENAME;
		portHandler = dynamixel::PortHandler::getPortHandler(dev_name);

		if (portHandler->openPort())
		{
			printf("Succeeded to open the port!\n\n");
			printf(" - Device Name : %s\n", dev_name);
			printf(" - Baudrate    : %d\n\n", portHandler->getBaudRate());
			settings->portOpen = true;
		}
		else
		{
			printf("Failed to open the port! [%s]\n", dev_name);
			printf("Press any key to terminate...\n");
			//		getch();
		}
	}
}

