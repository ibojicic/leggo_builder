from astropy.io import fits


def delete_extra_header(in_image, out_image=None, hdr_no=0):
    delete_items = ['CTYPE3', 'CRVAL3', 'CRPIX3', 'CDELT3', 'CUNIT3',
                    'CTYPE4', 'CRVAL4', 'CRPIX4', 'CDELT4', 'CUNIT4',
                    'NAXIS3', 'NAXIS4', 'CROTA3', 'CROTA4',
                    'PC3_1', 'PC4_1', 'PC3_2', 'PC4_2', 'PC1_3', 'PC2_3',
                    'PC3_3', 'PC4_3', 'PC1_4', 'PC2_4', 'PC3_4', 'PC4_4',
                    'PC03_01', 'PC04_01', 'PC03_02', 'PC04_02', 'PC01_03', 'PC02_03',
                    'PC03_03', 'PC04_03', 'PC01_04', 'PC02_04', 'PC03_04', 'PC04_04']
    hdu = fits.open(in_image)
    header = hdu[hdr_no].header
    data = hdu[hdr_no].data
    for item in delete_items:
        try:
            del header[item]
        except Exception:
            pass

    header['NAXIS'] = 2

    # data = data[0,0,:,:]
    data = data[:, :]

    hdu_new = fits.PrimaryHDU(data)
    hdul = fits.HDUList([hdu_new])
    hdul[0].header = header

    if out_image is None:
        hdul.writeto(in_image, overwrite=True)
    else:
        hdul.writeto(out_image, overwrite=True)
