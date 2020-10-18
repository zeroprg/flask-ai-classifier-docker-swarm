import os
import logging
import argparse

LOG = logging.getLogger("classifier-api.error")

def configure(FILE):
    # construct the argument parse and parse the arguments
    # I named config file as  file config.txt and stored it
    # in the same directory as the script
    separator = '='
    args = {}
    with open(FILE) as f:
        for line in f:
            if separator in line:
                # Find the name and value by splitting the string
                name, value = line.split(separator, 1)
                # Assign key value pair to dict
                # strip() removes white space from the ends of strings
                args[name.strip()] = value.strip()
    
    LOG.debug(args)
    if("ipaddress" in args.keys() ):
         ipaddress =  args["ipaddress"]
         LOG.info('DB ip address:' + ipaddress )
    return args     