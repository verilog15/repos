"""Extension management."""

from typing import Dict, Optional

from django.conf import settings
from django.urls import include
from django.urls import re_path
from django.utils.encoding import smart_str


class ModoExtension:
    """
    Base extension class.

    Each Modoboa extension must inherit from this class to be
    considered as valid.
    """

    name: str
    label: str
    version: str = "NA"
    description: str = ""
    needs_media: bool = False
    always_active: bool = False
    url: Optional[str] = None
    topredirection_url: Optional[str] = None

    def get_available_apps(self) -> list:
        return []

    def get_url(self):
        """Return extension base url."""
        if self.url is None:
            return self.name
        return self.url

    def infos(self):
        """Information about this extension."""
        return {
            "name": self.name,
            "label": self.label,
            "version": self.version,
            "description": self.description,
            "url": self.get_url(),
            "topredirection_url": self.topredirection_url,
            "always_active": self.always_active,
        }

    def load_initial_data(self):
        """Declare extension data in this method."""
        pass

    def load(self):
        """Add extension loading tasks in this method."""
        pass


class ExtensionsPool:
    """The extensions manager"""

    def __init__(self) -> None:
        self.extensions: Dict[str, Dict] = {}

    def register_extension(self, ext: ModoExtension, show: bool = True) -> None:
        """Register an extension.

        :param ext: a class inheriting from ``Extension``
        :param show: list the extension or not
        """
        self.extensions[ext.name] = {"cls": ext, "show": show}

    def get_extension(self, name: str) -> Optional[ModoExtension]:
        """Retrieve the current instance of an extension."""
        if name not in self.extensions:
            return None
        if "instance" not in self.extensions[name]:
            self.extensions[name]["instance"] = self.extensions[name]["cls"]()
        return self.extensions[name]["instance"]

    def get_extension_infos(self, name):
        """Return information about the specified extension."""
        instance = self.get_extension(name)
        if instance is None:
            return None
        return instance.infos()

    def load_extension(self, name):
        """Load a registered extension."""
        __import__(name, locals(), globals(), [smart_str("modo_extension")])
        extinstance = self.get_extension(name)
        if extinstance is None:
            return None
        extinstance.load()
        return extinstance

    def load_all(self):
        """Load all defined extensions.

        Each extension must be loaded in order to integrate with
        Modoboa. Only enabled and special extensions are loaded but
        urls are always returned. The reason is urls are imported only
        once so must know all of them when the python process
        starts. Otherwise, it would lead to unexpected 404 errors :p

        :return: a list of url maps
        """
        for ext in settings.MODOBOA_APPS:
            self.load_extension(ext)

    def get_available_apps(self) -> list:
        result: list = []
        for ext_name in list(self.extensions.keys()):
            ext = self.get_extension(ext_name)
            if ext:
                result += ext.get_available_apps()
        return result

    def get_urls(self, category="app"):
        """Get all urls defined by extensions."""
        result = []
        for ext_name in list(self.extensions.keys()):
            ext = self.get_extension(ext_name)
            if category == "api":
                root = ""
                pattern = "{}.urls_api"
            else:
                root = rf"^{ext.get_url()}/"
                pattern = "{}.urls"
            try:
                result.append(re_path(root, include(pattern.format(ext_name))))
            except ImportError:
                # No urls for this extension
                pass
        return result

    def list_all(self):
        """List all defined extensions."""
        result = []
        for extname, extdef in list(self.extensions.items()):
            if not extdef["show"]:
                continue
            infos = self.get_extension_infos(extname)
            infos["id"] = extname
            result += [infos]
        return sorted(result, key=lambda i: i["name"])


exts_pool = ExtensionsPool()
