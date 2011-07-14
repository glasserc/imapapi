import os.path
import subprocess
import ConfigParser
from test import ImapApiTest

imapapi_config = ConfigParser.SafeConfigParser()
# FIXME: more general?
imapapi_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
imapapi_config.read(os.path.join(imapapi_dir, "imapapi.conf"))

# FIXME: Try using which() first?
OFFLINEIMAPDIR = imapapi_config.get("Paths", "offlineimap")
OFFLINEIMAP = os.path.join(OFFLINEIMAPDIR, "offlineimap.py")

class OfflineImapTest(ImapApiTest):
    def __init__(self):
        self.mailboxes = {}
        self.conffile = ""

    def run_offlineimap(self, *args):
        print "Running offlineimap at {0}".format(OFFLINEIMAP)
        return subprocess.check_process("offlineimap", "-c",
                                        self.conffile, executable=OFFLINEIMAP)

    def generate_conf(self):
        pass

    def will_sync(self, local, remote):
        pass
