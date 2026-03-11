class DeTokenizer():
    def __init__(self, allow_empty: bool=False) -> None:
        self._s = ''
        self._allow_empty = allow_empty
        self._last_id = None

    @property
    def s(self) -> str:
        return self._s

    @property
    def allow_empty(self) -> str:
        return self._allow_empty

    def put_tokens(self, i: str, v: str) -> None:
        if type(i) is not str:
            raise(TypeError('id must be a string'))
        if len(i) != 2:
            raise(ValueError('len(id) is not 2'))
        if not i.isnumeric():
            raise(ValueError('id is not numeric'))
        if self._last_id is not None:
            if not i > self._last_id:
                raise(ValueError('id must increase'))
        self._last_id = i
        l = len(v)
        if not self.allow_empty and l == 0:
            raise(ValueError('len(value) must be > 0'))
        if l > 99:
            raise(ValueError('len(value) must be < 100'))
        self._s += i + "{:02d}".format(l) + v

    @staticmethod
    def entries_to_string(entries, allow_empty = True):
        detok = DeTokenizer(allow_empty)
        for ent in entries:
            if level != 0 or ent['id'] != CRC_ID:
                v = ent['value'] if type(ent['value']) is str else DeTokenizer.to_string(ent['value'], allow_empty, 1 + level)
                detok.put_tokens(ent['id'], v)
        
            return detok.s
