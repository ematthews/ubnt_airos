#!/usr/bin/env python

# The following scripts are based quite heavily on existing modules for
# collectd, so thank you to these folks for using GitHub!
#   Redis: https://github.com/powdahound/redis-collectd-plugin/blob/master/redis_info.py
#   Monitis: https://github.com/monitisexchange/Python-SDK/blob/master/monitis/tools/collectd_monitis/monitis_writer.py
# 
# And of course, the CollectD Python documentation at:
#   http://collectd.org/documentation/manpages/collectd-python.5.shtml#examples

import collectd
from airos import AirOS

devices = dict()
default_host = {
    'host': None,
    'user': 'ubnt',
    'pass': 'ubnt'
}
VERBOSE_LOGGING = False

def fetch_info(host, username, password):
    """ Connect to UBNT device and request info. """
    try:
        station = AirOS(host=host, username=username, password=password)
    except:
        collectd.error('ubnt_info plugin: Error connecting to %s' % (host))

    try:
        status = station.status
    except:
        collectd.error('ubnt_info plugin: Unable to read status from %s' % (host))

    return status

def configure_callback(conf):
    """ Receive configuration block """
#    global UBNT_HOST, UBNT_USER, UBNT_PASS
    global devices

    for node in conf.children:
        if node.key == 'Device':
            for child in node.children:
                if child.key == 'Host':
                    device_host = child.values[0]
                elif child.key == 'User':
                    device_user = child.values[0]
                elif child.key == 'Pass':
                    device_pass = child.values[0]

            devices[device_host] = default_host.copy()
            devices[device_host]['host'] = device_host
            devices[device_host]['user'] = device_user
            devices[device_host]['pass'] = device_pass

def dispatch_value(hostname, type, value, type_instance=None):
    if value is None:
        collectd.warning('ubnt_info plugin: Info key not found %s' % key)
        return

    if not type_instance:
        type_instance = key

    log_verbose('Sending value %s=%s' % (type_instance, value))

    val = collectd.Values(plugin='ubnt_info')
    val.host = hostname
    val.type = type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()

    return

def read_callback():
    log_verbose("UBNT read callback called.")
    for device in devices.keys():
        log_verbose("Connecting to %s" % device)
        info = fetch_info(devices[device]['host'], devices[device]['user'], devices[device]['pass'])

        if not info:
            collectd.error('ubnt_info: No info received from %s' % device['host'])
            return

        dispatch_value(device, 'gauge', info['wireless']['signal'], 'signal')
        dispatch_value(device, 'gauge', info['wireless']['txrate'], 'txrate')
        dispatch_value(device, 'gauge', info['wireless']['rxrate'], 'rxrate')
        dispatch_value(device, 'gauge', info['wireless']['distance'], 'distance')
        dispatch_value(device, 'gauge', info['wireless']['noisef'], 'noisef')
        dispatch_value(device, 'gauge', info['wireless']['rssi'], 'rssi')
        dispatch_value(device, 'gauge', info['host']['uptime'], 'uptime')
        dispatch_value(device, 'gauge', info['wireless']['polling']['capacity'], 'polling_capacity')
        dispatch_value(device, 'gauge', info['wireless']['polling']['quality'], 'polling_quality')
        log_verbose("Finished with %s" % device)

def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('ubnt_info [verbose]: %s' % msg)

collectd.register_config(configure_callback)
collectd.register_read(read_callback)
