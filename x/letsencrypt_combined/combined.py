"""Let's Encrypt Combined Certificate Installer plugin."""

import os
import logging

import zope.component
import zope.interface

from letsencrypt import interfaces
from letsencrypt.plugins import common

logger = logging.getLogger(__name__)

class Installer(common.Plugin):
    """Combined Certificate Installer"""

    zope.interface.implements(interfaces.IInstaller)
    zope.interface.classProvides(interfaces.IPluginFactory)

    description = "Combined Certificate Installer"

    @classmethod
    def add_parser_arguments(cls, add):
        add("path", default=os.path.normpath("/certs/"),
            help="Path to install combined certificates to.")

    def __init__(self, *args, **kwargs):
        super(Installer, self).__init__(*args, **kwargs)

    def prepare(self):  # pylint: disable=missing-docstring
        path = self.conf("path")
        path = os.path.realpath(path)
        logger.debug("Combined directory: %s" % (path))
        if not os.path.isdir(path):
            raise ValueError("Path must be a directory", path)
        self.path = path

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ""

    def get_all_names(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path): # pylint: disable=missing-docstring
        path = "%s.pem" % (os.path.join(self.path, domain))
        logger.debug("Combined file: %s" % (path))
        combined = open(path, "w")
        # Write key, cert & chain in one file
        for x_path in [key_path, cert_path, chain_path]:
            if (x_path and os.path.isfile(x_path)):
                logger.debug("Concatenating file: %s" % (x_path))
                x_file = open(x_path, "r")
                combined.write(x_file.read())
                x_file.close()
            elif (x_path):
                raise ValueError("Must exist and be a file", x_path)
        combined.close()
        logger.info("Wrote combined file to: %s" % (path))

    def enhance(self, domain, enhancement, options=None):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def supported_enhancements(self):  # pylint: disable=missing-docstring,no-self-use
        return []  # pragma: no cover

    def get_all_certs_keys(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def save(self, title=None, temporary=False):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def rollback_checkpoints(self, rollback=1):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def recovery_routine(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def view_config_changes(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def config_test(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def restart(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover
