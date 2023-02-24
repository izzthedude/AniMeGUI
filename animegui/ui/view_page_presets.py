from animegui.ui.view_page_base import BasePageView


class PresetsPageView(BasePageView):
    __gtype_name__ = "PresetsPageView"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debug_label.set_visible(True)

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "presets_page_view", "Presets", "open-book-symbolic"
