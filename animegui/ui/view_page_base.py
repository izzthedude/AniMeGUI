from gi.repository import Gtk


class BasePageView(Gtk.ScrolledWindow):
    __gtype_name__ = "BasePageView"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content_box: Gtk.Box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_top=30,
            margin_start=100,
            margin_end=100,
            margin_bottom=30,
            spacing=30
        )
        self.set_child(self.content_box)

        self.debug_label: Gtk.Label = Gtk.Label(
            vexpand=True,
            hexpand=True,
            visible=False,
            label=self._define_stackpage()[1]
        )
        self.debug_label.add_css_class("title-1")
        self.content_box.append(self.debug_label)

    def add_widget(self, widget: Gtk.Widget):
        """
        Add the given widget to the content box of the page.

        Parameters
        ----------
        widget: Gtk.Widget
            A widget that will be added to the page's content box.
        """
        self.content_box.append(widget)

    def _define_stackpage(self) -> tuple[str, str, str]:
        """
        Define some common AdwViewStackPage information by returning a tuple of (name, title, icon).

        Intended to be implemented by child classes.
        """
        raise NotImplementedError("Child classes must override this method.")
