from test import ImapApiTest

class TestOfflineImap(ImapApiTest):
    def __init__(self):
        self.mailboxes = {}

    def run_offlineimap(self):
        pass

    def will_sync(self, local, remote):
        pass
