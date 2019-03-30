import shapefile as ShapefileLib
from pyproj import Proj, transform

##############################################################################
##############################################################################
#####                       POLYGON SEMPLIFICATION                      ######
##############################################################################
##############################################################################

def distance_between_points(p1, p2):
    """ Distance between two 2D points """
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def substract_points(p1, p2):
    """ Difference between two 2D points """
    return (p1[0] - p2[0], p1[1] - p2[1])

def multiply_points(p1, p2):
    """ Multiplication between two 2D points """
    return p1[0] * p2[0] + p1[1] * p2[1]

def ramer_douglas_peucker(line, dist):
    """
        Apply Ramer-Douglas-Peucker algorithm to simplify a curve 
        using the distance as threshold:
        - `dist` is the distance threshold;
        - `line` is a list-of-tuples, where each tuple is a 2D coordinate.

        Returns the simplified line.

        https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
    """

    # Base condition to stop the recursion
    if len(line) < 3:
        return line

    (begin, end) = (line[0], line[-1]) if line[0] != line[-1] else (line[0], line[-2])

    # Computing square distances between all the points
    distSq = []
    for curr in line[1:-1]:
        tmp = (distance_between_points(begin, curr) - multiply_points(
                substract_points(end, begin), substract_points(curr, begin)
              ) ** 2 / distance_between_points(begin, end))
        distSq.append(tmp)

    # Find the max square distance
    maxdist = max(distSq)

    # Compare with threshold
    if maxdist < dist ** 2:
        return [begin, end]

    # Pick the index of the point
    pos = distSq.index(maxdist)

    # Call the function recursively starting from this point
    return (ramer_douglas_peucker(line[:pos + 2], dist) + 
            ramer_douglas_peucker(line[pos + 1:], dist)[1:])


##############################################################################
##############################################################################
#####                       COORDINATE CONVERSION                       ######
##############################################################################
##############################################################################

def convert_all_points(points):
    """ Convert all the input point from one coordinate system to another """
    new_points = []
    for point in points:
        new_points.append(convert_point_epsg(point[0], point[1]))
    return new_points

def convert_point_epsg(lat, lon, from_epsg="3004", to_epsg="4326"):
    """
        Trasform input point from one coordinate system to another

        https://github.com/pyproj4/pyproj
        https://3dmetrica.it/i-codici-epsg/
    """
    input_projection = Proj(init="epsg:{}".format(from_epsg))
    outpu_projection = Proj(init="epsg:{}".format(to_epsg))
    return transform(input_projection, outpu_projection, lat, lon)


##############################################################################
##############################################################################
#####                        SHAPEFILE MANAGEMENT                       ######
##############################################################################
##############################################################################

def extract_shapes_from_shapefile(filename, path="shapefiles/"):
    """
        Extract and return all shapes from a shapefile

        https://github.com/GeospatialPython/pyshp#reading-geometry
    """
    with ShapefileLib.Reader(path + filename) as shapefile:
        # Extract all the geometries from shapefile
        shapes = shapefile.shapes()
        return shapes

def extract_records_from_shapefile(filename, path="shapefiles/"):
    """
        Extract and return all the record from a shapefile

        https://github.com/GeospatialPython/pyshp#reading-geometry
    """
    with ShapefileLib.Reader(path + filename) as shapefile:
        # Extract all the records from shapefile
        records = shapefile.records()
        return records
