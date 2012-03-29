Personal dashboard
==================

[![Flattr Button](http://api.flattr.com/button/button-static-50x60.png "Flattr This!")](https://flattr.com/thing/153663/Personal-dashboard "Flattr")

Usage
-----

The core `dashboard.py` reads the configuration and writes an HTML (or any other text-based format) file with a configured name. It doesn't take any command line arguments and if everything goes well, doesn't write anything to the standard error and output. This makes it perfect to run it from cron on UNIX-like systems or Task Scheduler on Windows.

Setup and install
-----------------

1. Install the dependencies if necessary (see below).
2. Create a new directory / folder and check out the repository into it.
3. Copy the `dashboard.sample.conf` to `~/.config/dnet/dashboard.conf` and modify it to your needs.
4. You can now test it by running `python dashboard.py`.

License
-------

The whole project (including the Orgnode module by Charles Cave) is licensed under MIT license.

Module interface
----------------

A module named `foobar` should be in a file named `foobar.py`. There should be at least one class named `Foobar` with a constructor that takes no parameters. An instance of this class must have a `getTodo()` method which also takes no parameters and returns the list of todos in the following format. Todos are stored as a list of dictionaries, each of these should contain at least a `title`, a `subtitle` and a `link` item.

For persistence, the `Config` class in the `config` module should be used, which extends the `QSettings` class with a constructor that takes no parameters. This way, configuration is stored in a standard way, commonplace `QSettings` methods can and should be used, most frequently `setValue("group/key", value)` and `value("group/key")`. It stores configuration using a native method of the platform, such as `~/.config/dnet/dashboard.conf` on UNIX-like systems, and registry on Windows. Further information and reference can be found at http://doc.qt.nokia.com/qsettings.html.

Dependencies
------------

 - Python 2.x (tested on 2.5)
 - PyQt4 (Debian/Ubuntu package: `python-qt4`)
 - Django (Debian/Ubuntu package: `python-django`)
 - requests (http://docs.python-requests.org/)
 - aleph-python-api (for `aleph_loaned` module only, https://github.com/dnet/aleph-python-api)
