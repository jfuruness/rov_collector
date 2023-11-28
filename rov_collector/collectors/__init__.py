from .is_bgp_safe_yet_collector import IsBGPSafeYetCollector
from .rov_rpki_net_collector import ROVRPKINetCollector
from .tma_collector import TMACollector


rov_collector_classes = (TMACollector, IsBGPSafeYetCollector, ROVRPKINetCollector)

__all__ = [
    "rov_collector_classes",
    "IsBGPSafeYetCollector",
    "ROVRPKINetCollector",
    "TMACollector",
]
