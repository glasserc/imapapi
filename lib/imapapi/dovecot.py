import os.path
import subprocess
import shutil
import grp
import imapapi.maildir
import imapapi.utils

# Path to the dovecot executable.
DOVECOT=imapapi.utils.which("dovecot")
if not DOVECOT: DOVECOT = "/usr/sbin/dovecot"
if not imapapi.utils.is_exe(DOVECOT):
    raise RuntimeError, """dovecot could not be found on this machine.

At present, dovecot is required in order to run tests."""

class Dovecot(imapapi.maildir.Maildir):
    """Sets up a 'rootless' dovecot instance in serverpath.  Mail will be kept in a maildir serverpath/mail.

    You can start and stop dovecot's IMAP interface with start_server
    and stop_server.  IMAP will run on port 10143 as testuser/testpass."""
    def __init__(self, serverpath):
        self.serverpath = serverpath
        # Use real-dovecot.conf because dovecot puts a symlink in dovecot.conf
        self.conf = os.path.join(self.serverpath, "real-dovecot.conf")
        self.server = None
        if not os.path.exists(self.serverpath):
            os.mkdir(self.serverpath)
            self.write_config()

        super(Dovecot, self).__init__(os.path.join(serverpath, "mail"))

    def _list_messages(self, type, folder):
        "Dovecot doesn't actually use a folder called Inbox; instead it just reads/writes to the mail directory."
        newf = folder
        if newf == "INBOX": newf = ""
        return super(Dovecot, self)._list_messages(type, newf)

    def create_folder(self, folder="."):
        "Provide a different default argument (as above)"
        return super(Dovecot, self).create_folder(folder)

    def write_config(self):
        group = grp.getgrgid(os.getgid())
        serverpath = os.path.abspath(self.serverpath)

        imapapi.utils.fill_template(os.path.join(imapapi.sharedir, "dovecot.conf.template"),
                                    self.conf, {
                "MAIL_LOCATION": "maildir:"+os.path.join(serverpath, "mail"),
                "WHOAMI_GROUP_ID": str(os.getgid()),
                "WHOAMI_ID": str(os.getuid()),
                "WHOAMI_GROUP": group.gr_name,
                "WHOAMI": os.getlogin(),
                "DOVECOTDIR": serverpath,
                })

        shutil.copy(os.path.join(imapapi.sharedir, "passwd"), self.serverpath)

    def start_server(self):
        self.server = subprocess.Popen(["dovecot", "-F", "-c", self.conf], executable=DOVECOT)

    def stop_server(self):
        if not self.server: return
        subprocess.check_call(["kill", str(self.server.pid)])
        self.server = None

    def _deliver(self, mesg, folder):
        # FIXME: pass via stdin too?
        subprocess.check_call(["deliver", "-c", self.conf, "-m", folder, "-p", mesg], executable="/usr/lib/dovecot/deliver")

    def delete(self):
        self.stop_server()
        shutil.rmtree(self.serverpath)
