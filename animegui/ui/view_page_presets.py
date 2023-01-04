from gi.repository import Gtk

from animegui.ui.view_base import BasePageView


@Gtk.Template(resource_path="/com/github/izzthedude/AniMeGUI/ui/presets-page")
class PresetsPageView(Gtk.ScrolledWindow, BasePageView):
    __gtype_name__ = "PresetsPageView"

    label1 = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "presets_page_view", "Presets", "open-book-symbolic"
