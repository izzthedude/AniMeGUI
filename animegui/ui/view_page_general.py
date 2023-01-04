from gi.repository import Gtk

from animegui.ui.view_base import BasePageView


@Gtk.Template(resource_path="/com/github/izzthedude/AniMeGUI/ui/general-page")
class GeneralPageView(Gtk.ScrolledWindow, BasePageView):
    __gtype_name__ = "GeneralPageView"

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "general_page-view", "General", "tv-symbolic"
