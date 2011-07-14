import os.path
import imapapi

TESTDIR = os.path.dirname(__file__)
CORPUSDIR = os.path.join(TESTDIR, "corpus")


class ImapApiTest():
    def get_message_counts(self, maildir):
        u = maildir.count_messages(imapapi.UNREAD)
        r = maildir.count_messages(imapapi.READ)
        t = maildir.count_messages(imapapi.TOTAL)
        return (u, r, t)

    def corpus(self, fname):
        '''Returns the absolute filename of the corpus message specified by fname.

        E.g. self.corpus("0001.txt") -> "/home/ethan/src/imapapi.git/test/corpus/0001.txt"'''
        return os.path.join(CORPUSDIR, fname)
