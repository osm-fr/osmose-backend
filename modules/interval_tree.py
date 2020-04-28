#-*- coding: utf-8 -*-
# Original code from http://code.google.com/p/bpbio/source/browse/trunk/interval_tree/
# Copyright bpederse, 2011, MIT License
#
# 2012, Rodrigo Frederic, edit to work with semi-open interval (p1,p2]
# 2015, Rodrigo Frederic, no assume segments are ordered

import operator


class IntervalTree(object):
    __slots__ = ('intervals', 'left', 'right', 'center')

    def __init__(self, intervals, depth=16, minbucket=64, _extent=None, maxbucket=512):
        """\
        `intervals` a list of intervals *with start and stop* attributes.
        `depth`     the depth of the tree
        `minbucket` if any node in the tree has fewer than minbucket
                    elements, make it a leaf node
        `maxbucket` even it at specifined `depth`, if the number of intervals >
                    maxbucket, split the node, make the tree deeper.

        depth and minbucket usually do not need to be changed. if
        dealing with large numbers (> 1M) of intervals, the depth could
        be increased to 24.

        Useage:

         >>> ivals = [Interval(2, 3), Interval(1, 8), Interval(3, 6)]
         >>> tree = IntervalTree(ivals)
         >>> sorted(tree.find(1, 2))
         [Interval(2, 3), Interval(1, 8)]

        this provides an extreme and satisfying performance improvement
        over searching manually over all 3 elements in the list (like
        a sucker).

        the IntervalTree class now also supports the iterator protocol
        so it's easy to loop over all elements in the tree:

         >>> import operator
         >>> sorted([iv for iv in tree], key=operator.attrgetter('start'))
         [Interval(1, 8), Interval(2, 3), Interval(3, 6)]


        NOTE: any object with start and stop attributes can be used
        in the incoming intervals list.
        """

        depth -= 1
        if (depth == 0 or len(intervals) < minbucket) and len(intervals) < maxbucket:
            self.intervals = intervals
            self.left = self.right = None
            return

        if _extent is None:
            # sorting the first time through allows it to get
            # better performance in searching later.
            intervals.sort(key=operator.attrgetter('start'))

        left, right = _extent or \
               (intervals[0].start, max(i.stop for i in intervals))
        #center = intervals[len(intervals)/ 2].stop
        center = (left + right) / 2.0


        self.intervals = []
        lefts, rights  = [], []


        for interval in intervals:
            if interval.stop < center:
                lefts.append(interval)
            elif interval.start > center:
                rights.append(interval)
            else: # overlapping.
                self.intervals.append(interval)

        self.left = lefts and IntervalTree(lefts, depth, minbucket, (intervals[0].start,  center)) or None
        self.right = rights and IntervalTree(rights, depth, minbucket, (center, right)) or None
        self.center = center


    def find(self, start, stop):
        """find all elements between (or overlapping) start and stop"""
        def comp(i):
            if i.y1 <= i.y2:
                return i.y2 >= start and i.y1 < stop
            else:
                return i.y1 > start and i.y2 <= stop

        if self.intervals:
            overlapping = list(filter(comp, self.intervals))
        else:
            overlapping = []

        if self.left and start <= self.center:
            overlapping += self.left.find(start, stop)

        if self.right and stop >= self.center:
            overlapping += self.right.find(start, stop)

        return overlapping

    def __iter__(self):
        if self.left:
            for l in self.left: yield l

        for i in self.intervals: yield i

        if self.right:
            for r in self.right: yield r

    # methods to allow un/pickling (by pzs):
    def __getstate__(self):
        return { 'intervals': self.intervals,
                    'left':   self.left,
                    'right':  self.right,
                    'center': self.center }

    def __setstate__(self, state):
        for key,value in state.items():
            setattr(self, key, value)

class Interval(object):
    __slots__ = ('start', 'stop')
    def __init__(self, start, stop):
        self.start = start
        self.stop  = stop
    def __repr__(self):
        return "Interval(%i, %i)" % (self.start, self.stop)

    def __getstate__(self):
        return {'start': self.start,
                'stop': self.stop }
    def __setstate__(self, state):
        for k, v in state.items():
            setattr(self, k, v)

if __name__ == '__main__':

    def brute_force_find(intervals, start, stop):
        return [i for i in intervals if i.stop >= start and i.start <= stop]

    import random, time
    def rand():
        s = random.randint(1, 2000000)
        return Interval(s, s + random.randint(200, 6000))
    intervals = [rand() for i in range(300000)]
    START, STOP = 390000, 400000
    intervals.append(Interval(0, 500000))
    tries = 100


    tree = IntervalTree(intervals)
    t = time.time()
    for i in range(tries):
        res = tree.find(START, STOP)
    treetime = time.time() - t
    t = time.time()
    print(treetime)

    """

    for i in range(tries):
        bf = [i for i in intervals if i.stop >= START and i.start <= STOP]
    btime = time.time() - t
    assert not set(bf).symmetric_difference(res) , (len(bf), len(res), set(bf).difference(res), START, STOP)
    print treetime, btime, btime/treetime


    assert sum(1 for x in tree) == len(intervals), "iterator not working?"

    intervals = [rand() for i in range(300)]
    atree = IntervalTree(intervals)
    import cPickle
    btree = cPickle.loads(cPickle.dumps(atree, -1))

    af = atree.find(START, STOP)
    bf = btree.find(START, STOP)
    assert len(af) == len(bf)
    for a, b in zip(af, bf):
        assert a.start == b.start
        assert a.stop == b.stop


    import doctest
    doctest.testmod()
    """
