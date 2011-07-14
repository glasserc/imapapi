import os.path
import subprocess
import ConfigParser
from test import ImapApiTest

imapapi_config = ConfigParser.SafeConfigParser()
# FIXME: more general?
imapapi_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
imapapi_config.read(os.path.join(imapapi_dir, "imapapi.conf"))

# FIXME: Try using which() first?
OFFLINEIMAPDIR = os.path.expanduser(imapapi_config.get("Paths", "offlineimap"))
OFFLINEIMAP = os.path.join(OFFLINEIMAPDIR, "offlineimap.py")

class OfflineImapTest(ImapApiTest):
    def __init__(self):
        # FIXME: all these paths need to get straightened out.
        # Every test should have its own "chroot"?
        self.mailboxes = {}
        self.config = ConfigParser.SafeConfigParser()
        self.config.add_section("general")
        self.config.set("general", "metadata", "tmp/offlineimap-meta")
        self.config.set("general", "accounts", "Test")
        self.config.set("general", "ui", "Basic")

        self.config.add_section("Account Test")
        self.config.set("Account Test", "localrepository", "Local")
        self.config.set("Account Test", "remoterepository", "Remote")

        self.config.add_section("Repository Local")
        self.config.set("Repository Local", "type", "Maildir")
        # FIXME: should be based on test information
        self.config.set("Repository Local", "localfolders", os.path.abspath("tmp/offlineimap-maildir/"))

        self.config.add_section("Repository Remote")
        self.config.set("Repository Remote", "type", "IMAP")
        self.config.set("Repository Remote", "remotehost", "localhost")
        self.config.set("Repository Remote", "remoteport", "10143")
        self.config.set("Repository Remote", "remoteuser", "testuser")
        self.config.set("Repository Remote", "remotepass", "testpass")

        self.conffile = "tmp/offlineimap.conf"

    def run_offlineimap(self, *args):
        # Ensure config has been generated
        self.generate_conf()
        return subprocess.check_call(["offlineimap", "-c", self.conffile],
                                     executable=OFFLINEIMAP)

    def generate_conf(self):
        self.config.write(file(self.conffile, "w"))

    def will_sync(self, local, remote):
        # FIXME: this should somehow do something with the sections of
        # the conf file that are getting written out, store paths,
        # create an Account, etc.
        pass
