"""
Domain entities for Google Maps voice assistant.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

from domain.enums import TransportMode, MapType


@dataclass
class Location:
    """
    Represents a geographic location or place.

    Attributes:
        name: Location name or address
        latitude: Latitude coordinate (optional)
        longitude: Longitude coordinate (optional)
        place_id: Google Maps place ID (optional)
        formatted_address: Formatted address string (optional)
        place_type: Type of place (restaurant, hotel, etc.)
        metadata: Additional metadata
    """
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_id: Optional[str] = None
    formatted_address: Optional[str] = None
    place_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def has_coordinates(self) -> bool:
        """Check if location has coordinates."""
        return self.latitude is not None and self.longitude is not None

    def __str__(self) -> str:
        """String representation."""
        if self.formatted_address:
            return self.formatted_address
        return self.name


@dataclass
class Route:
    """
    Represents a route between two locations.

    Attributes:
        origin: Starting location
        destination: Ending location
        transport_mode: Mode of transportation
        distance: Total distance (e.g., "10.5 km")
        duration: Estimated duration (e.g., "15 mins")
        steps: List of route steps/directions
        waypoints: Intermediate waypoints
        is_active: Whether navigation is currently active
    """
    origin: Location
    destination: Location
    transport_mode: TransportMode = TransportMode.DRIVING
    distance: Optional[str] = None
    duration: Optional[str] = None
    steps: List[str] = field(default_factory=list)
    waypoints: List[Location] = field(default_factory=list)
    is_active: bool = False

    def __str__(self) -> str:
        """String representation."""
        mode_str = self.transport_mode.value
        if self.distance and self.duration:
            return (
                f"Route from {self.origin.name} to {self.destination.name} "
                f"({mode_str}): {self.distance}, {self.duration}"
            )
        return f"Route from {self.origin.name} to {self.destination.name} ({mode_str})"


@dataclass
class PlaceDetails:
    """
    Detailed information about a place.

    Attributes:
        location: The location object
        rating: Average rating (0-5)
        total_ratings: Number of ratings
        price_level: Price level (1-4, $ to $$$$)
        opening_hours: Opening hours information
        phone_number: Phone number
        website: Website URL
        reviews: List of reviews
        photos: List of photo URLs
        is_open_now: Whether place is currently open
    """
    location: Location
    rating: Optional[float] = None
    total_ratings: Optional[int] = None
    price_level: Optional[int] = None
    opening_hours: Optional[Dict[str, Any]] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None
    reviews: List[Dict[str, Any]] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)
    is_open_now: Optional[bool] = None

    def get_rating_text(self) -> str:
        """Get formatted rating text."""
        if self.rating and self.total_ratings:
            return f"{self.rating} stars ({self.total_ratings} reviews)"
        elif self.rating:
            return f"{self.rating} stars"
        return "No rating available"

    def __str__(self) -> str:
        """String representation."""
        parts = [self.location.name]
        if self.rating:
            parts.append(f"Rating: {self.rating}")
        if self.is_open_now is not None:
            parts.append("Open now" if self.is_open_now else "Closed")
        return " - ".join(parts)


@dataclass
class MapState:
    """
    Represents the current state of the map view.

    Attributes:
        map_type: Current map type (default, satellite, terrain)
        center_location: Center point of the map
        zoom_level: Current zoom level
        traffic_enabled: Whether traffic layer is shown
        current_route: Active route (if navigating)
        selected_place: Currently selected place details
        search_results: Recent search results
        last_search_query: Last search query
        timestamp: Last update timestamp
    """
    map_type: MapType = MapType.DEFAULT
    center_location: Optional[Location] = None
    zoom_level: int = 15  # Default zoom level
    traffic_enabled: bool = False
    current_route: Optional[Route] = None
    selected_place: Optional[PlaceDetails] = None
    search_results: List[Location] = field(default_factory=list)
    last_search_query: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def is_navigating(self) -> bool:
        """Check if currently navigating a route."""
        return self.current_route is not None and self.current_route.is_active

    def has_search_results(self) -> bool:
        """Check if there are search results available."""
        return len(self.search_results) > 0

    def update_timestamp(self):
        """Update the timestamp to current time."""
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        """String representation."""
        parts = [f"Map: {self.map_type.value}"]
        if self.center_location:
            parts.append(f"Center: {self.center_location.name}")
        if self.is_navigating():
            parts.append(f"Navigating to {self.current_route.destination.name}")
        return ", ".join(parts)


@dataclass
class SearchResult:
    """
    Represents a search result with selection capability.

    Attributes:
        locations: List of location results
        query: Original search query
        selected_index: Index of selected result (for ordinal selection)
        timestamp: When search was performed
    """
    locations: List[Location]
    query: str
    selected_index: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def select(self, index: int) -> Location:
        """
        Select a location by index.

        Args:
            index: 0-based index

        Returns:
            Selected location

        Raises:
            IndexError: If index out of range
        """
        if index < 0 or index >= len(self.locations):
            raise IndexError(f"Index {index} out of range (0-{len(self.locations)-1})")

        self.selected_index = index
        return self.locations[index]

    def select_by_ordinal(self, ordinal: str) -> Location:
        """
        Select by ordinal string (first, second, third).

        Args:
            ordinal: Ordinal string

        Returns:
            Selected location
        """
        ordinal_map = {
            "first": 0,
            "1st": 0,
            "one": 0,
            "second": 1,
            "2nd": 1,
            "two": 1,
            "third": 2,
            "3rd": 2,
            "three": 2,
        }

        index = ordinal_map.get(ordinal.lower())
        if index is None:
            raise ValueError(f"Unknown ordinal: {ordinal}")

        return self.select(index)

    def get_top_n(self, n: int = 3) -> List[Location]:
        """Get top N results."""
        return self.locations[:n]

    def __len__(self) -> int:
        """Number of results."""
        return len(self.locations)
