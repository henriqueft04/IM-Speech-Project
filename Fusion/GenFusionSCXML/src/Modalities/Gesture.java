/*
 *   Gesture.java generated for multimodal gesture interaction
 */

package Modalities;

import scxmlgen.interfaces.IModality;

public enum Gesture implements IModality{

	// Map Filters (match Gestures.xml SEMANTIC codes)
	RESTAURANTS("[GESTURES][RESTAURANTS]", 1500),
	HOTELS("[GESTURES][HOTELS]", 1500),
	GAS_STATIONS("[GESTURES][GAS_STATIONS]", 1500),
	TRANSPORTS("[GESTURES][TRANSPORTS]", 1500),

	// Map Navigation (match Gestures.xml SEMANTIC codes)
	SWIPELL("[GESTURES][SWIPELL]", 1500),    // SwipeLeft_Left
	SWIPERR("[GESTURES][SWIPERR]", 1500),    // SwipeRight_Right
	SWIPEU("[GESTURES][SWIPEU]", 1500),      // SwipeUp
	SWIPED("[GESTURES][SWIPED]", 1500),      // SwipeDown
	ZOOMI("[GESTURES][ZOOMI]", 1500),        // ZoomIn
	ZOOMO("[GESTURES][ZOOMO]", 1500),        // ZoomOut

	// Street View (match Gestures.xml SEMANTIC codes)
	ENTERS("[GESTURES][ENTERS]", 1500),      // EnterStreet
	EXITS("[GESTURES][EXITS]", 1500),        // ExitStreet
	// FORWARD = SWIPEU in Street View context (handled by app)
	CAMERA("[GESTURES][CAMERA]", 1500),      // Camera

	// List Navigation (match Gestures.xml SEMANTIC codes)
	SELECT("[GESTURES][SELECT]", 1500),      // Select
	UPOR("[GESTURES][UPOR]", 1500),          // UpOption_Right
	DOWNOL("[GESTURES][DOWNOL]", 1500);      // DownOption_Left


private String event;
private int timeout;

Gesture(String m, int time) {
	event=m;
	timeout=time;
}

@Override
public int getTimeOut(){
	return timeout;
}

@Override
public String getEventName(){
	return event;
}

@Override
public String getEvName(){
	return getModalityName().toLowerCase() +event.toLowerCase();
}

}
