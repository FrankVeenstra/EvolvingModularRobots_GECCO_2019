#pragma once
#include <vector>
#include <memory>
#include "Modular_Morphology.h"
#include "../../dynamixel/c++/src/dynamixel_sdk.h"

#define PROTOCOL_VERSION1               1.0                 // See which protocol version is used in the Dynamixel
#define PROTOCOL_VERSION2               2.0

#define DEVICENAME                      "\\\\.\\COM26" //"/dev/ttyUSB0"      // Check which port is being used on your controller

using namespace std;

class Modular_Dynamixel : public Modular_Morphology // Abstract Class
{
public:
	Modular_Dynamixel(){};
	~Modular_Dynamixel();
	bool modular = true;
	typedef shared_ptr<ER_Module> ModulePointer;
	virtual vector <ModulePointer> getCreatedModules();
	virtual int getAmountBrokenModules();
	vector<vector <int> > maxModuleTypes;
	int amountIncrement = 1;

	virtual void openPort() = 0;
	void closePort();

	dynamixel::PacketHandler *packetHandler1;
	dynamixel::PacketHandler *packetHandler2;
	dynamixel::PortHandler *portHandler;
};
