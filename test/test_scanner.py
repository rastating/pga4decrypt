import sqlite3
import unittest

from lib.scanner import read_servers
from lib.scanner import decrypt_password
from lib.scanner import read_and_decrypt_servers

from unittest.mock import MagicMock, patch

class TestReadServers(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect('test/pgadmin4.db')

    def test_returns_each_row(self):
        servers = read_servers(self.db)
        self.assertTrue(len(servers) == 3)

    def test_includes_server_name(self):
        servers = read_servers(self.db)
        self.assertEqual(servers[0]['name'], 'Server 2')
        self.assertEqual(servers[1]['name'], 'Server 3')
        self.assertEqual(servers[2]['name'], 'Server 1')

    def test_includes_host(self):
        servers = read_servers(self.db)
        self.assertEqual(servers[0]['host'], '10.8.0.101')
        self.assertEqual(servers[1]['host'], '10.8.0.102')
        self.assertEqual(servers[2]['host'], '10.8.0.100')

    def test_includes_port(self):
        servers = read_servers(self.db)
        self.assertEqual(servers[0]['port'], 5432)
        self.assertEqual(servers[1]['port'], 5432)
        self.assertEqual(servers[2]['port'], 5432)

    def test_includes_username(self):
        servers = read_servers(self.db)
        self.assertEqual(servers[0]['username'], 'billy')
        self.assertEqual(servers[1]['username'], 'billy')
        self.assertEqual(servers[2]['username'], 'alice')

    def test_includes_encrypted_password(self):
        servers = read_servers(self.db)
        self.assertEqual(servers[0]['password'], 'qJ6xh7QrKXqbFfG0mek7k+jgiUGRSxHumFQrh0w+UChOT10JQ55k7P3g4KSgQkYYt6KD+DSWQw==')
        self.assertEqual(servers[1]['password'], '0SYeawiDClt4BtXASH9V2ks/xBa4Yw==')
        self.assertEqual(servers[2]['password'], 'zozz+iek61AC1khxnPWxvtzRZUUSuy7dzJEQMwhalA==')

    def test_includes_encryption_key(self):
        servers = read_servers(self.db)
        self.assertEqual(servers[0]['key'], '$pbkdf2-sha512$25000$yVlL6X3POWdM6d1bC6F0bg$wYXYXkIuTYw4fxauhI1bliCEHxOCm/wJYd6hW9fwhbaC/8Z6lMQySVNdPaOlsgfWFdOUIChdxhCs6i0Uj4mt5g')
        self.assertEqual(servers[1]['key'], '$pbkdf2-sha512$25000$yVlL6X3POWdM6d1bC6F0bg$wYXYXkIuTYw4fxauhI1bliCEHxOCm/wJYd6hW9fwhbaC/8Z6lMQySVNdPaOlsgfWFdOUIChdxhCs6i0Uj4mt5g')
        self.assertEqual(servers[2]['key'], '$pbkdf2-sha512$25000$ldI6p/R.7/2/F6K0FqK0tg$hMWW4TItRAHnBBmXuTtajBQ9ffkZnaI6LPTRGkQjJdj2zvzccF.6kZIqBTDCyvqCvL50ClsdKWPRtV1BFEBWuA')

class TestDecryptPassword(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect('test/pgadmin4.db')

    def test_decrypts_the_server_password(self):
        servers = read_servers(self.db)
        self.assertEqual(decrypt_password(servers[0]), 'DespiteAllMyRageIAmStillJustARatInACage')
        self.assertEqual(decrypt_password(servers[1]), 'iamone')
        self.assertEqual(decrypt_password(servers[2]), 'GetOutOfMySwamp')

class TestReadAndDecryptServers(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect('test/pgadmin4.db')
        self.unreadable_server = {}
        self.unreadable_server['name'] = 'name'
        self.unreadable_server['host'] = '127.0.0.1'
        self.unreadable_server['port'] = 1234
        self.unreadable_server['username'] = 'sa'
        self.unreadable_server['password'] = ''
        self.unreadable_server['key'] = 'a'

    @patch('lib.scanner.read_servers')
    def test_returns_all_servers_that_can_be_decrypted(self, read_mock):
        servers = read_servers(self.db)
        servers.append(self.unreadable_server)
        self.assertEqual(len(servers), 4)

        read_mock.return_value = servers
        result = read_and_decrypt_servers(self.db)
        self.assertEqual(len(result), 3)

    def test_includes_server_name(self):
        servers = read_and_decrypt_servers(self.db)
        self.assertEqual(servers[0]['name'], 'Server 2')
        self.assertEqual(servers[1]['name'], 'Server 3')
        self.assertEqual(servers[2]['name'], 'Server 1')

    def test_includes_host(self):
        servers = read_and_decrypt_servers(self.db)
        self.assertEqual(servers[0]['host'], '10.8.0.101')
        self.assertEqual(servers[1]['host'], '10.8.0.102')
        self.assertEqual(servers[2]['host'], '10.8.0.100')

    def test_includes_port(self):
        servers = read_and_decrypt_servers(self.db)
        self.assertEqual(servers[0]['port'], 5432)
        self.assertEqual(servers[1]['port'], 5432)
        self.assertEqual(servers[2]['port'], 5432)

    def test_includes_username(self):
        servers = read_and_decrypt_servers(self.db)
        self.assertEqual(servers[0]['username'], 'billy')
        self.assertEqual(servers[1]['username'], 'billy')
        self.assertEqual(servers[2]['username'], 'alice')

    def test_includes_decrypted_password(self):
        servers = read_and_decrypt_servers(self.db)
        self.assertEqual(servers[0]['password'], 'DespiteAllMyRageIAmStillJustARatInACage')
        self.assertEqual(servers[1]['password'], 'iamone')
        self.assertEqual(servers[2]['password'], 'GetOutOfMySwamp')
