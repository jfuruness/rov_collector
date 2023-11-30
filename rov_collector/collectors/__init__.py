from .apnic_collector import APNICCollector
from .is_bgp_safe_yet_collector import IsBGPSafeYetCollector
from .friends_collector import FriendsCollector
from .rov_rpki_net_collector import ROVRPKINetCollector
from .rovista_collector import ROVISTACollector
from .tma_collector import TMACollector


rov_collector_classes = (
    APNICCollector,
    TMACollector,
    IsBGPSafeYetCollector,
    FriendsCollector,
    ROVRPKINetCollector,
    ROVISTACollector,
)

__all__ = [
    "rov_collector_classes",
    "APNICCollector",
    "IsBGPSafeYetCollector",
    "FriendsCollector",
    "ROVISTACollector",
    "ROVRPKINetCollector",
    "TMACollector",
]
