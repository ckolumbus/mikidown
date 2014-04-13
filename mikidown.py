#!/usr/bin/env python3

import sys
import logging
import mikidown

# Check the python version
try:
    version_info = sys.version_info
    assert version_info > (3, 0)
except:
    print('ERROR: mikidown needs python >= 3.0', file=sys.stderr)
    sys.exit(1)

# Run mikidown
try:
    logging.basicConfig(filename='mikidown.log', level=logging.DEBUG)
    logging.debug('Started')
    mikidown.main()
    logging.debug('Finished')

except KeyboardInterrupt:
    print('Interrupt', file=sys.stderr)
    sys.exit(1)
else:
    sys.exit(0)
