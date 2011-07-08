import time
import socket
import imapapi.dovecot

dovecot = imapapi.dovecot.Dovecot("tmp/dovecot")

def tearDown():
    #dovecot.delete()
    pass

class TestDovecot():
    def setUp(self):
        dovecot.start_server()

    def tearDown(self):
        dovecot.stop_server()

    def test_server(self):
        # dovecot takes a second to grab the socket
        time.sleep(1)

        # If you want to see the output, run with nosetests -s

        # http://documents.made-it.com/imapcmd.html
        sock = socket.create_connection(("localhost", 10143))
        hello = sock.recv(4096)
        print "!" + hello + "!"
        assert hello.startswith("* OK")
        assert hello.endswith("Dovecot ready.\r\n")

        sock.send("01 LOGIN testuser testpass\r\n")
        login = sock.recv(4096)
        print "@" + login + "@"
        assert login.startswith("01 OK")
        assert login.endswith("Logged in\r\n")

        sock.send('02 LIST "" *\r\n')
        mailboxes = sock.recv(4096)
        print "#" + mailboxes + "#"
        assert '"INBOX"' in mailboxes
        assert mailboxes.endswith("02 OK List completed.\r\n")
