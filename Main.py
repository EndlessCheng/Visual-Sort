# -*- coding: utf-8 -*-
import random
import string


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        assert isinstance(other, Point)
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def output(self):
        print "%2d %2d" % (self.x, self.y)


class People(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __lt__(self, other):
        assert isinstance(other, People)
        return self.name < other.name or (self.name == other.name and self.age < other.age)

    def output(self):
        print "%s %2d" % (self.name, self.age)


def cmp_less(a, b):
    return a < b


def cmp_greater(a, b):
    return b < a


def insertion_sort(a, comp):
    if len(a) == 1:
        return a
    b = insertion_sort(a[1:], comp)
    for i in xrange(len(b)):
        if comp(a[0], b[i]):
            b.insert(i, a[0])
            return b
    return b + [a[0]]


def bubble_sort(a, comp):
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if comp(a[j], a[i]):
                a[i], a[j] = a[j], a[i]
    return a


def quick_sort(a, comp):
    if len(a) <= 1:
        return a
    pivot_element = random.choice(a)
    small = [i for i in a if comp(i, pivot_element)]
    medium = [i for i in a if i == pivot_element]
    large = [i for i in a if comp(pivot_element, i)]
    return quick_sort(small, comp) + medium + quick_sort(large, comp)


def main():
    a = []
    random_range = 99

    for i in range(5):
        x = random.randint(0, random_range)
        a.append(Point(x, random.randint(0, random_range)))
        a.append(Point(x, random.randint(0, random_range)))

    a2 = list(a)

    print "原序列："
    for p in a:
        p.output()
    print ""

    print "升序，使用插入排序："
    a = insertion_sort(a, cmp_less)
    for p in a:
        p.output()
    print ""

    print "降序，使用冒泡排序："
    a = bubble_sort(a2, cmp_greater)
    for p in a:
        p.output()
    print ""

    a = []
    for i in range(5):
        x = "".join([random.choice(string.lowercase) for i in range(5)])
        a.append(People(x, random.randint(0, random_range)))
        a.append(People(x, random.randint(0, random_range)))

    print "原序列："
    for man in a:
        man.output()
    print ""

    print "字典序，使用快速排序："
    a = quick_sort(a, cmp_less)
    for p in a:
        p.output()
    print ""


if __name__ == '__main__':
    main()