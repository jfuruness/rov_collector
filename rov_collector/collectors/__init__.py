from .apnic_collector import APNICCollector
from .is_bgp_safe_yet_collector import IsBGPSafeYetCollector
from .rov_rpki_net_collector import ROVRPKINetCollector
from .rovista_collector import ROVISTACollector
from .tma_collector import TMACollector


rov_collector_classes = (
    APNICCollector,
    TMACollector,
    IsBGPSafeYetCollector,
    ROVRPKINetCollector,
    ROVISTACollector,
)

__all__ = [
    "rov_collector_classes",
    "APNICCollector",
    "IsBGPSafeYetCollector",
    "ROVISTACollector",
    "ROVRPKINetCollector",
    "TMACollector",
]
