import os.path
libdir = os.path.dirname(os.path.dirname(__file__))
# FIXME: more general???
sharedir = os.path.join(os.path.dirname(libdir), "share")

class MessageSearch(object):
    pass

class READ(MessageSearch):
    pass

class UNREAD(MessageSearch):
    pass

class TOTAL(MessageSearch):
    pass

class Mailbox(object):
    """A container that stores mail.

    A Mailbox can have folders.  Most methods take an optional folder
    argument.  If folder is None, default to 'inbox'.

    Subclasses should override _list_messages(), _deliver(), and
    _mark_message().  Override _count_messages if it's possible to do
    more efficiently.
    """

    def __init__(self):
        pass

    def count_messages(self, type, folder=None):
        """Count messages of type (READ, UNREAD) in the folder :argument:`folder`, or Inbox if None."""
        return self._count_messages(type, folder or "Inbox")

    def _count_messages(self, type, folder):
        return len(self.list_messages(type, folder))

    def list_messages(self, type, folder=None):
        """Return message IDs matching the type in the folder."""
        return self._list_messages(type, folder or "Inbox")

    def _list_messages(self, type, folder):
        raise NotImplementedYet

    def deliver(self, mesg, folder=None):
        """mesg is either a file-like object which will be read, or a filename.

        Return a message ID."""
        return self._deliver(mesg, folder or "Inbox")

    def _deliver(self, mesg, folder):
        raise NotImplementedYet

    def mark_message(self, message_id, type, folder=None):
        """Mark a message as READ or UNREAD.  message_id is presumed to be a message in folder.

        Return a new message id?"""
        return self._mark_message(message_id, type, folder or "Inbox")

    def _mark_message(self, message_id, type, folder):
        raise NotImplementedYet
