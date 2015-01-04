ubnt_airos
==========

This is a collection of scripts that I am using to communicate with AirOS devices, specifically Nanostations, from the awesome Ubiquiti Networks.

Requirements
------------
```
sudo pip install requests json argparse
```

Exection
--------
```
python get_status.py -u ubnt -p ubnt 192.168.0.20
```

This will dump out the basic JSON contents of status.cgi.

More to come!!

ubnt_info CollectD plugin
=========================

Values presently captured:
* signal
* txrate
* rxrate
* distance
* noisef
* rssi
* uptime
* polling_capacity
* polling_quality

collectd config file
--------------------
- Check out this repo somewhere, this example assumes /opt/ubnt_airos.
- Copy the config into /etc/collectd.d/ubnt.conf (or appropriate)
- Update the ModulePath value below.

```
<LoadPlugin python>
    Globals true
</LoadPlugin>

<Plugin python>
    ModulePath "/opt/ubnt_airos"
    LogTraces true
    Interactive true
    Import "ubnt_collectd"
    <Module "ubnt_collectd">
        <Device>
            Host "10.0.0.2"
            User "ubnt"
            Pass "ubnt"
        </Device>
        <Device>
            Host "10.0.0.3"
            User "ubnt"
            Pass "ubnt"
        </Device>
        <Device>
            Host "10.0.0.4"
            User "ubnt"
            Pass "ubnt"
        </Device>
    </Module>
</Plugin>
```

Grafana config
--------------
I use InfluxDB and my Metrics config point to something like 10_0_0_2.ubnt_info.gauge.signal.
