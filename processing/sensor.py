
'''
Description: Module to extract embedded information from Product IDs and
             supply configured values for each product

License: NASA Open Source Agreement 1.3
'''


import re
import datetime
from collections import namedtuple


"""Sensor information that is extracted from the details available in the
   Product ID.  Some Items are built from the details, while others are
   generated.

   product_prefix: Generated and specific to the sensor.
   date_acquired: Extracted and converted to a datetime.date object.
   sensor_name: Generated based on the sensor.
   default_pixel_size:  Generated base on the sensor and is a dictionary with
                        keys of 'meters' and 'dd'
"""
SensorInfo = namedtuple('SensorInfo', ['product_prefix',
                                       'date_acquired',
                                       'sensor_name',
                                       'default_pixel_size',
                                       'horizontal',
                                       'vertical',
                                       'path',
                                       'row'])


"""Supported Sensor Codes
"""
LT04_SENSOR_CODE = 'LT04'
LT05_SENSOR_CODE = 'LT05'
LE07_SENSOR_CODE = 'LE07'
LT08_SENSOR_CODE = 'LT08'
LC08_SENSOR_CODE = 'LC08'
LO08_SENSOR_CODE = 'LO08'

TERRA_SENSOR_CODE = 'MOD'
AQUA_SENSOR_CODE = 'MYD'


"""Default pixel sizes based on the input products
"""
DEFAULT_PIXEL_SIZE = {
    'meters': {
        '09A1': 500,
        '09GA': 500,
        '09GQ': 250,
        '09Q1': 250,
        '11A1': 1000,
        '13Q1': 250,
        '13A3': 1000,
        '13A2': 1000,
        '13A1': 500,
        'LC8': 30,
        'LC08': 30,
        'LO8': 30,
        'LO08': 30,
        'LE7': 30,
        'LE07': 30,
        'LT5': 30,
        'LT05': 30,
        'LT4': 30,
        'LT04': 30
    },
    'dd': {
        '09A1': 0.00449155,
        '09GA': 0.00449155,
        '09GQ': 0.002245775,
        '09Q1': 0.002245775,
        '11A1': 0.0089831,
        '13Q1': 0.002245775,
        '13A3': 0.0089831,
        '13A2': 0.0089831,
        '13A1': 0.00449155,
        'LC8': 0.0002695,
        'LC08': 0.0002695,
        'LO8': 0.0002695,
        'LO08': 0.0002695,
        'LE7': 0.0002695,
        'LE07': 0.0002695,
        'LT5': 0.0002695,
        'LT05': 0.0002695,
        'LT4': 0.0002695,
        'LT04': 0.0002695
        }
}


def landsat_sensor_info(product_id):
    """Determine information from Product ID

    Args:
        product_id (str): The Product ID
    """

    (sensor_code, proc_level, path_row, date_acq, proc_date,
     collection_id, tier) = product_id.split('_')

    path = path_row[0:3]
    row = path_row[3:]

    date_acquired = datetime.datetime.strptime(date_acq, '%Y%m%d').date()

    # Determine the product prefix
    product_prefix = ('{0}{1:>03}{2:>03}{3:>08}{4:>02}{5:>02}'
                      .format(sensor_code, path, row, date_acq,
                              collection_id, tier))

    # Determine the default pixel sizes
    meters = DEFAULT_PIXEL_SIZE['meters'][sensor_code]
    dd = DEFAULT_PIXEL_SIZE['dd'][sensor_code]

    default_pixel_size = {'meters': meters, 'dd': dd}

    # Sensor string is used in plotting
    sensor_name = None
    if is_landsat4(product_id):
        sensor_name = 'L4'
    elif is_landsat5(product_id):
        sensor_name = 'L5'
    elif is_landsat7(product_id):
        sensor_name = 'L7'
    elif is_landsat8(product_id):
        sensor_name = 'L8'

    return SensorInfo(product_prefix=product_prefix,
                      date_acquired=date_acquired,
                      sensor_name=sensor_name,
                      default_pixel_size=default_pixel_size,
                      horizontal=0, vertical=0,
                      path=path, row=row)


def modis_sensor_info(product_id):
    """Determine information from Modis Product ID

    Args:
        product_id (str): The Modis Product ID
    """

    parts = product_id.split('.')

    short_name = parts[0]

    date_YYYYDDD = parts[1][1:]
    date_acquired = datetime.datetime.strptime(date_YYYYDDD, '%Y%j').date()

    year = date_acquired.year
    doy = date_acquired.timetuple().tm_yday

    horizontal = parts[2][1:3]
    vertical = parts[2][4:6]

    collection = int(parts[3])

    # Determine the product prefix
    product_prefix = ('{0}h{1:>02}v{2:>02}{3:>04}{4:>03}{5:>03}'
                      .format(short_name, horizontal, vertical, year, doy,
                              collection))

    # Determine the default pixel sizes
    _product_code = short_name[3:]

    meters = DEFAULT_PIXEL_SIZE['meters'][_product_code]
    dd = DEFAULT_PIXEL_SIZE['dd'][_product_code]

    default_pixel_size = {'meters': meters, 'dd': dd}

    # Sensor string is used in plotting
    sensor_name = None
    if is_terra(product_id):
        sensor_name = 'Terra'
    elif is_aqua(product_id):
        sensor_name = 'Aqua'

    return SensorInfo(product_prefix=product_prefix,
                      date_acquired=date_acquired,
                      sensor_name=sensor_name,
                      default_pixel_size=default_pixel_size,
                      horizontal=horizontal, vertical=vertical,
                      path=0, row=0)


"""Map Landsat regular expressions for supported products to the correct
   Product ID parser.

   Example Collection Product ID Format:
       LT05_L1TP_038038_19950624_20160302_01_T1
"""
LANDSAT_COLLECTION_REGEXP_MAPPING = {
    'lt04': (r'^lt04_[a-z0-9]{4}_\d{6}_\d{8}_\d{8}_\d{2}_[a-z0-9]{2}$',
             landsat_sensor_info),

    'lt05': (r'^lt05_[a-z0-9]{4}_\d{6}_\d{8}_\d{8}_\d{2}_[a-z0-9]{2}$',
             landsat_sensor_info),

    'le07': (r'^le07_[a-z0-9]{4}_\d{6}_\d{8}_\d{8}_\d{2}_[a-z0-9]{2}$',
             landsat_sensor_info),

    'lc08': (r'^lc08_[a-z0-9]{4}_\d{6}_\d{8}_\d{8}_\d{2}_[a-z0-9]{2}$',
             landsat_sensor_info),

    'lo08': (r'^lo08_[a-z0-9]{4}_\d{6}_\d{8}_\d{8}_\d{2}_[a-z0-9]{2}$',
             landsat_sensor_info)
}


"""Map MODIS regular expressions for supported products to the correct
   Product ID parser

   Example Product ID Format:
       MOD09GQ.A2000072.h02v09.005.2008237032813
"""
MODIS_REGEXP_MAPPING = {
    'mod09a1': (r'^mod09a1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'mod09ga': (r'^mod09ga\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'mod09gq': (r'^mod09gq\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'mod09q1': (r'^mod09q1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'mod11a1': (r'^mod11a1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'mod13a1': (r'^mod13a1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'mod13a2': (r'^mod13a2\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'mod13a3': (r'^mod13a3\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'mod13q1': (r'^mod13q1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'myd09a1': (r'^myd09a1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'myd09ga': (r'^myd09ga\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'myd09gq': (r'^myd09gq\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'myd09q1': (r'^myd09q1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'myd11a1': (r'^myd11a1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'myd13a1': (r'^myd13a1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'myd13a2': (r'^myd13a2\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'myd13a3': (r'^myd13a3\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info),

    'myd13q1': (r'^myd13q1\.a\d{7}\.h\d{2}v\d{2}\.00[56]\.\d{13}$',
                modis_sensor_info)
}


def is_landsat4(a):
    return a.upper().startswith(LT04_SENSOR_CODE)


def is_landsat5(a):
    return a.upper().startswith(LT05_SENSOR_CODE)


def is_landsat7(a):
    return a.upper().startswith(LE07_SENSOR_CODE)


def is_lt08(a):
    return a.upper().startswith(LT08_SENSOR_CODE)


def is_lc08(a):
    return a.upper().startswith(LC08_SENSOR_CODE)


def is_lo08(a):
    return a.upper().startswith(LO08_SENSOR_CODE)


def is_landsat8(a):
    return any([is_lc08(a), is_lo08(a), is_lt08(a)])


def is_landsat(a):
    return any([is_landsat8(a), is_landsat7(a), is_landsat5(a), is_landsat4(a)])


def is_terra(a):
    return a.upper().startswith('MOD')


def is_aqua(a):
    return a.upper().startswith('MYD')


def is_modis(a):
    return any([is_terra(a), is_aqua(a)])


class ProductNotImplemented(NotImplementedError):
    """Thrown when trying to instantiate an unsupported product
    """
    pass


LANDSAT_COLLECTION_ID_LENGTH = 40
MODIS_COLLECTION_ID_LENGTH = 41


class sensor_memoize(object):
    """Implements a special memoize decorator for sensor information

    Note: This is because the Product ID, may not be just the Product ID, it
          may be a filename.  And we want to use the Product ID, not the
          filename for the key.
    """

    def __init__(self, function):
        """Constructor
        """

        self.function = function
        self.memory = dict()

    def __call__(self, *args):
        """Executes the wrapped function
        """

        # Make sure we use a clean Product ID.
        temp_id = args[0].strip()
        product_id = None

        # Only usethe Product ID
        if is_landsat(temp_id):
            product_id = temp_id[:LANDSAT_COLLECTION_ID_LENGTH]
        elif is_modis(temp_id):
            product_id = temp_id[:MODIS_COLLECTION_ID_LENGTH]
        else:
            raise ProductNotImplemented('[{0}] is not a supported product'
                                        .format(temp_id))

        # Check if we already have it before creating a new one
        try:
            return self.memory[product_id]
        except KeyError:
            self.memory[product_id] = self.function(product_id)
            return self.memory[product_id]


@sensor_memoize
def info(product_id):
    """Return an class instance for the correct Sensor

    Args:
        product_id (str): The Product ID for the requested product.  Can also
                          be a filename with the assumption that the Product
                          ID is prefixed on the filename.
    """

    mapping = None

    # We only support an explicit set of Product ID formats, so that
    # processing breaks if it is changed
    if is_landsat(product_id):
        mapping = LANDSAT_COLLECTION_REGEXP_MAPPING

    elif is_modis(product_id):
        mapping = MODIS_REGEXP_MAPPING

    test_id = product_id.lower()

    # Search through the dictionary and return the object for the match
    for key in mapping.iterkeys():
        if re.match(mapping[key][0], test_id):
            return mapping[key][1](product_id)

    raise ProductNotImplemented('[{0}] is not a supported Product ID format'
                                .format(product_id))
