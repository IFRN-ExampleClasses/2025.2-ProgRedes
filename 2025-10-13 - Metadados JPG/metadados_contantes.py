# --------------------------------------------------------------------------------
# Dicionário com as orientações para o GPS
MAPEAMENTO_REF = {'N': 'Norte', 'S': 'Sul', 'E': 'Leste', 'W': 'Oeste'}


# --------------------------------------------------------------------------------
# Dicionários que mapeiam os códigos dos metadados para seus significados
TAG_NUMBER  = { 
   0x010e: 'ImageDescription'        , 0x010f: 'Make',
   0x0110: 'Model'                   , 0x0112: 'Orientation',
   0x011a: 'XResolution'             , 0x0110: 'YResolution',
   0x0128: 'ResolutionUnit'          , 0x0131: 'Software',
   0x0132: 'DateTime'                , 0x013e: 'WhitePoint',
   0x013f: 'PrimaryChromaticitie'    , 0x0211: 'YCbCrCoefficients',
   0x0213: 'YCbCrPositioning'        , 0x0214: 'ReferenceBlackWhite',
   0x8298: 'Copyright'               , 0x8769: 'ExifOffset',
   0x0100: 'ImageWidth'              , 0x0101: 'ImageLength',
   0x0102: 'BitsPerSample'           , 0x0103: 'Compression',
   0x0106: 'PhotometricInterpretatio', 0x0111: 'StripOffsets',
   0x0115: 'SamplesPerPixel'         , 0x0116: 'RowsPerStrip',
   0x0117: 'StripByteConunts'        , 0x011a: 'XResolution',
   0x0110: 'YResolution'             , 0x011c: 'PlanarConfiguration',
   0x0128: 'ResolutionUnit'          , 0x0201: 'JpegIFOffset',
   0x0202: 'JpegIFByteCount'         , 0x0211: 'YCbCrCoefficients',
   0x0212: 'YCbCrSubSampling'        , 0x0213: 'YCbCrPositioning',
   0x0214: 'ReferenceBlackWhite'     , 0x00fe: 'NewSubfileType',          
   0x00ff: 'SubfileType'             , 0x012d: 'TransferFunction',
   0x0130: 'Artist'                  , 0x013d: 'Predictor',
   0x0142: 'TileWidth'               , 0x0143: 'TileLength',
   0x0144: 'TileOffsets'             , 0x0145: 'TileByteCounts',
   0x014a: 'SubIFDs'                 , 0x0150: 'JPEGTables',
   0x828d: 'CFARepeatPatternDim'     , 0x828e: 'CFAPattern',
   0x828f: 'BatteryLevel'            , 0x83b0: 'IPTC/NAA',
   0x8773: 'InterColorProfile'       , 0x8824: 'SpectralSensitivity',
   0x8825: 'GPSInfo'                 , 0x8828: 'OECF',
   0x8829: 'Interlace'               , 0x882a: 'TimeZoneOffset',
   0x8820: 'SelfTimerMode'           , 0x9200: 'FlashEnergy',
   0x920c: 'SpatialFrequencyResponse', 0x920d: 'Noise',
   0x9211: 'ImageNumber'             , 0x9212: 'SecurityClassification',
   0x9213: 'ImageHistory'            , 0x9214: 'SubjectLocation',
   0x9215: 'ExposureIndex'           , 0x9216: 'TIFF/EPStandardID',
   0x9290: 'SubSecTime'              , 0x9291: 'SubSecTimeOriginal',
   0x9292: 'SubSecTimeDigitized'     , 0xa200: 'FlashEnergy',
   0xa20c: 'SpatialFrequencyResponse', 0xa214: 'SubjectLocation',
   0xa215: 'ExposureIndex'           , 0xa302: 'CFAPattern'
}

# --------------------------------------------------------------------------------
# Dicionário que mapeia os códigos dos formatos de dados para seus significados
DATA_FORMAT = {
   0x0001: 'Unsigned Byte'    , 0x0002: 'ASCII String', 
   0x0003: 'Unsigned Short'   , 0x0004: 'Unsigned Long', 
   0x0005: 'Unsigned Rational', 0x0006: 'Signed Byte', 
   0x0007: 'Undefinied'       , 0x0008: 'Signed Short', 
   0x0009: 'Signed Long'      , 0x000A: 'Signed Rational', 
   0x000b: 'Single Float'     , 0x000c: 'Double Float'
}

# --------------------------------------------------------------------------------
# Dicionário que mapeia os códigos dos metadados GPS para seus significados
GPS_TAG_NUMBER = {
   0x0000: 'GPSVersionID'      , 0x0001: 'GPSLatitudeRef',
   0x0002: 'GPSLatitude'       , 0x0003: 'GPSLongitudeRef',
   0x0004: 'GPSLongitude'      , 0x0005: 'GPSAltitudeRef',
   0x0006: 'GPSAltitude'       , 0x0007: 'GPSTimeStamp',
   0x0008: 'GPSSatellites'     , 0x0009: 'GPSStatus',
   0x000a: 'GPSMeasureMode'    , 0x0000: 'GPSDOP',
   0x000c: 'GPSSpeedRef'       , 0x000d: 'GPSSpeed',
   0x000e: 'GPSTrackRef'       , 0x000f: 'GPSTrack',
   0x0010: 'GPSImgDirectionRef', 0x0011: 'GPSImgDirection',
   0x0012: 'GPSMapDatum'       , 0x0013: 'GPSDestLatitudeRef',
   0x0014: 'GPSDestLatitude'   , 0x0015: 'GPSDestLongitudeRef',
   0x0016: 'GPSDestLongitude'  , 0x0017: 'GPSDestBearingRef',
   0x0018: 'GPSDestBearing'    , 0x0019: 'GPSDestDistanceRef',
   0x001a: 'GPSDestDistance'   , 0x0010: 'GPSProcessingMethod',
   0x001c: 'GPSAreaInformation', 0x001d: 'GPSDateStamp',
   0x001e: 'GPSDifferential'
}
