from decimal import Decimal


class Interval:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @property
    def len(self):
        return self.right-self.left

    def halflen(self):
        r = Decimal(self.len)/2
        if r ==0:
            raise InvalidInterval()
        return r

    def left_half(self):
        return Interval(self.left, self.left + self.halflen())

    def right_half(self):
        return Interval(self.left + self.halflen(), self.right)

    @property
    def half(self):
        return self.left+self.halflen()

    def __str__(self):
        return '<{:f}:{:f}>' % (self.left, self.right)


class IntInterval:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @property
    def len(self):
        return self.right-self.left

    def halflen(self):
        r = self.len//2
        if r ==0:
            r=1
        return r

    def left_half(self):
        return IntInterval(self.left, self.left + self.halflen())

    def right_half(self):
        return IntInterval(self.left + self.halflen(), self.right)

    @property
    def half(self):
        return self.left+self.halflen()

    def __str__(self):
        return '<%s:%s>'%(self.left, self.right)


class InvalidInterval(Exception):
    pass


err_msg = "Object of type %s has no attribute '%s'"


class BisectScanner:
    def __init__(self, f, delta=1):
        self.delta = delta
        self.f = f

    def scan_interval(self, interval):
        # handle degenerated case: ie: extremes match
        val = self.f(interval.left)
        if val == self.f(interval.right) and val==True:
            return interval
        if val == self.f(interval.right) and val==False:
            return IntInterval(interval.left, interval.left)
        return self._scan_interval(interval)

    def _scan_interval(self, interval):
        self.steps = 0
        while interval.len>self.delta:
            left = self.f(interval.left)
            right = self.f(interval.right)
            half = self.f(interval.half)
            print( '%05d | %s -- %s -- %s  [%r %r %r] (len:%d)' % (self.steps,
                interval.left, interval.half, interval.right,
                left, half, right, interval.len))
            assert {True, False} == {left == half, right == half}, \
                "left: (%d)%s  half: (%d)%s  right: (%d)%s" %(interval.left,
                          left, interval.half, half, interval.right, right)
            if left==half:
                interval = interval.right_half()
            elif right==half:
                interval = interval.left_half()
            else:
                raise InvalidInterval()
            self.steps += 1
        return interval


def array_cmp(i, a, x, left=False):
    custom_cmp = lambda _a,_b: _a<_b if left else _a<=_b
    if i < len(a):
        r = custom_cmp(a[i], x)
        return r
    if i == len(a):
        return False
    return custom_cmp(a[i],x)


class MySlice(object):
    def __init__(self, a, start, stop=None):
        self.a = a
        self.start = start
        self.stop = stop if stop else len(a)

    def __len__(self):
        return self.stop-self.start

    def __getitem__(self, idx):
        if self.start+idx>self.stop:
            raise IndexError(idx)
        return self.a[self.start + idx]


def bisectf(f, lo, hi, delta=Decimal('0.001')):
    bs = BisectScanner(f, delta)
    i = bs.scan_interval(Interval(lo, hi))
    return i.right


def bisect_list(a, x, left=False):
    if not hasattr(a, '__getitem__'):
        raise TypeError(err_msg % (a.__class__.__name__, '__getitem__'))
    if not hasattr(a, '__len__'):
        raise TypeError(err_msg % (a.__class__.__name__, '__len__'))
    if len(a)==0:
        return 0
    bs = BisectScanner(lambda i: array_cmp(i, a, x, left=left))
    i = bs.scan_interval(IntInterval(0, len(a)))
    print('---------->     %r)' % i.right)
    return i.right


def bisect_right(a, x, lo=0, hi=None, left=False):
    """basic implementation.
    handle extra indices and index error.
    also support objects which supports not slices.
    """
    if lo<0:
        raise ValueError()
    print('<----------  bisect(%r)(%r,%r,%r,%r)'%(left, a, x, lo, hi))
    return lo+bisect_list(MySlice(a, lo, hi), x, left=left)  # ..(a[lo:hi] ..


def bisect_left(a, x, lo=0, hi=None):
    return bisect_right(a, x, lo=lo, hi=hi, left=True)


def insort_left(a, x, lo=0, hi=None):
    if not hasattr(a, 'insert'):
        raise TypeError(err_msg % (a.__class__.__name__, 'insert'))
    return a.insert(bisect_left(a, x, lo, hi), x)


def insort_right(a, x, lo=0, hi=None):
    if not hasattr(a, 'insert'):
        raise TypeError(err_msg % (a.__class__.__name__, 'insert'))
    return a.insert(bisect_right(a, x, lo, hi), x)


insort = insort_right
bisect = bisect_right
