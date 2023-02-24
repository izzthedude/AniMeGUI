from animegui.ui.view_page_base import BasePageView


class LivePageView(BasePageView):
    __gtype_name__ = "LivePageView"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debug_label.set_visible(True)

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "live_page_view", "Live", "camera-photo-symbolic"
