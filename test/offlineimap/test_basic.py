import imapapi.maildir
import imapapi.dovecot
from test.offlineimap import OfflineImapTest

class TestBasic(OfflineImapTest):
    def setUp(self):
        self.local = imapapi.maildir.Maildir("tmp/maildir")
        # FIXME: how do we insist on starting 'fresh'?
        # If we delete in the tear-down, we can't inspect the results
        # of the test.  But if we delete it here, we really have to
        # create it twice.
        self.remote = imapapi.dovecot.Dovecot("tmp/dovecot-basic")
        self.remote.delete()
        self.remote = imapapi.dovecot.Dovecot("tmp/dovecot-basic")
        self.remote.start_server()

    def tearDown(self):
        self.remote.stop_server()

    def test_sync(self):
        assert (0, 0, 0) == self.get_message_counts(self.local)
        assert (0, 0, 0) == self.get_message_counts(self.remote)

        self.remote.deliver(self.corpus("0001.txt"))
        assert (1, 0, 1) == self.get_message_counts(self.remote)

        self.will_sync(self.local, self.remote)
        self.run_offlineimap()

        assert (1, 0, 1) == self.get_message_counts(self.local), "OfflineIMAP didn't copy messages"

        # Check that reading the message locally syncs back this status
        unread_id = self.local.list_messages(imapapi.UNREAD)[0]

        self.local.mark_message(unread_id, imapapi.READ)
        assert (0, 1, 1) == self.get_message_counts(self.local) # sanity check


        self.run_offlineimap()
        assert (0, 1, 1) == self.get_message_counts(self.remote), "OfflineIMAP didn't sync read status"
