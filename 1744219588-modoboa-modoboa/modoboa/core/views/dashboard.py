"""Core dashboard views."""

import feedparser
import requests
from dateutil import parser
from requests.exceptions import RequestException

from django.contrib.auth import mixins as auth_mixins
from django.views import generic

from django.conf import settings

from .. import signals

MODOBOA_WEBSITE_URL = "https://modoboa.org/"


class DashboardView(auth_mixins.AccessMixin, generic.TemplateView):
    """Dashboard view."""

    template_name = "core/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        """Check if user can access dashboard."""
        if not request.user.is_authenticated or not request.user.is_admin:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add context variables."""
        context = super().get_context_data(**kwargs)
        context.update({"selection": "dashboard", "widgets": {"left": [], "right": []}})
        # Fetch latest news
        if self.request.user.language == "fr":
            lang = "fr"
        else:
            lang = "en"
        context.update({"selection": "dashboard"})

        feed_url = f"{MODOBOA_WEBSITE_URL}{lang}/weblog/feeds/"
        if self.request.user.role != "SuperAdmins":
            custom_feed_url = self.request.localconfig.parameters.get_value(
                "rss_feed_url"
            )
            if custom_feed_url:
                feed_url = custom_feed_url
        entries = []
        if not settings.DISABLE_DASHBOARD_EXTERNAL_QUERIES:
            posts = feedparser.parse(feed_url)
            for entry in posts["entries"][:5]:
                entry["published"] = parser.parse(entry["published"])
                entries.append(entry)
        context["widgets"]["left"].append("core/_latest_news_widget.html")
        context.update({"news": entries})

        hide_features_widget = self.request.localconfig.parameters.get_value(
            "hide_features_widget"
        )
        if self.request.user.is_superuser or not hide_features_widget:
            url = f"{MODOBOA_WEBSITE_URL}{lang}/api/projects/?featured=true"
            features = []
            if not settings.DISABLE_DASHBOARD_EXTERNAL_QUERIES:
                try:
                    response = requests.get(url)
                except RequestException:
                    pass
                else:
                    if response.status_code == 200:
                        features = response.json()
            context["widgets"]["right"].append("core/_current_features.html")
            context.update({"features": features})

        # Extra widgets
        result = signals.extra_admin_dashboard_widgets.send(
            sender=self.__class__, user=self.request.user
        )
        for _receiver, widgets in result:
            for widget in widgets:
                context["widgets"][widget["column"]].append(widget["template"])
                # FIXME: can raise conflicts...
                context.update(widget["context"])

        return context
