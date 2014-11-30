
**************
SSH backend
**************



SSH
====

SSH (Secure SHell) is a network protocol which can be used to remotely log in a user into a device, it provides cryptographic communication between two networked hosts.


This backend provides access to remote device through SSH (Secure SHell).
Moreover SSH backend supports three main system:

 * AirOS
 * OpenWRT
 * Debian


AirOS example
=============

Here it is an example of how to import the SSH.AirOS backend, declare a device and invoke methods and properties on it::

 from netengine.backends.ssh import AirOS

Now we can invoke methods and properties by simply typing::


    device = AirOS('10.40.0.1', 'root', 'password')

    device.name
    'RM5PomeziaSNode'
    device.model
    'Rocket M5'
    device.os
    ('AirOS', 'XMar7240.v5.3.3.sdk.9634.1111221.2238')

    device.to_json()



OpenWRT example
================

Now we try to use OpenWRT instead of AirOS

::

 from netengine.backends.ssh import OpenWRT

 device = OpenWRT('10.177.8.100', 'root', 'password')

 device.name
 'owrt1'
 device.os
 '('OpenWrt', '12.09 (Attitude Adjustment 12.09, r36088)')'

 device.to_json()


Debian example
==============

Here an example using a Debian based linux distro::

  from netengine.backends.ssh import Debian

  device = Debian('10.177.8.100', 'ubuntu')

  print device
  '<SSH (Debian): 10.177.8.100>'
  print device.to_dict()
  'OrderedDict([('os_version', '14.04 (Ubuntu 14.04.1 LTS)'), ('uptime', 2077357), ('uptime_tuple', (24, 577, 34622)), ('name', 'ppp'), ('RAM_total', 2039000), ('antennas', []), ('os', 'Ubuntu'), ('interfaces', ['lo', 'p32p1', 'p33p1', 'p34p1', 'p35p1', 'p36p1', 'p37p1', 'br0']), ('type', 'server'), ('manufacturer', None)])'
