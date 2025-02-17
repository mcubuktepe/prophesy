from prophesy.data.interval import Interval, string_to_interval, BoundType, constraint_to_interval
import pycarl

def test_interval_parsing():
    int1 = string_to_interval("(2,5)", int)
    assert int1.left_bound() == 2
    assert int1.left_bound_type() == BoundType.open
    assert int1.right_bound() == 5
    assert int1.right_bound_type() == BoundType.open
    assert str(int1) == "(2,5)";
    int1 = string_to_interval("(2,7]", int)
    assert int1.left_bound() == 2
    assert int1.left_bound_type() == BoundType.open
    assert int1.right_bound() == 7
    assert int1.right_bound_type() == BoundType.closed
    assert str(int1) == "(2,7]";

def test_interval_intersect():
    i1 = Interval(-pycarl.inf, BoundType.open, pycarl.inf, BoundType.open)
    assert i1.intersect(i1) == i1
    i2 = Interval(-3, BoundType.open, 4, BoundType.closed)
    assert i1.intersect(i2) == i2
    assert i2.intersect(i1) == i2
    i3 = Interval(5, BoundType.open, 6, BoundType.closed)
    assert i3.intersect(i2).empty()
    i4 = Interval(4, BoundType.closed, 6, BoundType.open)
    i5 = Interval(5, BoundType.open, 6, BoundType.open)
    assert i4.intersect(i3) == i5
    assert i4.intersect(i2) == Interval(4, BoundType.closed, 4, BoundType.closed)

def test_contains():
    i1 = Interval(-pycarl.inf, BoundType.open, pycarl.inf, BoundType.open)
    assert i1.contains(3)
    assert i1.contains(-4)
    i2 = Interval(-3, BoundType.open, 4, BoundType.closed)
    assert i2.contains(4)
    assert not i2.contains(-3)

def test_hash():
    i1 = Interval(-pycarl.inf, BoundType.open, pycarl.inf, BoundType.open)
    hash(i1)

def test_constraint_to_interval():
    s = "-10.2<fghhklöl<15.3"
    interval = constraint_to_interval(s, float)
    assert interval == string_to_interval("(-10.2,15.3)", float)

def test_interval_setminus():
    i1 = string_to_interval("[-10,10]", float)  # the closed universe

    # check the cases:
    # left from the interval - should be empty
    i = string_to_interval("[-20,-15]", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]
    i = string_to_interval("(-20,-15)", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]
    i = string_to_interval("[-20,-15)", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]
    i = string_to_interval("(-20,-15]", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]

    # right from the interval -should be empty
    i = string_to_interval("[15,20]", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]
    i = string_to_interval("[15,20)", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]
    i = string_to_interval("(15,20]", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]
    i = string_to_interval("(15,20)", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]

    # left from the interval ending at the lower bound
    i = string_to_interval("[-20,-10]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("(-10,10]", float)
    i = string_to_interval("(-20,-10)", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]
    i = string_to_interval("[-20,-10)", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]
    i = string_to_interval("(-20,-10]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("(-10,10]", float)

    # right from the interval ending at the lower bound
    i = string_to_interval("[10,15]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,10)", float)
    i = string_to_interval("(10,15)", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]
    i = string_to_interval("[10,15)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,10)", float)
    i = string_to_interval("(10,15]", float)
    intersection = i1.setminus(i)
    assert i1 == intersection[0]

    # left from the interval ending in the interval
    i = string_to_interval("[-20,0]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("(0,10]", float)
    i = string_to_interval("(-20,0)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[0,10]", float)
    i = string_to_interval("[-20,0)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[0,10]", float)
    i = string_to_interval("(-20,0]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("(0,10]", float)

    # right from the interval ending in the interval
    i = string_to_interval("[0,15]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,0)", float)
    i = string_to_interval("(0,15)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,0]", float)
    i = string_to_interval("[0,15)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,0)", float)
    i = string_to_interval("(0,15]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,0]", float)

    # left from the interval ending at the upper bound
    i = string_to_interval("[-20,10]", float)
    intersection = i1.setminus(i)
    assert not intersection
    i = string_to_interval("(-20,10)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[10,10]", float)
    i = string_to_interval("[-20,10)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[10,10]", float)
    i = string_to_interval("(-20,10]", float)
    intersection = i1.setminus(i)
    assert not intersection

    # right from the interval ending at the lower bound
    i = string_to_interval("[-10,15]", float)
    intersection = i1.setminus(i)
    assert not intersection
    i = string_to_interval("(-10,15)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,-10]", float)
    i = string_to_interval("[-10,15)", float)
    intersection = i1.setminus(i)
    assert not intersection
    i = string_to_interval("(-10,15]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,-10]", float)

    # inside the interval
    i = string_to_interval("[-5,5]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,-5)", float) and \
           intersection[1] == string_to_interval("(5,10]", float)
    i = string_to_interval("[-5,5)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,-5)", float) and \
           intersection[1] == string_to_interval("[5,10]", float)
    i = string_to_interval("(-5,5]", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,-5]", float) and \
           intersection[1] == string_to_interval("(5,10]", float)
    i = string_to_interval("(-5,5)", float)
    intersection = i1.setminus(i)
    assert intersection[0] == string_to_interval("[-10,-5]", float) and \
           intersection[1] == string_to_interval("[5,10]", float)

    # bigger than the interval
    i = string_to_interval("[-20,20]", float)
    intersection = i1.setminus(i)
    assert not intersection
    i = string_to_interval("(-20,20)", float)
    intersection = i1.setminus(i)
    assert not intersection
    i = string_to_interval("[-20,20)", float)
    intersection = i1.setminus(i)
    assert not intersection
    i = string_to_interval("(-20,20]", float)
    intersection = i1.setminus(i)
    assert not intersection
