from abc import ABC, abstractmethod
from typing import Optional


class ServiceABC(ABC):
    @abstractmethod
    def get_length_track(self, title: str, artist: str, album: Optional[str]) -> Optional[int]:
        pass
