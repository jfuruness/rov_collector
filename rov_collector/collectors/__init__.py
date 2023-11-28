from .is_bgp_safe_yet_collector import IsBGPSafeYetCollector
from .tma_collector import TMACollector


rov_collector_classes = (TMACollector, IsBGPSafeYetCollector)

__all__ = [
    "rov_collector_classes",
    "IsBGPSafeYetCollector",
    "TMACollector",
]
