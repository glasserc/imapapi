from test import ImapApiTest
import imapapi.maildir

class TestMaildir(ImapApiTest):
    def setUp(self):
        self.m = imapapi.maildir.Maildir("tmp/maildir")

    def tearDown(self):
        self.m.delete()

    def test_deliver(self):
        u, r, t = self.get_message_counts(self.m)
        assert t == r+u

        # New unread message
        mesg_id = self.m.deliver("test/corpus/0001.txt")
        assert (u+1, r, t+1) == self.get_message_counts(self.m)

        # Message is now read
        mesg_id = self.m.mark_message(mesg_id, imapapi.READ)
        assert (u, r+1, t+1) == self.get_message_counts(self.m)

        # Message is now unread again
        mesg_id = self.m.mark_message(mesg_id, imapapi.UNREAD)
        assert (u+1, r, t+1) == self.get_message_counts(self.m)

        # Double-marking a message is fine
        mesg_id = self.m.mark_message(mesg_id, imapapi.UNREAD)
        assert (u+1, r, t+1) == self.get_message_counts(self.m)
