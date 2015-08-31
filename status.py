#!/usr/bin/env python3
from SetupDreamland import configs
import multiSSH

if __name__ == "__main__":
    s = multiSSH.MultiDreamandPi(configs)
    s.ping()
    print('Finished setup run.')
