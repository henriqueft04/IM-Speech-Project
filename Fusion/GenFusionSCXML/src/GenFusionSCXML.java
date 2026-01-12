/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


import java.io.IOException;

import Modalities.Gesture;
import Modalities.Output;
import Modalities.Speech;
import scxmlgen.Fusion.FusionGenerator;

/**
 *
 * @author nunof
 */
public class GenFusionSCXML {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {

    FusionGenerator fg = new FusionGenerator();


    fg.Complementary(Speech.ZOOM_IN, Gesture.SWIPEU, Output.ZOOM_IN_UP);
    fg.Complementary(Speech.ZOOM_IN, Gesture.SWIPED, Output.ZOOM_IN_DOWN);
    fg.Complementary(Speech.ZOOM_IN, Gesture.SWIPELL, Output.ZOOM_IN_LEFT);
    fg.Complementary(Speech.ZOOM_IN, Gesture.SWIPERR, Output.ZOOM_IN_RIGHT);
    fg.Complementary(Speech.ZOOM_OUT, Gesture.SWIPEU, Output.ZOOM_OUT_UP);
    fg.Complementary(Speech.ZOOM_OUT, Gesture.SWIPED, Output.ZOOM_OUT_DOWN);
    fg.Complementary(Speech.ZOOM_OUT, Gesture.SWIPELL, Output.ZOOM_OUT_LEFT);
    fg.Complementary(Speech.ZOOM_OUT, Gesture.SWIPERR, Output.ZOOM_OUT_RIGHT);
    fg.Complementary(Speech.GET_DIRECTIONS, Gesture.TRANSPORTS, Output.DIRECTIONS_PUBLIC_TRANSPORT);
    fg.Complementary(Speech.SHOW_TRAFFIC, Gesture.ZOOMO, Output.TRAFFIC_OVERVIEW);
    fg.Complementary(Speech.RECENTER_MAP, Gesture.RESTAURANTS, Output.FILTER_RESTAURANTS_CENTER);
    fg.Complementary(Speech.START_NAVIGATION, Gesture.SWIPEU, Output.STREET_VIEW_FORWARD_CONTINUOUS); // SwipeUp = Forward in Street View




    // Speech Modality - Single Input
    // Search & Navigation
    fg.Single(Speech.SEARCH_LOCATION, Output.SEARCH_LOCATION);
    fg.Single(Speech.GET_DIRECTIONS, Output.GET_DIRECTIONS);
    fg.Single(Speech.START_NAVIGATION, Output.START_NAVIGATION);
    fg.Single(Speech.STOP_NAVIGATION, Output.STOP_NAVIGATION);

    // Map Controls
    fg.Single(Speech.ZOOM_IN, Output.ZOOM_IN);
    fg.Single(Speech.ZOOM_OUT, Output.ZOOM_OUT);
    fg.Single(Speech.CHANGE_MAP_TYPE, Output.CHANGE_MAP_TYPE);
    fg.Single(Speech.RECENTER_MAP, Output.RECENTER_MAP);
    fg.Single(Speech.CENTER_LOCATION, Output.CENTER_LOCATION);
    fg.Single(Speech.SHOW_TRAFFIC, Output.SHOW_TRAFFIC);
    fg.Single(Speech.HIDE_TRAFFIC, Output.HIDE_TRAFFIC);

    // Trip Information
    fg.Single(Speech.GET_TRIP_DURATION, Output.GET_TRIP_DURATION);
    fg.Single(Speech.GET_TRIP_DISTANCE, Output.GET_TRIP_DISTANCE);
    fg.Single(Speech.CHANGE_TRANSPORT_MODE, Output.CHANGE_TRANSPORT_MODE);
    fg.Single(Speech.SWAP_ROUTE, Output.SWAP_ROUTE);

    // Place Selection
    fg.Single(Speech.SELECT_PLACE, Output.SELECT_PLACE);
    fg.Single(Speech.SELECT_ALTERNATIVE_ROUTE, Output.SELECT_ALTERNATIVE_ROUTE);

    // Location Information
    fg.Single(Speech.SHOW_PLACE_DETAILS, Output.SHOW_PLACE_DETAILS);
    fg.Single(Speech.GET_LOCATION_INFO, Output.GET_LOCATION_INFO);
    fg.Single(Speech.SHOW_REVIEWS, Output.SHOW_REVIEWS);
    fg.Single(Speech.SHOW_PHOTOS, Output.SHOW_PHOTOS);
    fg.Single(Speech.GET_OPENING_HOURS, Output.GET_OPENING_HOURS);
    fg.Single(Speech.WHATS_HERE, Output.WHATS_HERE);

    // Conversational
    fg.Single(Speech.HELP, Output.HELP);
    fg.Single(Speech.CANCEL, Output.CANCEL);
    fg.Single(Speech.THANKS, Output.THANKS);

    // Gesture Modality - Single Input
    // Map Filters
    fg.Single(Gesture.RESTAURANTS, Output.GESTURE_RESTAURANTS);
    fg.Single(Gesture.HOTELS, Output.GESTURE_HOTELS);
    fg.Single(Gesture.GAS_STATIONS, Output.GESTURE_GAS_STATIONS);
    fg.Single(Gesture.TRANSPORTS, Output.GESTURE_TRANSPORTS);

    // Map Navigation
    fg.Single(Gesture.SWIPELL, Output.GESTURE_SWIPE_LEFT);
    fg.Single(Gesture.SWIPERR, Output.GESTURE_SWIPE_RIGHT);
    fg.Single(Gesture.SWIPEU, Output.GESTURE_SWIPE_UP);
    fg.Single(Gesture.SWIPED, Output.GESTURE_SWIPE_DOWN);
    fg.Single(Gesture.ZOOMI, Output.GESTURE_ZOOM_IN);
    fg.Single(Gesture.ZOOMO, Output.GESTURE_ZOOM_OUT);

    // Street View
    fg.Single(Gesture.ENTERS, Output.GESTURE_ENTER_STREET);
    fg.Single(Gesture.EXITS, Output.GESTURE_EXIT_STREET);
    // SWIPEU in street view = forward (handled by app context)
    fg.Single(Gesture.CAMERA, Output.GESTURE_CAMERA);

    // List Navigation
    fg.Single(Gesture.SELECT, Output.GESTURE_SELECT);
    fg.Single(Gesture.UPOR, Output.GESTURE_UP_OPTION);
    fg.Single(Gesture.DOWNOL, Output.GESTURE_DOWN_OPTION);

    fg.Redundancy(Speech.ZOOM_IN, Gesture.ZOOMI, Output.ZOOM_IN);
    fg.Redundancy(Speech.ZOOM_OUT, Gesture.ZOOMO, Output.ZOOM_OUT);

    // Cancel Action - Say "cancel" OR exit gesture
    fg.Redundancy(Speech.CANCEL, Gesture.EXITS, Output.CANCEL);
    

    fg.Build("fusion.scxml");

    }
    
}
