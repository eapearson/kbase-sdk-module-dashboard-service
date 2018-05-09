import copy
import os


class DataPaletteTypes:

    _TYPES = {}
    _KEYS = frozenset([key for key in _TYPES])

    def __init__(self, switchOn):
        if switchOn:
            self._TYPES = {"KBaseSets.ReadsSet": {},
                           "KBaseFile.PairedEndLibrary": {},
                           "KBaseFile.SingleEndLibrary": {},
                           "KBaseAssembly.SingleEndLibrary": {},
                           "KBaseAssembly.PairedEndLibrary": {}
                           }
            if "OVERRIDE_TYPES" in os.environ:
                for dtype in os.environ["OVERRIDE_TYPES"]:
                    self._TYPES[dtype] = {}
            self._KEYS = frozenset([key for key in self._TYPES])

    def get(self, type_name):
        ret = self._TYPES.get(type_name)
        if ret is None:
            return None
        return copy.deepcopy(ret)

    def keys(self):
        return self._KEYS
