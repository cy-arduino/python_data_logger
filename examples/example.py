#!/usr/bin/env python

import os
import logging
from datetime import datetime

from datalogger import Logger, BgMonitor, Column

if __name__ == '__main__':
    LOG_FMT = "%(asctime)s [%(levelname)s] " \
              "%(filename)s:%(lineno)s %(name)s %(funcName)s() : %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FMT)

    log_path = './log_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    try:
        os.makedirs(log_path)
    except FileExistsError:
        pass


    monitors = []
    monitors.append(
        BgMonitor('top', 'top -b -d 1', log_path + '/top.log'))

    columns = []
    columns.append(Column('mem total', Column.ACTION_CMD,
                          cmd="free -m | grep Mem | awk '{{print $2}}'"))

    columns.append(Column('mem used', Column.ACTION_CMD,
                          cmd="free -m | grep Mem | awk '{{print $3}}'"))

    logger = Logger('logger', columns=columns, bg_monitors=monitors,
                    log_path=log_path, interval=1, timeout=100)
    logger.start()
