def classFactory(iface):
    from .mainPlugin import MobileSamPlugin
    return MobileSamPlugin(iface)