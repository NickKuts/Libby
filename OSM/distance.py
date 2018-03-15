import math

#         Lat        Long
#coord1 = (60.184663, 24.828095)
#coord2 = (60.188321, 24.836429)
#coord2 = (60.186955, 24.821373)  # T-talo
coord1 = (60.184757, 24.827740)
#coord2 = (60.188176, 24.836499)
coord2 = (90, coord1[1])


def to_radians(deg):
    return deg * math.pi / 180


def calc(c1, c2):
    lat_diff = c1[0] - c2[0]
    lon_diff = c1[1] - c2[1]
    return math.sqrt(lat_diff ** 2 + lon_diff ** 2)


def calc2(lat1, lon1, lat2, lon2):
    radius = 6371 * 1000
    d_lat = to_radians(lat2 - lat1)
    d_lon = to_radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2
    b = math.cos(to_radians(lat1)) * math.cos(to_radians(lat2))
    c = math.sin(d_lon / 2) ** 2
    d = a + b * c
    e = 2 * math.atan2(math.sqrt(d), math.sqrt(1 - d))
    f = radius * e
    return f


def angle(lat1, lon1, lat2, lon2):
    """
    x = math.cos(lat2) * math.sin(lon2 - lon1)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2- lon1)
    return math.atan2(x, y)
    """
    lat1 = to_radians(lat1)
    lon1 = to_radians(lon1)
    lat2 = to_radians(lat2)
    lon2 = to_radians(lon2)
    d_lon = lon2 - lon1
    y = math.sin(d_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    brng = math.atan2(y, x)
    brng = brng * 180 / math.pi
    brng = (brng + 360) % 360
    return brng


print(calc2(coord1[0], coord1[1], coord2[0], coord2[1]))
print(angle(coord1[0], coord1[1], coord2[0], coord2[1]))
