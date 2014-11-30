"""
Class to extract information from Debian/Ubuntu based devices
"""

__all__ = ['Debian']


from netengine.backends.ssh import SSH
import json


class Debian(SSH):
    """
    Debian SSH backend
    """

    def __str__(self):
        """ print a human readable object description """
        return u"<SSH (Debian): %s@%s>" % (self.username, self.host)

    @property
    def name(self):
        """ get device name """
        return self.run('uname -a').split(' ')[1]

    @property
    def os(self):
        """ get os name and version, return as tuple """
        # cache command output
        output = self.run('cat /etc/lsb-release')
        # init empty dict
        info = {}

        # loop over lines of output
        # parse output and store in python dict
        for line in output.split('\n'):
            # tidy up before filling the dictionary
            key, value = line.split('=')
            key = key.replace('DISTRIB_', '').lower()
            value = value.replace('"', '')
            # fill!
            info[key] = value

        os = info['id']
        version = info['release']

        if info.get('description'):
            if info.get('revision'):
                additional_info = "%(description)s, %(revision)s" % info
            else:
                additional_info = "%(description)s" % info
            # remove redundant Debian occuerrence
            additional_info = additional_info.replace('Debian ', '')
            version = "%s (%s)" % (version, additional_info)
        return (os, version)

    @property
    def interfaces_to_dict(self):
        out = self.run("ip link | grep '^[0-9]' | cut -d : -f 2 | tr -d ' ':")
        ifaces = []
        for line in out.split('\n'):
            ifaces.append(line)
        return ifaces

    @property
    def RAM_total(self):
        return int(self.run("cat /proc/meminfo | grep MemTotal | awk '{print $2}'"))

    @property
    def uptime(self):
        """
        returns an integer representing the number of seconds of uptime
        """
        output = self.run('cat /proc/uptime')
        seconds = float(output.split()[0])
        return int(seconds)

    @property
    def manufacturer(self):
        """
        returns a string representing the manufacturer of the device
        """
        return None
        # returns first not None value
        for interface in self.ubus_dict.keys(): #FIXME
            # ignore loopback interface
            if interface != "lo":
                mac_address = self.ubus_dict[interface]['macaddr']
                manufacturer = self.get_manufacturer(mac_address)
                if manufacturer:
                    return manufacturer

    @property
    def uptime_tuple(self):
        """
        Return a tuple (days, hours, minutes)
        """
        uptime = float(self.run('cat /proc/uptime').split()[0])
        seconds = int(uptime)
        minutes = int(seconds // 60)
        hours = int(minutes // 60)
        days = int(hours // 24)
        output = days, hours, minutes
        return output

    def to_dict(self):
        return self._dict({
            "name": self.name,
            "type": "server",
            "os": self.os[0],
            "os_version": self.os[1],
            "manufacturer": self.manufacturer,
            "RAM_total": self.RAM_total,
            "uptime": self.uptime,
            "uptime_tuple": self.uptime_tuple,
            "interfaces": self.interfaces_to_dict,
            "antennas": [],
        })
