import unittest
import MockSSH

from netengine.backends.ssh import OpenWRT

from ..settings import settings

from mock_openwrt import commands

from twisted.internet import reactor

__all__ = ['TestSSHOpenWRT']


class TestSSHOpenWRT(unittest.TestCase):

    _thread = None
    
    @classmethod
    def setUpClass(cls):
        users = {'root': 'password'}
        cls._thread = MockSSH.threadedServer(commands,
                prompt="$",
                interface="localhost",
                port=9856,
                **users)

    @classmethod
    def tearDownClass(cls):
        reactor.callFromThread(reactor.stop)


    def setUp(self):
        self.host = settings['openwrt-ssh']['host']
        self.username = settings['openwrt-ssh']['username']
        self.password = settings['openwrt-ssh']['password']
        self.port = settings['openwrt-ssh'].get('port', 22)

        self.device = OpenWRT(self.host, self.username, self.password, self.port)
        self.device.connect()
    
    def test_properties(self):
        device = self.device
        
        device.os
        device.name
        device.olsr
        device.disconnect()
    
#    def test_wireless_mode(self):
#        self.assertTrue(self.device.wireless_mode in ['ap', 'sta'])
        
    def test_RAM_total(self):
        self.assertTrue(type(self.device.RAM_total) == int)

    def test_uptime(self):
        self.assertTrue(type(self.device.uptime) == int)
    
    def test_interfaces_to_dict(self):
        self.assertTrue(type(self.device.interfaces_to_dict) == dict)

    def test_uptime_tuple(self):
        self.assertTrue(type(self.device.uptime_tuple) == tuple)
    
    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))

    def test_filter_radio_interfaces(self):
        self.assertTrue(isinstance(self.device._filter_radio_interfaces(), dict))
    
    def test_filter_radio(self):
        self.assertTrue(isinstance(self.device._filter_radio(), dict))
    
    def test_manufacturer(self):
        self.assertTrue(type(self.device.manufacturer) == str)

    def test_filter_routing_protocols(self):
        self.assertTrue(isinstance(self.device._filter_routing_protocols(), list))
