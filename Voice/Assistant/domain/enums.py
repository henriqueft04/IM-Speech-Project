"""
Domain enumerations for Google Maps voice assistant.
"""

from enum import Enum, auto


class TransportMode(Enum):
    """Transportation modes for directions."""
    DRIVING = "driving"
    WALKING = "walking"
    TRANSIT = "transit"
    CYCLING = "cycling"
    TWO_WHEELER = "two-wheeler"

    @classmethod
    def from_string(cls, value: str) -> "TransportMode":
        """
        Convert string to TransportMode.

        Args:
            value: String representation (e.g., "car", "drive", "walking")

        Returns:
            TransportMode enum value

        Raises:
            ValueError: If value cannot be mapped
        """
        value_lower = value.lower().strip()

        # Mapping of common terms to transport modes (pt-PT + en)
        mapping = {
            # English
            "driving": cls.DRIVING,
            "drive": cls.DRIVING,
            "car": cls.DRIVING,
            "auto": cls.DRIVING,
            "vehicle": cls.DRIVING,
            "walking": cls.WALKING,
            "walk": cls.WALKING,
            "on foot": cls.WALKING,
            "foot": cls.WALKING,
            "transit": cls.TRANSIT,
            "public transport": cls.TRANSIT,
            "public transportation": cls.TRANSIT,
            "bus": cls.TRANSIT,
            "train": cls.TRANSIT,
            "metro": cls.TRANSIT,
            "subway": cls.TRANSIT,
            "cycling": cls.CYCLING,
            "bike": cls.CYCLING,
            "bicycle": cls.CYCLING,
            "biking": cls.CYCLING,
            "two-wheeler": cls.TWO_WHEELER,
            "motorcycle": cls.TWO_WHEELER,
            "scooter": cls.TWO_WHEELER,
            # Portuguese (pt-PT)
            "carro": cls.DRIVING,
            "conduzir": cls.DRIVING,
            "automóvel": cls.DRIVING,
            "viatura": cls.DRIVING,
            "a pé": cls.WALKING,
            "andar": cls.WALKING,
            "caminhar": cls.WALKING,
            "transportes públicos": cls.TRANSIT,
            "autocarro": cls.TRANSIT,
            "comboio": cls.TRANSIT,
            "trem": cls.TRANSIT,
            "bicicleta": cls.CYCLING,
            "bici": cls.CYCLING,
            "ciclismo": cls.CYCLING,
            "mota": cls.TWO_WHEELER,
            "motociclo": cls.TWO_WHEELER,
            "scooter": cls.TWO_WHEELER,
        }

        if value_lower in mapping:
            return mapping[value_lower]

        for mode in cls:
            if mode.value == value_lower:
                return mode

        raise ValueError(f"Unknown transport mode: {value}")


class MapType(Enum):
    """Map view types."""
    DEFAULT = "default"
    SATELLITE = "satellite"
    TERRAIN = "terrain"
    TRAFFIC = "traffic"

    @classmethod
    def from_string(cls, value: str) -> "MapType":
        """
        Convert string to MapType.

        Args:
            value: String representation

        Returns:
            MapType enum value
        """
        value_lower = value.lower().strip()

        mapping = {
            # English
            "default": cls.DEFAULT,
            "map": cls.DEFAULT,
            "normal": cls.DEFAULT,
            "standard": cls.DEFAULT,
            "satellite": cls.SATELLITE,
            "sat": cls.SATELLITE,
            "aerial": cls.SATELLITE,
            "terrain": cls.TERRAIN,
            "topographic": cls.TERRAIN,
            "topo": cls.TERRAIN,
            "traffic": cls.TRAFFIC,
            "transit": cls.TRAFFIC,
            # Portuguese (pt-PT)
            "padrão": cls.DEFAULT,
            "mapa": cls.DEFAULT,
            "satélite": cls.SATELLITE,
            "terreno": cls.TERRAIN,
            "relevo": cls.TERRAIN,
            "trânsito": cls.TRAFFIC,
            "tráfego": cls.TRAFFIC,
        }

        if value_lower in mapping:
            return mapping[value_lower]

        for map_type in cls:
            if map_type.value == value_lower:
                return map_type

        raise ValueError(f"Unknown map type: {value}")





class ZoomLevel(Enum):
    """Zoom intensity levels."""
    LITTLE = 1
    NORMAL = 2
    LOT = 3

    @classmethod
    def from_string(cls, value: str) -> "ZoomLevel":
        """
        Convert string to ZoomLevel.

        Args:
            value: String representation

        Returns:
            ZoomLevel enum value
        """
        value_lower = value.lower().strip()

        mapping = {
            # English
            "a little": cls.LITTLE,
            "little": cls.LITTLE,
            "slightly": cls.LITTLE,
            "bit": cls.LITTLE,
            "normal": cls.NORMAL,
            "medium": cls.NORMAL,
            "a lot": cls.LOT,
            "lot": cls.LOT,
            "much": cls.LOT,
            "very": cls.LOT,
            # Portuguese (pt-PT)
            "um pouco": cls.LITTLE,
            "pouco": cls.LITTLE,
            "ligeiramente": cls.LITTLE,
            "muito": cls.LOT,
            "bastante": cls.LOT,
        }

        if value_lower in mapping:
            return mapping[value_lower]

        return cls.NORMAL  # Default
