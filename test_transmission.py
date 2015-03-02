import unittest
from transmissionapi import TransmissionDaemon
from transmissionapi import Torrent

class  TestTransmission(unittest.TestCase):

    def test_init(self):
        daemon = TransmissionDaemon(host='192.168.1.12')
        self.assertEqual(daemon.host, '192.168.1.12')
        self.assertEqual(daemon.port, '9091')

    def test_add_torrent(self):
        daemon = TransmissionDaemon(host='192.168.1.12')
        torrent = Torrent('http://sample-file.bazadanni.com/download/applications/torrent/sample.torrent')
        response = daemon.add_torrent(torrent)
        self.assertEqual(response['result'], 'success')




if __name__ == '__main__':
    unittest.main()
