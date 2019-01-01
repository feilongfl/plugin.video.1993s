#!/usr/bin/env python

import decode
import sys

code = sys.argv[-1]
print(decode.var['decode'](code))
