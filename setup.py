from distutils.core import setup
import glob
import py2exe

setup(
        console=['run.py'],windows=['run.py'],
        data_files=[('media',
                      glob.glob('media/*')),
		    ('animals',
		      glob.glob('animals/*.py')),
		   ],
    )

