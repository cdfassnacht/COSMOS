"""
Takes LCOGT files and adds the OBJCTRA and OBJCTDEC keywords so that
they can be used by CCDSoft.

Usage: python lcogt_to_ccdsoft.py [directory_name]

  e.g., python lcogt_to_ccdsoft.py sdss_r_band
"""

import sys
import pyfits as pf
import glob

""" Check command line syntax"""

if len(sys.argv)<2:
    print ''
    print 'ERROR.  This script requires one input parameter'
    print '    1. Name of directory containing files to be modified'
    print ''
    print 'Example:  python kait_to_ccdsoft.py V_band'
    print ''
    exit()

""" Get list of input files """
inlist = glob.glob('%s/*' % sys.argv[1])
nfiles = len(inlist)
print ''
print 'Found %d input files' % nfiles

""" Loop through input files and add the headers needed for CCDSoft """
for i in range(nfiles):
    print ''
    try:
        hdu = pf.open(inlist[i],mode='update')
    except:
        print 'ERROR: Could not open %s' % inlist[i]
        print ''
        exit()
    print '%s' % inlist[i]
    hdr = hdu[0].header

    """ Set the OBJCTRA keyword """
    try:
        rastr0 = hdr['ra']
    except:
        print ''
        print 'ERROR: Cannot open RA keyword'
        print ''
        exit()
    ra1,ra2,ra3 = rastr0.split(':')
    ra3f = float(ra3)
    rastr = '%s:%s:%05.2f' % (ra1,ra2,ra3f)

    try:
        hdr['objctra'] = rastr
    except:
        try:
            hdr.update('objctra',rastr)
        except:
            print ''
            print 'ERROR: Could not create OBJCTRA keyword'
            print ''
            exit()
    print 'OBJCTRA = %s' % hdr['objctra']

    """ Set the OBJCTDEC keyword """
    try:
        hdr['objctdec'] = hdr['dec']
    except:
        try:
            hdr.update('objctdec',hdr['dec'])
        except:
            print ''
            print 'ERROR: Could not create OBJCTDEC keyword'
            print ''
            exit()
    print 'OBJCTDEC = %s' % hdr['objctdec']

    """ Clean up """
    hdu.flush()
    del hdu



