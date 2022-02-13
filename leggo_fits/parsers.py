import os

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.io.fits import getheader, getdata, getval
from astropy.wcs import WCS

import leggo_builder_settings.fits as leggo_fits_settings
import leggo_builder_settings.paths as leggo_paths_settings


def get_all_header_items(fits_file):
    header_items = {}
    fits_path = os.path.join(leggo_paths_settings.FILE_UPLOADS, fits_file)
    header = getheader(fits_path)
    for key, val in header.items():
        if key in leggo_fits_settings.HEADER_COMBINE_FIELDS:
            val = val.replace(";", ",")
            if key not in header_items:
                header_items[key] = val
            else:
                header_items[key] += val
        elif key not in header_items:
            header_items[key] = val
        else:
            raise RuntimeError

    return header_items, header


def get_full_header(fits_file):
    fits_path = os.path.join(leggo_paths_settings.FILE_UPLOADS, fits_file)
    return getheader(fits_path)


def fits_table_header(fits_file):
    header = get_full_header(fits_file)
    results = []
    for key, val in header.items():
        results.append({'key': key, 'value': val})

    return results

def object_table_header(input_object):
    results = []
    for key, val in input_object.items():
        results.append({'key': key, 'value': val})

    return results


def getHeaderItems(inImage, items, hdrNo=0):
    result = {}
    for key in items:
        try:
            value = getval(inImage, key, hdrNo)
        except KeyError:
            value = None
        result[key] = value
    return result


def delete_header_item(inImage, hdrKey, outImage=None, hdrNo=0):
    hdu = fits.open(inImage)
    header = hdu[hdrNo].header
    for item in hdrKey:
        try:
            del header[item]
        except:
            print("item ", item, ' not in the header')
    if outImage is None:
        hdu.writeto(inImage, overwrite=True)
    else:
        hdu.writeto(outImage, overwrite=True)


def create_footprint(in_image):
    fits_path = os.path.join(leggo_paths_settings.FILE_UPLOADS, in_image)
    wcs = WCS(fits.getheader(fits_path))
    return wcs.calc_footprint()


def check_footprint(in_image, coords):
    wcs = WCS(fits.getheader(in_image))
    return wcs.footprint_contains(coords)


def parse_coordinates(input_coordinates, input_frame, input_units):
    if input_units == 'hmsdms':
        unit = (u.hourangle, u.deg)
    elif input_units == 'deg':
        unit = (u.deg, u.deg)
    else:
        raise NotImplementedError

    c = SkyCoord(input_coordinates, frame=input_frame, unit=unit)

    gal = c.galactic

    return gal.b.value, gal.l.value


def set_slice_header(header):
    delitems = ['CTYPE3', 'CRVAL3', 'CRPIX3', 'CDELT3', 'CUNIT3',
                'CTYPE4', 'CRVAL4', 'CRPIX4', 'CDELT4', 'CUNIT4',
                'NAXIS3', 'NAXIS4', 'NAXIS5', 'CROTA3', 'CROTA4', 'CROTA5',
                'PC3_1', 'PC4_1', 'PC3_2', 'PC4_2', 'PC1_3', 'PC2_3',
                'PC3_3', 'PC4_3', 'PC1_4', 'PC2_4', 'PC3_4', 'PC4_4',
                'PC03_01', 'PC04_01', 'PC03_02', 'PC04_02', 'PC01_03', 'PC02_03',
                'PC03_03', 'PC04_03', 'PC01_04', 'PC02_04', 'PC03_04', 'PC04_04']
    for item in delitems:
        try:
            header.remove(item)
        except:
            print("item ", item, ' not in the header')
    header.set('NAXIS', 2)
    header.add_history("Original Fits header processed by Leggo Builder")
    return header


def get_cube_slice(in_image, naxis3=None, naxis4=None, naxis5=None, hdr_no=0):
    fits_path = os.path.join(leggo_paths_settings.FILE_UPLOADS, in_image)

    data_cube = getdata(fits_path, hdr_no)
    if naxis5 is None:
        if naxis4 is None:
            if naxis3 is None:
                out_data = data_cube
            else:
                out_data = data_cube[naxis3, :, :]
        else:
            out_data = data_cube[naxis4, naxis3, :, :]
    else:
        out_data = data_cube[naxis5, naxis4, naxis3, :, :]

    return out_data


def write_fits_image(data, header, out_image):
    hdu_new = fits.PrimaryHDU(data)
    hdul = fits.HDUList([hdu_new])
    hdul[0].header = header
    hdul.writeto(out_image, overwrite=False)
