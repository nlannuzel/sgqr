class Tokenizer():
    def __init__(self, s: str) -> None:
        self._s = s
        self._pos = None
        self._last_id = None

    @property
    def s(self) -> str:
        return self._s
    @property
    def pos(self) -> str:
        return self._pos
    @pos.setter
    def pos(self, value) -> None:
        self._pos = value

    def _get_next_token(self, n: int) -> str:
        if n > (len(self.s) - self.pos):
            raise NotEnoughChractersError(self, n)
        res = self.s[self.pos:self.pos+n]
        self.pos += n
        return res

    def _get_dd(self, e):
        s = self._get_next_token(2)
        if not s.isnumeric():
            raise e(self, s)
        return s

    def _get_id(self):
        i = self._get_dd(InvalidIDError)
        if self._last_id is not None:
            if not i > self._last_id:
                raise IDOrderError(self, i)
        self._last_id = i
        return i

    def _get_len(self):
        return int(self._get_dd(InvalidLengthError))

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if not self.pos < len(self.s):
            raise StopIteration
        return [
            self._get_id(),
            self._get_next_token(self._get_len())]

    @staticmethod
    def to_entries(s):
        return [ {'id': tok[0], 'value': tok[1]} for tok in iter(Tokenizer(s)) ]

class TokenizerError(RuntimeError):
    pass

class NotEnoughChractersError(TokenizerError):
    def __init__(self, tok, n):
        super().__init__(f"tokenizer: string={tok.s}, len is {len(tok.s)}, pos={tok.pos}, read {n}: not enough characters")

class InvalidLengthError(TokenizerError):
    def __init__(self, tok, s):
        super().__init__(f"tokenizer: expected a two character length, but got {s}")

class InvalidIDError(TokenizerError):
    def __init__(self, tok, s):
        super().__init__(f"tokenizer: expected a two character id between 00 and 99, but got {s}")

class IDOrderError(TokenizerError):
    def __init__(self, tok, i):
        super().__init__(f"tokenizer: field IDs must be sorted and unique, got {i}, was expecting a value > {tok._last_id}")
