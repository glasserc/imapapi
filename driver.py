import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import imapapi.maildir

m = imapapi.maildir.Maildir("tmp/maildir")

mesg_id = m.deliver("test/corpus/0001.txt")

print m.count_messages(imapapi.UNREAD), m.count_messages(imapapi.READ), m.count_messages(imapapi.TOTAL)

mesg_id = m.mark_message(mesg_id, imapapi.READ)

print m.count_messages(imapapi.UNREAD), m.count_messages(imapapi.READ), m.count_messages(imapapi.TOTAL)

mesg_id = m.mark_message(mesg_id, imapapi.UNREAD)

print m.count_messages(imapapi.UNREAD), m.count_messages(imapapi.READ), m.count_messages(imapapi.TOTAL)

mesg_id = m.mark_message(mesg_id, imapapi.UNREAD)

print m.count_messages(imapapi.UNREAD), m.count_messages(imapapi.READ), m.count_messages(imapapi.TOTAL)

m.delete()
