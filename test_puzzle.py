import numpy as np
from puzzle import Tile, Puzzle, Transformation, Swap, Rotate, Flip, make_scramble_plan

# ---- Tile ---- #
img = np.array([[1, 2], [3, 4]])
t = Tile(img, home_index=0)
t.rotate(1)
assert np.array_equal(t.image, [[3, 1], [4, 2]]), t.image    # clockwise
t.rotate(3)
assert t.is_upright()
t.flip(horizontal=True)
assert np.array_equal(t.image, [[2, 1], [4, 3]]), t.image
t.flip(horizontal=True)
assert t.is_upright()

# ---- Transformations ---- #
for x in [Swap(0, 1), Rotate(0, 1), Flip(0, True)]:
    assert isinstance(x, Transformation)
assert Swap(0, 1).restore_cost == 1
assert [Rotate(0, k).restore_cost for k in (1, 2, 3)] == [3, 2, 1]
assert Flip(0, True).restore_cost == 1
assert Flip(0, False).restore_cost == 3
try:
    Transformation()
    assert False, "should have failed"
except TypeError:
    pass


# ---- Puzzle ---- #
def fake_tiles(n):
    # 4 distinct values per tile so rotations/flips are detectable
    return [np.arange(4).reshape(2, 2) + 10 * i for i in range(n * n)]


for n in (3, 4, 5):
    for _ in range(200):               # scramble is random, so repeat
        plan = make_scramble_plan(n)
        targets = []
        for x in plan:
            targets += [x.i, x.j] if isinstance(x, Swap) else [x.index]
        assert len(targets) == len(set(targets)), "duplicate target"
        assert any(isinstance(x, Swap) for x in plan)
        assert any(isinstance(x, Rotate) for x in plan)
        assert any(isinstance(x, Flip) for x in plan)
        assert len(plan) == {3: 6, 4: 12, 5: 20}[n]

        p = Puzzle(fake_tiles(n), n)
        assert not p.is_solved()
        assert p.moves == 0
        p.solve()
        assert p.is_solved() and p.moves == 0

        # par_moves is exact, using only swap / rotate / horizontal flip #
        p = Puzzle(fake_tiles(n), n)
        par = p.par_moves
        for x in reversed(p._scramble):          # test peeks at the private list #
            if isinstance(x, Swap):
                p.swap(x.i, x.j)
            elif isinstance(x, Rotate):
                for _ in range(x.restore_cost):
                    p.rotate(x.index)
            else:
                p.flip(x.index)
                if not x.horizontal:             # vertical = flip + rotate 180 #
                    p.rotate(x.index)
                    p.rotate(x.index)
        assert p.is_solved()
        assert p.moves == par, (p.moves, par)
        
    # ---- restart returns to the starting scramble ----
    p = Puzzle(fake_tiles(3), 3)
    before = [t.image.copy() for t in p.tiles]
    p.swap(0, 1)
    p.rotate(2)
    p.flip(3)
    p.restart()
    assert p.moves == 0
    assert all(np.array_equal(a, t.image) for a, t in zip(before, p.tiles))

print("All tests OK")