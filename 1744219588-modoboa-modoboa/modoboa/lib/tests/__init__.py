"""Testing utilities."""

import socket
import tempfile

from django.conf import settings
from django.core import management
from django.test import TestCase

from importlib import import_module

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from modoboa.core import models as core_models
from .. import sysutils

try:
    s = socket.create_connection(("127.0.0.1", 25))
    s.close()
    NO_SMTP = False
except OSError:
    NO_SMTP = True

try:
    import ldap  # noqa

    NO_LDAP = False
except ImportError:
    NO_LDAP = True


class ParametersMixin:
    """Add tools to manage parameters."""

    @classmethod
    def setUpTestData(cls):  # noqa
        """Set LocalConfig instance."""
        super().setUpTestData()
        cls.localconfig = core_models.LocalConfig.objects.first()

    def set_global_parameter(self, name, value, app=None):
        """Set global parameter for the given app."""
        if app is None:
            app = sysutils.guess_extension_name()
        self.localconfig.parameters.set_value(name, value, app=app)
        self.localconfig.save()

    def set_global_parameters(self, parameters, app=None):
        """Set/update global parameters for the given app."""
        if app is None:
            app = sysutils.guess_extension_name()
        self.localconfig.parameters.set_values(parameters, app=app)
        self.localconfig.save()


class SimpleModoTestCase(ParametersMixin, TestCase):
    """Simple class to add parameters editing."""


class ModoTestCase(ParametersMixin, TestCase):
    """All test cases must inherit from this one."""

    @classmethod
    def setUpTestData(cls):  # noqa
        """Create a default user."""
        super().setUpTestData()
        management.call_command("load_initial_data", "--no-frontend")

    def setUp(self, username="admin", password="password"):
        """Initiate test context."""
        self.assertEqual(self.client.login(username=username, password=password), True)
        self.workdir = tempfile.mkdtemp()
        self.set_global_parameter("storage_dir", self.workdir, app="pdfcredentials")

    def ajax_request(self, method, url, params=None, status=200):
        if params is None:
            params = {}
        response = getattr(self.client, method)(
            url, params, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, status)
        return response.json()

    def ajax_post(self, *args, **kwargs):
        return self.ajax_request("post", *args, **kwargs)

    def ajax_put(self, *args, **kwargs):
        return self.ajax_request("put", *args, **kwargs)

    def ajax_delete(self, *args, **kwargs):
        return self.ajax_request("delete", *args, **kwargs)

    def ajax_get(self, *args, **kwargs):
        return self.ajax_request("get", *args, **kwargs)


class ModoAPITestCase(ParametersMixin, APITestCase):
    """All test cases must inherit from this one."""

    @classmethod
    def setUpTestData(cls):  # noqa
        """Create a default user."""
        super().setUpTestData()
        management.call_command("load_initial_data")
        cls.token = Token.objects.create(
            user=core_models.User.objects.get(username="admin")
        )

    def setUp(self):
        """Setup."""
        super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.workdir = tempfile.mkdtemp()
        self.set_global_parameter("storage_dir", self.workdir, app="pdfcredentials")

    def create_session(self):
        """Enable session storage across requests."""
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
