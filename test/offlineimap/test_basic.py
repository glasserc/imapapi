import os.path
import shutil
import imapapi.maildir
import imapapi.dovecot
from test.offlineimap import OfflineImapTest

class TestBasic(OfflineImapTest):
    def setUp(self):
        self.local = imapapi.maildir.Maildir.fresh("tmp/offlineimap-maildir")
        self.remote = imapapi.dovecot.Dovecot.fresh("tmp/offlineimap-dovecot")
        self.remote.start_server()

    def tearDown(self):
        self.remote.stop_server()
        if os.path.exists("tmp/offlineimap-meta"):
            shutil.rmtree("tmp/offlineimap-meta")
        # FIXME: it's like I forgot Python???
        #super(TestBasic, self).tearDown()

    def test_sync(self):
        assert (0, 0, 0) == self.get_message_counts(self.local)
        assert (0, 0, 0) == self.get_message_counts(self.remote)

        self.remote.deliver(self.corpus("0001.txt"))
        assert (1, 0, 1) == self.get_message_counts(self.remote)

        self.will_sync(self.local, self.remote)
        self.run_offlineimap()

        assert (1, 0, 1) == self.get_message_counts(self.local), "OfflineIMAP didn't copy messages"

        # Check that offlineimap syncs back "read" status
        unread_id = self.local.list_messages(imapapi.UNREAD)[0]

        self.local.mark_message(unread_id, imapapi.READ)
        assert (0, 1, 1) == self.get_message_counts(self.local) # sanity check


        self.run_offlineimap()
        assert (0, 1, 1) == self.get_message_counts(self.remote), "OfflineIMAP didn't sync read status"
