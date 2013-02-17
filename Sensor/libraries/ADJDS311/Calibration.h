#ifndef Calibration_h
#define Calibration_h

struct calRGBC{
	int red;
	int blue;
	int green;
};


struct Calibration{
	int colorHalf;
	int clearHalf;
	calRGBC capacitor;
};

#endif
