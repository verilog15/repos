"""A client for Modoboa's public API."""

import logging
import os

import pkg_resources
import requests
from requests.exceptions import RequestException

from django.utils.translation import gettext as _

logger = logging.getLogger("modoboa.admin")


class ModoAPIClient:
    """A simple client for the public API."""

    def __init__(self, api_url=None):
        """Constructor."""
        if api_url is None:
            from django.conf import settings

            self._api_url = settings.MODOBOA_API_URL
        else:
            self._api_url = api_url
        self._local_core_version = None

    def __send_request(self, url, params=None):
        """Send a request to the API."""
        if params is None:
            params = {}
        try:
            resp = requests.get(url, params=params)
        except RequestException as err:
            logger.critical(_("Failed to communicate with public API: %s"), str(err))
            return None
        if resp.status_code != 200:
            return None
        return resp.json()

    @property
    def local_core_version(self):
        """Return the version installed locally."""
        if self._local_core_version is None:
            try:
                self._local_core_version = pkg_resources.get_distribution(
                    "modoboa"
                ).version
            except pkg_resources.DistributionNotFound:
                self._local_core_version = "unknown"
        return self._local_core_version

    def list_extensions(self):
        """List all official extensions."""
        url = os.path.join(self._api_url, "extensions/")
        return self.__send_request(url)

    def register_instance(self, hostname):
        """Register this instance."""
        url = f"{self._api_url}instances/search/?hostname={hostname}"
        instance = self.__send_request(url)
        if instance is None:
            url = f"{self._api_url}instances/"
            data = {"hostname": hostname, "known_version": self.local_core_version}
            try:
                response = requests.post(url, data=data)
            except RequestException as err:
                logger.critical(
                    _("Failed to communicate with public API: %s"), str(err)
                )
                return None
            if response.status_code != 201:
                return None
            instance = response.json()
        return int(instance["pk"])

    def update_instance(self, pk, data):
        """Update instance and send stats."""
        url = f"{self._api_url}instances/{pk}/"
        try:
            response = requests.put(url, data=data)
        except RequestException as err:
            logger.critical(_("Failed to communicate with public API: %s"), str(err))
            return
        if response.status_code != 200:
            logger.critical(
                _("Failed to communicate with public API: %s"), response.text
            )

    def versions(self):
        """Fetch core and extension versions."""
        url = f"{self._api_url}versions/"
        return self.__send_request(url)
