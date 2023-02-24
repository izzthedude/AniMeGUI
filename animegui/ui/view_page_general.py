from animegui.ui.view_page_base import BasePageView


class GeneralPageView(BasePageView):
    __gtype_name__ = "GeneralPageView"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debug_label.set_visible(True)

    def _define_stackpage(self) -> tuple[str, str, str]:
        return "general_page-view", "General", "tv-symbolic"
