from pathlib import Path
from package.handleGeometry.nearPoint import nearPoint
from package.handleGeometry.AdjacentCoding import AdjacentCoding
from package.handleGeometry.utils import to_geojson


def handleNearPoint(data: Path, accuracy: int | float, save):
    res = nearPoint(data, accuracy, save)
    return res


def getGeojson(filepath, crs):
    return to_geojson(filepath, crs)
