from enum import Enum


class LaneSide(Enum):
    """
    Lane boundary side
    """
    LH = 1  # Left
    RH = 2  # Right


class SignalName(Enum):
    """
    Coefficient value of line polynomial

    C0 : Lateral distance [m]
    C1 : Yaw angle [radian]
    C2 : Curvature/2 [1/m]
    C3 : Curvature rate/6 [1/m^2]
    ViewRangeEnd : Maximum longitudinal distance of view range
    ViewRangeStart : Minimum longitudinal distance of view range
    Confidence : Reliability of LD output
    """
    C0 = 1
    C1 = 2
    C2 = 3
    C3 = 4
    ViewRangeEnd = 5
    ViewRangeStart = 5.1
    Confidence = 6
    Quality = 6.1


