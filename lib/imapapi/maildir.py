import os
import os.path
import shutil
import imapapi

class Maildir(imapapi.Mailbox):
    def __init__(self, path):
        self.path = path

        # Not sure about these; how should we be creating/tearing down?
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.create_folder()

    def create_folder(self, folder=None):
        """Create an empty Maildir structure in folder"""
        folder = folder or "INBOX"
        basedir = os.path.join(self.path, folder)

        for d in ['', 'cur', 'new', 'tmp']:
            if not os.path.exists(os.path.join(basedir, d)):
                os.mkdir(os.path.join(basedir, d))

    def delete(self):
        shutil.rmtree(self.path)

    def _list_messages(self, type, folder):
        if type == imapapi.READ:
            return self._list_messages_read(folder)

        elif type == imapapi.TOTAL:
            return self._list_messages_total(folder)

        else:
            return self._list_messages_unread(folder)

    def _list_messages_read(self, folder):
        # FIXME: is this true?
        # Read mails must have been processed by a MUA, ergo they must
        # be in "cur", and not "new"
        acc = []
        return [mail for mail in os.listdir(os.path.join(self.path, folder, "cur")) \
                    if mail.endswith("S")]

    def _list_messages_unread(self, folder):
        new = os.listdir(os.path.join(self.path, folder, "new"))
        cur = [mail for mail in os.listdir(os.path.join(self.path, folder, "cur")) \
                 if not mail.endswith("S")]
        return new + cur

    def _list_messages_total(self, folder):
        return os.listdir(os.path.join(self.path, folder, "new")) + \
            os.listdir(os.path.join(self.path, folder, "cur"))

    def _deliver(self, mesg, folder):
        basename = os.path.basename(mesg)
        # FIXME: Probably unsafe against concurrent access
        shutil.copy(mesg, os.path.join(self.path, folder, "new"))
        return basename

    def _mark_message(self, mesg, type, folder):
        fdir = os.path.join(self.path, folder)
        newsrc = os.path.join(fdir, "new", mesg)
        # FIXME: Probably could work based on presence of :2, in filename
        if os.path.exists(newsrc):
            if type == imapapi.UNREAD:
                # no need to mark it unread; it's already in "new"
                return mesg

            # move it to cur
            curdest = os.path.join(fdir, "cur", mesg + ":2,")
            shutil.move(newsrc, curdest)
            mesg = mesg + ":2,"

        mesgbase, mesgflags = mesg.split(":2,")
        if type == imapapi.READ:
            if "S" in mesgflags:
                # Already read
                return mesg
            mesgflags = mesgflags + "S"

        if type == imapapi.UNREAD:
            if "S" not in mesgflags:
                # Already unread
                return mesg
            mesgflags = mesgflags.replace("S", "")

        newmesg = mesgbase + ":2," + mesgflags
        cursrc = os.path.join(fdir, "cur", mesg)
        curdest = os.path.join(fdir, "cur", newmesg)
        shutil.move(cursrc, curdest)
        return newmesg
