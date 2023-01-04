from gi.repository import Gtk

from animegui.ui.view_base import BasePageView


@Gtk.Template(resource_path="/com/github/izzthedude/AniMeGUI/ui/live-page")
class LivePageView(Gtk.ScrolledWindow, BasePageView):
    __gtype_name__ = "LivePageView"

    label2 = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "live_page_view", "Live", "camera-photo-symbolic"
