Summary
-------

``imapapi`` is a library for accessing mailboxes, as well as a test suite that uses this library to verify the behavior of other mail-handling software (for example, ``offlineimap``).  To test offlineimap, we start up a local IMAP server and run offlineimap against it.

imapapi is licensed under an MIT license.  imapapi is provided as-is with no guarantee.

Layout
------

* ``test`` contains all tests, including self-tests.
* ``test/offlineimap`` contains tests that run OfflineIMAP and verify its behavior.

* ``test`` is also a module, defining a class ImapApiTest, which has a
  few methods useful for writing tests and accessing imapapi.
* ``test.offlineimap`` defines OfflineImapTest, which also provides a
  few methods for running offlineimap in a generic, but controlled,
  way.

Requirements
------------

* ``python-nose``

Usage
-----

::

    $ nosetests                   # to run all tests, including self-tests
    $ nosetests test/offlineimap  # to run OfflineIMAP tests
