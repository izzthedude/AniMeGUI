class BasePageView:
    def _define_stackpage(self) -> tuple[str, str, str]:
        """
        Define some common AdwViewStackPage information as a tuple of (name, title, icon).
        """
        raise NotImplementedError("Child classes must override this method.")
