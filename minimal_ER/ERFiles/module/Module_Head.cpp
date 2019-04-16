#include "Module_Head.h"
#include <iostream>

using namespace std; 

Module_Head::Module_Head()
{

}


Module_Head::~Module_Head()
{
	//cout << "REMOVING MODULE!" << endl; 
	removeModule();
}

int Module_Head::init() {
	return -1;
}

int Module_Head::mutate(float mutationRate) {
	
	return -1;
}

int Module_Head::createModule(vector<float> configuration, int relativePosHandle, int parentHandle) {

	int head = simLoadModel("models/headModule.ttm");

	vector<int> shapes;
	vector<int> joints;
	vector<int> sensors;
	simAddObjectToSelection(sim_handle_tree, head);
	int shapesStorage[10]; // stores up to 10 shapes
	simGetObjectSelection(shapesStorage);
	for (int i = 0; i < 10; i++) {
		int objectType = simGetObjectType(shapesStorage[i]);
		if (objectType == sim_object_shape_type) {
			shapes.push_back(shapesStorage[i]);
		}
		else if (objectType == sim_object_joint_type) {
			joints.push_back(shapesStorage[i]);
		}
		else {
			sensors.push_back(shapesStorage[i]);
		}
	}
	simRemoveObjectFromSelection(sim_handle_all, head);

	int fsParams[5];
	fsParams[0] = 0;
	fsParams[1] = 1;
	fsParams[2] = 20; // settings->consecutiveThresholdViolations;
	fsParams[3] = 0;
	fsParams[4] = 0;
	float fsFParams[5];
	fsFParams[0] = 0.005;
	fsFParams[1] = 800; //settings->maxForceSensor;
	fsFParams[2] = 1000;// 1.7; //settings->maxForceSensor; // change torque
	fsFParams[3] = 0;
	fsFParams[4] = 0;
	int fs = simCreateForceSensor(3, fsParams, fsFParams, NULL);

	float fsR[3];
	fsR[0] = configuration[3];
	fsR[1] = configuration[4];
	fsR[2] = configuration[5];

	float fsPos[3];
	fsPos[0] = configuration[0];
	fsPos[1] = configuration[1];
	fsPos[2] = configuration[2];

	float objectOrigin[3]; 
	float zeroOrigin[3] = { 0,0,0 };

	float relPos[3];
	simGetObjectPosition(relativePosHandle, NULL, relPos);
	phenV = 0;
	phenV += relPos[0];
	phenV += relPos[1];
	phenV += relPos[2];
	if (phenV > 1000) {
		phenV = 1000;
	}
	else if (phenV < -1000) {
		phenV = -1000;
	}

	simSetObjectParent(fs, parentHandle, false);
	simSetObjectOrientation(fs, relativePosHandle, fsR);
	simSetObjectPosition(fs, fs, fsPos);

	objectOrigin[0] = 0.0;
	objectOrigin[1] = 0.0;
	objectOrigin[2] = 0.002528001;

	float rotationOrigin[3];
	rotationOrigin[0] = 0.0;
	rotationOrigin[1] = 0.0;
	rotationOrigin[2] = 0.0;

	float PI = 3.14159265;

	simSetObjectOrientation(head, fs, rotationOrigin);
	simSetObjectPosition(head, fs, objectOrigin);
	simSetObjectParent(head, fs, true);

	for (int i = 0; i < shapes.size(); i++) {
		objectHandles.push_back(shapes[i]);
	}
	for (int i = 0; i < joints.size(); i++) {
		objectHandles.push_back(joints[i]);
	}
	for (int i = 0; i < sensors.size(); i++) {
		objectHandles.push_back(sensors[i]);
	}
	//	simReleaseBuffer((simChar*) allHandles);
	//	simReleaseBuffer(NULL);
	objectHandles.push_back(fs);
	//	simSetObjectParent(rdr, -1, true);
	//	attachHandles.push_back(rdr);
	simRemoveObject(head); // removes the dummy that was the parent of the object.

	if (parentHandle == -1) {
		simRemoveObject(fs);
	}
	for (int j = 0; j < objectHandles.size(); j++) {
		simSetObjectSpecialProperty(objectHandles[j], sim_objectspecialproperty_detectable_all);
	}

	return shapes[0];
}

void Module_Head::removeModule() {
	for (int i = 0; i < objectHandles.size(); i++) {
		simRemoveObject(objectHandles[i]);
	}
}

vector<int> Module_Head::getFreeSites(vector<int> targetSites) {
	vector<int> tempFreeSites; 
	for (int i = 0; i < targetSites.size(); i++) {
		for (int j = i; j < freeSites.size(); j++) {
			if (targetSites[i] == freeSites[j] && targetSites[i] != -1) {
				tempFreeSites.push_back(targetSites[i]);
			}
		}
	}
	return tempFreeSites; 
}

void Module_Head::setModuleColor() {

}

vector<int> Module_Head::getObjectHandles() {
	return objectHandles; 
}
shared_ptr<ER_Module> Module_Head::clone() {
	return shared_ptr<ER_Module>(new Module_Head(*this));
}

vector<float> Module_Head::updateModule(vector<float> input) {
	ER_Module::updateModule(input);
	return input;
}

stringstream Module_Head::getModuleParams() {
	// needs to save variables of the module
	stringstream ss;
	ss << "#ModuleType:," << 1 << endl;  // make sure this is the same number as in the module factory
	//ss << "#siteParameters:,";
	//for (int i = 0; i < siteConfigurations.size(); i++) {
	//	ss << "/t,#site:," << 1 << "," << endl;
	//	for (int j = 0; j < siteConfigurations[i].size(); j++) {
	//		ss << siteConfigurations[i][j].x << ",";
	//		ss << siteConfigurations[i][j].y << ",";
	//		ss << siteConfigurations[i][j].z << ",";
	//		ss << siteConfigurations[i][j].rX << ",";
	//		ss << siteConfigurations[i][j].rY << ",";
	//		ss << siteConfigurations[i][j].rZ << ",";
	//	}
	//}
	ss << endl;
	return ss;

}

void Module_Head::setModuleParams(vector<string> values) {

}

vector<float> Module_Head::getPosition() {
	vector<float> positionVector;
	float pos[3];
	simGetObjectPosition(objectHandles[1], -1, pos);
	positionVector.push_back(pos[0]);
	positionVector.push_back(pos[1]);
	positionVector.push_back(pos[2]);
	return positionVector;
};

stringstream Module_Head::getControlParams() {
	stringstream ss;
	ss << "#ControlType," << -1 << endl;
	ss << endl;
	return ss;
}