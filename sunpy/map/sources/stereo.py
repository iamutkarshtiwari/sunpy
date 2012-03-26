"""STEREO Map subclass definitions"""
#pylint: disable=W0221,W0222

__author__ = "Keith Hughitt"
__email__ = "keith.hughitt@nasa.gov"

from sunpy.map.basemap import BaseMap
from datetime import datetime
from sunpy.cm import cm

class EUVIMap(BaseMap):
    """EUVI Image Map definition"""
    def __new__(cls, data, header):
        return BaseMap.__new__(cls, data)
        
    @classmethod
    def get_properties(cls, header):
        """Returns the default and normalized values to use for the Map"""
        date_format = "%Y-%m-%dT%H:%M:%S.%f"

        properties = BaseMap.get_properties(header)
        properties.update({
            "date": datetime.strptime(header['date_obs'], date_format),
            "det": "EUVI",
            "inst": "SECCHI",
            "meas": 'header['wavelnth']',
            "obs": header['obsrvtry'],
            "dsun": header.get('dsun_obs'),
            "cmap": cm.get_cmap(name='sohoeit' + str(header.get('wavelnth'))),
            "name": "EUVI %s" % header['wavelnth'],
            "exptime": header.get('exptime')
        })
        return properties
        
    @classmethod
    def is_datasource_for(cls, header):
        """Determines if header corresponds to an EUVI image"""
        return header.get('detector') == 'EUVI'
        
class CORMap(BaseMap):
    """COR Image Map definition"""
    def __new__(cls, data, header):
        return BaseMap.__new__(cls, data)
        
    @classmethod
    def get_properties(cls, header):
        """Returns the default and normalized values to use for the Map"""
        properties = BaseMap.get_properties(header)
        date_format = "%Y-%m-%dT%H:%M:%S.%f"

        # @TODO: Deal with invalid values for exptime. E.g. STEREO-B COR2
        # on 2012/03/20 has -1 for some images.
        properties.update({
            "date": datetime.strptime(header['date_obs'], date_format),
            "det": header['detector'],
            "inst": "SECCHI",
            "meas": "white-light",
            "obs": header['obsrvtry'],
            'dsun': header.get('dsun_obs'),
            "name": "SECCHI %s" % header['detector'],
            "exptime": header.get('exptime')
        })
        return properties
        
    @classmethod
    def is_datasource_for(cls, header):
        """Determines if header corresponds to an COR image"""
        return header.get('detector') and header.get('detector')[0:3] == "COR"

