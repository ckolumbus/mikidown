#!/usr/bin/env python3

# http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import sys
import logging
import mikidown

# Check the python version
try:
    version_info = sys.version_info
    assert version_info > (3, 0)
except:
    #print('ERROR: mikidown needs python >= 3.0', file=sys.stderr)
    #sys.exit(1)
    pass

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
