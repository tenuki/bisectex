from decimal import Decimal

__all__ = ['BisectScanner', 'IntInterval', 'Interval', 'InvalidInterval',
           'SimpleSliceView', 'bisect', 'bisect_left', 'bisect_list',
           'bisect_right', 'bisect_f', 'insort', 'insort_left', 'insort_right']


class InvalidInterval(Exception):
    pass


class Interval:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @property
    def len(self):
        return self.right - self.left

    def half_len(self):
        r = Decimal(self.len) / 2
        if r == 0:
            raise InvalidInterval()
        return r

    def left_half(self):
        return self.__class__(self.left, self.left + self.half_len())

    def right_half(self):
        return self.__class__(self.left + self.half_len(), self.right)

    @property
    def half(self):
        return self.left + self.half_len()

    def __str__(self):
        return '<{:f}:{:f}>' % (self.left, self.right)


class IntInterval(Interval):
    def __init__(self, left, right):
        super().__init__(int(left), int(right))

    def half_len(self):
        r = self.len // 2
        if r == 0:
            r = 1
        return r


err_msg = "Object of type %s has no attribute '%s'"


class BisectScanner:
    def __init__(self, f, delta=1):
        self.delta = delta
        self.f = f

    def scan_interval(self, interval):
        # handle degenerated case: ie: extremes match
        val = self.f(interval.left)
        if val == self.f(interval.right):
            if val:
                return interval
            else:
                return IntInterval(interval.left, interval.left)
        return self._scan_interval(interval)

    def _scan_interval(self, interval):
        self.steps = 0
        left = self.f(interval.left)
        right = self.f(interval.right)
        while interval.len > self.delta:
            half = self.f(interval.half)
            assert {True, False} == {left == half, right == half}, self.state(
                interval, left, half, right)
            if left == half:
                interval = interval.right_half()
                left = self.f(interval.left)
            elif right == half:
                interval = interval.left_half()
                right = self.f(interval.right)
            else:
                raise InvalidInterval()
            self.steps += 1
        return interval

    def state(self, interval, left, half, right):
        return ("left: (%d)%s  half: (%d)%s  right: (%d)%s" % (interval.left,
                                                               left,
                                                               interval.half,
                                                               half,
                                                               interval.right,
                                                               right))


def array_cmp(i, a, x, left=False, key=None):
    custom_cmp = lambda _a, _b: _a < _b if left else _a <= _b
    get_elem = lambda x: x if key is None else key(x)
    if i < len(a):
        return custom_cmp(get_elem(a[i]), get_elem(x))
    if i == len(a):
        return False
    return custom_cmp(get_elem(a[i]), get_elem(x))


class SimpleSliceView(object):
    def __init__(self, a, start, stop=None):
        self.a = a
        self.start = start
        self.stop = stop if stop else len(a)

    def __len__(self):
        return self.stop - self.start

    def __getitem__(self, idx):
        if self.start + idx > self.stop:
            raise IndexError(idx)
        return self.a[self.start + idx]


def bisect_f(f, lo, hi, delta=Decimal('0.001')):
    bs = BisectScanner(f, delta)
    i = bs.scan_interval(Interval(lo, hi))
    return i.right


def bisect_list(a, x, left=False, key=None):
    if not hasattr(a, '__getitem__'):
        raise TypeError(err_msg % (a.__class__.__name__, '__getitem__'))
    if not hasattr(a, '__len__'):
        raise TypeError(err_msg % (a.__class__.__name__, '__len__'))
    if len(a) == 0:
        return 0
    bs = BisectScanner(lambda i: array_cmp(i, a, x, left=left, key=key))
    i = bs.scan_interval(IntInterval(0, len(a)))
    return i.right


def bisect_right(a, x, lo=0, hi=None, left=False, key=None):
    """basic implementation.
    handle extra indices and index error.
    also support objects which supports not slices.
    """
    if lo < 0:
        raise ValueError()
    return lo + bisect_list(SimpleSliceView(a, lo, hi), x, left=left, key=key)


def bisect_left(a, x, lo=0, hi=None, key=None):
    return bisect_right(a, x, lo=lo, hi=hi, left=True, key=key)


def insort_left(a, x, lo=0, hi=None, key=None):
    if not hasattr(a, 'insert'):
        raise TypeError(err_msg % (a.__class__.__name__, 'insert'))
    return a.insert(bisect_left(a, x, lo, hi, key=key), x)


def insort_right(a, x, lo=0, hi=None, key=None):
    if not hasattr(a, 'insert'):
        raise TypeError(err_msg % (a.__class__.__name__, 'insert'))
    return a.insert(bisect_right(a, x, lo, hi, key=key), x)


insort = insort_right
bisect = bisect_right
