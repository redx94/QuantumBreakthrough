#!/usr/bin/env python
# Logger utility

import logging

def setup_logger(name):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)

if __name__ == "__main__":
    print("Logger module activated.")
