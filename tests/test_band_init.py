import pytest
from rects.region import Band


def test_y1_greater_than_y2():
    with pytest.raises(ValueError, match="Band invalid"):
        Band(5, 3, [1, 2, 3])
