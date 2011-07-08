import imapapi.maildir

class TestMaildir():
    def setUp(self):
        self.m = imapapi.maildir.Maildir("tmp/maildir")

    def tearDown(self):
        self.m.delete()

    def get_message_counts(self):
        u = self.m.count_messages(imapapi.UNREAD)
        r = self.m.count_messages(imapapi.READ)
        t = self.m.count_messages(imapapi.TOTAL)
        return (u, r, t)

    def test_deliver(self):
        u, r, t = self.get_message_counts()
        assert t == r+u

        # New unread message
        mesg_id = self.m.deliver("test/corpus/0001.txt")
        assert (u+1, r, t+1) == self.get_message_counts()

        # Message is now read
        mesg_id = self.m.mark_message(mesg_id, imapapi.READ)
        assert (u, r+1, t+1) == self.get_message_counts()

        # Message is now unread again
        mesg_id = self.m.mark_message(mesg_id, imapapi.UNREAD)
        assert (u+1, r, t+1) == self.get_message_counts()

        # Double-marking a message is fine
        mesg_id = self.m.mark_message(mesg_id, imapapi.UNREAD)
        assert (u+1, r, t+1) == self.get_message_counts()
