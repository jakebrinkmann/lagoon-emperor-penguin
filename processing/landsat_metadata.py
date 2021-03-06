
'''
Description:  Provieds retrieval and modifications for the Landsat metadata.

License: NASA Open Source Agreement 1.3
'''

import os
import shutil
import glob
import logging
from cStringIO import StringIO

import settings


def fix_file(filename):
    """Fixes the MTL file

    Historical MTL files may contain binary data also somtimes the file names
    were generated incorrectly.  This methods fixes known issues and returns
    the correct filename to use.

    Args:
        filename (str): The MTL filename to fix.

    Returns:
        new_filename (str): The correct filename to use for the MTL data.
    """

    # Backup the original file
    backup_filename = ''.join([filename, '.old'])
    shutil.copy(filename, backup_filename)

    # Read in the file into a list
    file_data = list()
    with open(filename, 'r') as metadata_fd:
        file_data = metadata_fd.readlines()

    # The following process of writing the an IO buffer and then reading it
    # back as a string, will get rid of any binary characters at the end of
    # some of the metadata files
    data_buffer = StringIO()
    for line in file_data:
        data_buffer.write(line)
    fixed_data = data_buffer.getvalue()

    # Fix the stupid error where the filename has a bad extention
    new_name = filename
    if filename.endswith('.TIF'):
        new_name = filename.replace('.TIF', '.txt')

    # Write the newly formatted data out to the correct filename
    with open(new_name, 'w+') as metadata_fd:
        metadata_fd.write(fixed_data)

    # Remove backup filename
    os.unlink(backup_filename)

    # Report the correct filename back to the caller
    return new_name


def get_filename(work_dir, product_id):
    """Retrieve the Landsat metadata filename to use

    The file may have issues, so call the fix function to remove those issues.
    """
    try:
        parser = lambda x: 'old' not in x and not x.startswith('lnd')
        filename = filter(parser, glob.glob('{0}_MTL.*'.format(product_id))).pop()

        logging.debug('Located MTL file: [{0}]'.format(filename))

        filename = fix_file(filename)

        logging.info('Using MTL file: [{0}]'.format(filename))

    except IndexError:
        raise IOError('Unable to locate the MTL file in [{0}]'.format(work_dir))

    return filename
