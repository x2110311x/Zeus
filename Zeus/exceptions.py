# Control Signals

class Signal(Exception):
    pass

class RestartSignal(Signal):
    pass

class ShutdownSignal(Signal):
    pass