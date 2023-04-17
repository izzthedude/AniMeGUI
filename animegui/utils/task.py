from gi.repository import GObject, Gio, GLib

from animegui.utils.gi_helpers import create_signal


class TaskManager(GObject.Object):
    STARTED = "snowsuit-greeting"
    FINISHED = "mango-eggplant"
    ERROR = "xbox-rebate"
    CANCELLED = "saint-voice"

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        if not GObject.signal_list_names(self):
            self._setup_signals()

        # TODO: Add cancel functionality

        self._func = func
        self._args = args
        self._kwargs = kwargs

        self._on_finish = None
        self._on_finish_args = None
        self._on_finish_kwargs = None

        self._on_error = None
        self._on_error_args = None
        self._on_error_kwargs = None

        self._on_cancel = None
        self._on_cancel_args = None
        self._on_cancel_kwargs = None

        self._source = None
        self._cancellable = Gio.Cancellable()

    def start(self):
        task: Gio.Task = Gio.Task.new(self._source, self._cancellable, self._func_ready_wrapper, None)
        task.set_check_cancellable(True)
        task.set_return_on_cancel(True)
        task.return_error_if_cancelled()
        if self._on_finish: self.connect(self.FINISHED, self._on_finish_wrapper)
        if self._on_error: self.connect(self.ERROR, self._on_finish_wrapper)
        task.run_in_thread(self._func_wrapper)

    def cancel(self):
        self._cancellable.cancel()

    def is_cancelled(self):
        self._cancellable.is_cancelled()

    def set_on_finish(self, func, *args, **kwargs):
        self._on_finish = func
        self._on_finish_args = args
        self._on_finish_kwargs = kwargs

    def set_on_error(self, func, *args, **kwargs):
        self._on_error = func
        self._on_error_args = args
        self._on_error_kwargs = kwargs

    def set_on_cancel(self, func, *args, **kwargs):
        self._on_cancel = func
        self._on_cancel_args = args
        self._on_cancel_kwargs = kwargs

    def set_source(self, source):
        self._source = source

    def set_cancellable(self, cancellable: Gio.Cancellable):
        self._cancellable = cancellable

    def _func_wrapper(self, task: Gio.Task, source, data, cancellable: Gio.Cancellable):
        func_name = self._func.__name__
        print(f"Worker running function: {func_name}{self._args}{self._kwargs}")

        try:
            self.emit(self.STARTED)
            result = self._func(*self._args, **self._kwargs)
            task.return_value(result)

        except Exception as err:
            print(f"An error has occurred while running '{func_name}' in thread: {err}")
            task.return_value(err)

    def _func_ready_wrapper(self, source, task: Gio.Task, error):
        cancellable = task.get_cancellable()
        if cancellable.is_cancelled():
            print(f"Function {self._func.__name__}{self._args}{self._kwargs} cancelled")
            self.emit(self.CANCELLED)
            if self._on_cancel:
                self._on_cancel(*self._on_cancel_args, **self._on_cancel_kwargs)
            return

        # Get result and emit it. Depends on whether an error occurred while running.
        result = task.propagate_value()[1]
        signal = self.FINISHED
        if isinstance(result, BaseException) or isinstance(result, GLib.Error):
            signal = self.ERROR
        self.emit(signal, result)

    def _on_finish_wrapper(self, taskmanager, result):
        # Determine if self._on_finish or self._on_error should run
        is_error = isinstance(result, Exception)
        func = self._on_finish if not is_error else self._on_error
        func_args = self._on_finish_args if not is_error else self._on_error_args
        func_kwargs = self._on_finish_kwargs if not is_error else self._on_error_kwargs
        func_name = func.__name__

        print(f"Worker running on finished function: {func_name}{func_args}{func_kwargs}")
        try:
            if result is None:
                func(*func_args, **func_kwargs)
            else:
                func(*func_args, result, **func_kwargs)

        except Exception as err:
            print(f"An error has occurred while running '{func_name}': {err}")

    def _setup_signals(self):
        create_signal(self, self.STARTED)
        create_signal(self, self.FINISHED, [object])
        create_signal(self, self.ERROR, [object])  # param_type is Exception
        create_signal(self, self.CANCELLED)
