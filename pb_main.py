import sys
import os
import pb_apps as apps

from pb_const import *

#---------------------------------------------------------------------
# MAIN FUNCTION
#---------------------------------------------------------------------
def main():
    mode = 0
    for argc in sys.argv:
        opt = argc.split('=')
        if opt[0] == '--mode' and len(opt) == 2:
            mode = int(opt[1])

    appl = apps.PB_Application()
    appl.run(mode)
    
#---------------------------------------------------------------------
# RUN MAIN FUNCTION
#---------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())

