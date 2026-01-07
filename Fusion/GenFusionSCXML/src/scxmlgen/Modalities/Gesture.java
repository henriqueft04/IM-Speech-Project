/*
 *   Gesture.java generated for multimodal gesture interaction
 */

package scxmlgen.Modalities;

import scxmlgen.interfaces.IModality;

public enum Gesture implements IModality{

	// Map Filters
	RESTAURANTS("[GESTURES][RESTAURANTS]", 1500),
	HOTELS("[GESTURES][HOTELS]", 1500),
	GAS_STATIONS("[GESTURES][GAS_STATIONS]", 1500),
	TRANSPORTS("[GESTURES][TRANSPORTS]", 1500),

	// Map Navigation
	SWIPE_LEFT("[GESTURES][SWIPE_LEFT]", 1500),
	SWIPE_RIGHT("[GESTURES][SWIPE_RIGHT]", 1500),
	SWIPE_UP("[GESTURES][SWIPE_UP]", 1500),
	SWIPE_DOWN("[GESTURES][SWIPE_DOWN]", 1500),
	ZOOM_IN("[GESTURES][ZOOM_IN]", 1500),
	ZOOM_OUT("[GESTURES][ZOOM_OUT]", 1500),

	// Street View
	ENTER_STREET("[GESTURES][ENTER_STREET]", 1500),
	EXIT_STREET("[GESTURES][EXIT_STREET]", 1500),
	FORWARD("[GESTURES][FORWARD]", 1500),
	CAMERA("[GESTURES][CAMERA]", 1500),

	// List Navigation
	SELECT("[GESTURES][SELECT]", 1500),
	UP_OPTION("[GESTURES][UP_OPTION]", 1500),
	DOWN_OPTION("[GESTURES][DOWN_OPTION]", 1500);


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
