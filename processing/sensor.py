
'''
    Module to extract embedded information from product names and supply
    configured values for each product'''

import settings
import utilities
import re
import datetime


'''Resolves system-wide identification of sensor name based on three letter
   prefix'''
SENSOR_INFO = {
    'LO8': {'name': 'oli'},
    'LO08': {'name': 'oli'},
    'LC8': {'name': 'olitirs'},
    'LC08': {'name': 'olitirs'},
    'LE7': {'name': 'etm'},
    'LE07': {'name': 'etm'},
    'LT4': {'name': 'tm'},
    'LT04': {'name': 'tm'},
    'LT5': {'name': 'tm'},
    'LT05': {'name': 'tm'},
    'MYD': {'name': 'aqua'},
    'MOD': {'name': 'terra'}
}


'''Default pixel sizes based on the input products'''
DEFAULT_PIXEL_SIZE = {
    'meters': {
        '09A1': 500,
        '09GA': 500,
        '09GQ': 250,
        '09Q1': 250,
        '13Q1': 250,
        '13A3': 1000,
        '13A2': 1000,
        '13A1': 500,
        'LC8': 30,
        'LO8': 30,
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
        '13Q1': 0.002245775,
        '13A3': 0.0089831,
        '13A2': 0.0089831,
        '13A1': 0.00449155,
        'LC8': 0.0002695,
        'LO8': 0.0002695,
        'LE7': 0.0002695,
        'LE07': 0.0002695,
        'LT5': 0.0002695,
        'LT05': 0.0002695,
        'LT4': 0.0002695,
        'LT04': 0.0002695
        }
}


class ProductNotImplemented(NotImplementedError):
    '''Thrown when trying to instantiate an unsupported product'''
    pass


class SensorProduct(object):
    '''Base class for all sensor products'''

    # landsat sceneid, modis tile name, aster granule id, etc.
    product_id = None

    # lt5, le7, mod, myd, etc
    sensor_code = None

    # tm, etm, terra, aqua, etc
    sensor_name = None

    # four digits
    year = None

    # three digits
    doy = None

    # last 5 for LANDSAT, collection # for MODIS
    version = None

    # this is a dictionary
    default_pixel_size = {}

    def __init__(self, product_id):
        '''Constructor for the SensorProduct base class

        Keyword args:
        product_id -- The product id for the requested product
                      (e.g. Landsat is scene id, Modis is tilename, minus
                      file extension)

        Return:
        None
        '''

        super(SensorProduct, self).__init__()

        # Set the Product ID and determine the Sensor Code
        self.product_id = product_id
        self.sensor_code = self.get_satellite_sensor_code(product_id)

        if self.sensor_code not in SENSOR_INFO:
            raise ProductNotImplemented('Unsupported Sensor Code [{0}]'
                                        .format(self.sensor_code))

        self.sensor_name = SENSOR_INFO[self.sensor_code]['name']

    @classmethod
    def get_satellite_sensor_code(cls, product_id):
        '''Returns the satellite-sensor code if known'''

        old_prefixes = ['LT4', 'LT5', 'LE7',
                        'LT8', 'LC8', 'LO8',
                        'MOD', 'MYD']
        collection_prefixes = ['LT04', 'LT05', 'LE07',
                               'LT08', 'LC08', 'LO08']

        satellite_sensor_code = product_id[0:3].upper()
        if satellite_sensor_code in old_prefixes:
            return satellite_sensor_code

        satellite_sensor_code = product_id[0:4].upper()
        if satellite_sensor_code in collection_prefixes:
            return satellite_sensor_code

        raise ProductNotImplemented('Unknown Sensor Code [{0}] or [{1}]'
                                    .format(product_id[0:3], product_id[0:4]))


class Modis(SensorProduct):
    ''' Superclass for all Modis products '''
    version = None
    short_name = None
    horizontal = None
    vertical = None
    date_acquired = None
    date_produced = None

    def __init__(self, product_id):

        super(Modis, self).__init__(product_id)

        parts = product_id.strip().split('.')

        self.short_name = parts[0]
        self.date_acquired = parts[1][1:]
        self.year = self.date_acquired[0:4]
        self.doy = self.date_acquired[4:8]

        # Now that we have the year and doy, we can get the month and day of
        # month
        date = utilities.date_from_doy(self.year, self.doy)
        self.month = date.month
        self.day = date.day

        __hv = parts[2]
        self.horizontal = __hv[1:3]
        self.vertical = __hv[4:6]
        self.version = parts[3]
        self.date_produced = parts[4]

        # set the default pixel sizes

        # this comes out to 09A1, 09GA, 13A1, etc
        _product_code = self.short_name.split(self.sensor_code)[1]

        _meters = DEFAULT_PIXEL_SIZE['meters'][_product_code]

        _dd = DEFAULT_PIXEL_SIZE['dd'][_product_code]

        self.default_pixel_size = {'meters': _meters, 'dd': _dd}


class Terra(Modis):
    ''' Superclass for Terra based Modis products '''
    def __init__(self, product_id):
        super(Terra, self).__init__(product_id)


class Aqua(Modis):
    ''' Superclass for Aqua based Modis products '''
    def __init__(self, product_id):
        super(Aqua, self).__init__(product_id)


class ModisTerra09A1(Terra):
    def __init__(self, product_id):
        super(ModisTerra09A1, self).__init__(product_id)


class ModisTerra09GA(Terra):
    def __init__(self, product_id):
        super(ModisTerra09GA, self).__init__(product_id)


class ModisTerra09GQ(Terra):
    def __init__(self, product_id):
        super(ModisTerra09GQ, self).__init__(product_id)


class ModisTerra09Q1(Terra):
    def __init__(self, product_id):
        super(ModisTerra09Q1, self).__init__(product_id)


class ModisTerra13A1(Terra):
    def __init__(self, product_id):
        super(ModisTerra13A1, self).__init__(product_id)


class ModisTerra13A2(Terra):
    def __init__(self, product_id):
        super(ModisTerra13A2, self).__init__(product_id)


class ModisTerra13A3(Terra):
    def __init__(self, product_id):
        super(ModisTerra13A3, self).__init__(product_id)


class ModisTerra13Q1(Terra):
    def __init__(self, product_id):
        super(ModisTerra13Q1, self).__init__(product_id)


class ModisAqua09A1(Aqua):
    def __init__(self, product_id):
        super(ModisAqua09A1, self).__init__(product_id)


class ModisAqua09GA(Aqua):
    def __init__(self, product_id):
        super(ModisAqua09GA, self).__init__(product_id)


class ModisAqua09GQ(Aqua):
    def __init__(self, product_id):
        super(ModisAqua09GQ, self).__init__(product_id)


class ModisAqua09Q1(Aqua):
    def __init__(self, product_id):
        super(ModisAqua09Q1, self).__init__(product_id)


class ModisAqua13A1(Aqua):
    def __init__(self, product_id):
        super(ModisAqua13A1, self).__init__(product_id)


class ModisAqua13A2(Aqua):
    def __init__(self, product_id):
        super(ModisAqua13A2, self).__init__(product_id)


class ModisAqua13A3(Aqua):
    def __init__(self, product_id):
        super(ModisAqua13A3, self).__init__(product_id)


class ModisAqua13Q1(Aqua):
    def __init__(self, product_id):
        super(ModisAqua13Q1, self).__init__(product_id)


class Landsat(SensorProduct):
    ''' Superclass for all Landsat based products '''

    def __init__(self, product_id):

        product_id = product_id.strip()

        super(Landsat, self).__init__(product_id)

        self.path = product_id[3:6].lstrip('0')
        self.row = product_id[6:9].lstrip('0')
        self.year = product_id[9:13]
        self.doy = product_id[13:16]
        self.station = product_id[16:19]
        self.version = product_id[19:21]

        # Now that we have the year and doy, we can get the month and day of
        # month
        date = utilities.date_from_doy(self.year, self.doy)
        self.month = date.month
        self.day = date.day

        # set the default pixel sizes
        _meters = DEFAULT_PIXEL_SIZE['meters'][self.sensor_code]

        _dd = DEFAULT_PIXEL_SIZE['dd'][self.sensor_code]

        self.default_pixel_size = {'meters': _meters, 'dd': _dd}


class LandsatTM(Landsat):
    ''' Models Thematic Mapper based products '''
    def __init__(self, product_id):
        super(LandsatTM, self).__init__(product_id)


class LandsatETM(Landsat):
    ''' Models Enhanced Thematic Mapper Plus based products '''
    def __init__(self, product_id):
        super(LandsatETM, self).__init__(product_id)


class LandsatOLITIRS(Landsat):
    ''' Models combined Landsat 8 OLI/TIRS products '''
    def __init__(self, product_id):
        super(LandsatOLITIRS, self).__init__(product_id)


class LandsatOLI(Landsat):
    ''' Models Landsat 8 OLI only products '''
    def __init__(self, product_id):
        super(LandsatOLI, self).__init__(product_id)


class LandsatCollection(SensorProduct):
    ''' Superclass for all Landsat collection based products '''

    def __init__(self, product_id):

        product_id = product_id.strip()

        super(LandsatCollection, self).__init__(product_id)

        parts = product_id.split('_')

        self.path = parts[2][0:3].lstrip('0')
        self.row = parts[2][4:].lstrip('0')

        self.year = parts[3][0:4]
        self.month = parts[3][4:6]
        self.day = parts[3][6:]

        # Now that we have the year, month, and day, we can get the day of year
        dt = datetime.date(int(self.year), int(self.month), int(self.day))
        self.doy = dt.timetuple().tm_yday

        # set the default pixel sizes
        _meters = DEFAULT_PIXEL_SIZE['meters'][self.sensor_code]

        _dd = DEFAULT_PIXEL_SIZE['dd'][self.sensor_code]

        self.default_pixel_size = {'meters': _meters, 'dd': _dd}


class LandsatTMCollection(LandsatCollection):
    ''' Models Thematic Mapper based products '''
    def __init__(self, product_id):
        super(LandsatTMCollection, self).__init__(product_id)


class LandsatETMCollection(LandsatCollection):
    ''' Models Enhanced Thematic Mapper Plus based products '''
    def __init__(self, product_id):
        super(LandsatETMCollection, self).__init__(product_id)


def instance(product_id):
    """
    MODIS:
        Supported Products:
            MOD09A1 MOD09GA MOD09GQ MOD09Q1 MYD09A1 MYD09GA MYD09GQ MYD09Q1
            MOD13A1 MOD13A2 MOD13A3 MOD13Q1 MYD13A1 MYD13A2 MYD13A3 MYD13Q1

        Product ID Format: MOD09GQ.A2000072.h02v09.005.2008237032813

    LANDSAT:
        Supported Products:
            LT4 LT5 LE7 LC8 LO8
            LT04 LT05 LE07 LC08 LO08

        Product ID Format: LE72181092013069PFS00
        Collection Product ID Format: LT05_L1T_038038_19950624_20160302_01_T1
    """

    # Remove known file extensions before comparison
    # Do not alter the case of the actual product_id!
    _id = product_id.lower().strip()

    if _id.endswith(settings.MODIS_INPUT_FILENAME_EXTENSION):
        index = _id.index(settings.MODIS_INPUT_FILENAME_EXTENSION)
        # leave original case intact
        product_id = product_id[0:index]
        _id = _id[0:index]

    elif _id.endswith(settings.LANDSAT_INPUT_FILENAME_EXTENSION):
        index = _id.index(settings.LANDSAT_INPUT_FILENAME_EXTENSION)
        # leave original case intact
        product_id = product_id[0:index]
        _id = _id[0:index]

    instances = {
        'lt4': (r'^lt4\d{3}\d{3}\d{4}\d{3}[a-z]{3}[a-z0-9]{2}$',
                LandsatTM),

        'lt04': (r'^lt04_[a-z0-9]{3}_\d{6}_\d{8}_\d{8}_\d{2}_[a-z0-9]{2}$',
                 LandsatTMCollection),

        'lt5': (r'^lt5\d{3}\d{3}\d{4}\d{3}[a-z]{3}[a-z0-9]{2}$',
                LandsatTM),

        'lt05': (r'^lt05_[a-z0-9]{3}_\d{6}_\d{8}_\d{8}_\d{2}_[a-z0-9]{2}$',
                 LandsatTMCollection),

        'le7': (r'^le7\d{3}\d{3}\d{4}\d{3}\w{3}.{2}$',
                LandsatETM),

        'le07': (r'^le07_[a-z0-9]{3}_\d{6}_\d{8}_\d{8}_\d{2}_[a-z0-9]{2}$',
                 LandsatETMCollection),

        'lc8': (r'^lc8\d{3}\d{3}\d{4}\d{3}\w{3}.{2}$',
                LandsatOLITIRS),

        'lo8': (r'^lo8\d{3}\d{3}\d{4}\d{3}\w{3}.{2}$',
                LandsatOLI),

        'mod09a1': (r'^mod09a1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra09A1),

        'mod09ga': (r'^mod09ga\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra09GA),

        'mod09gq': (r'^mod09gq\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra09GQ),

        'mod09q1': (r'^mod09q1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra09Q1),

        'mod13a1': (r'^mod13a1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra13A1),

        'mod13a2': (r'^mod13a2\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra13A2),

        'mod13a3': (r'^mod13a3\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra13A3),

        'mod13q1': (r'^mod13q1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra13Q1),

        'myd09a1': (r'^myd09a1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua09A1),

        'myd09ga': (r'^myd09ga\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua09GA),

        'myd09gq': (r'^myd09gq\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua09GQ),

        'myd09q1': (r'^myd09q1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua09Q1),

        'myd13a1': (r'^myd13a1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua13A1),

        'myd13a2': (r'^myd13a2\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua13A2),

        'myd13a3': (r'^myd13a3\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua13A3),

        'myd13q1': (r'^myd13q1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua13Q1)
    }

    for key in instances.iterkeys():
        if re.match(instances[key][0], _id):
            return instances[key][1](product_id.strip())

    raise ProductNotImplemented('[{0}] is not a supported product'
                                .format(product_id))
