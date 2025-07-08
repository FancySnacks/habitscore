import pytest

from habitscore.task import Task, Completion


def test_raises_when_score_exceeds_range():
    with pytest.raises(ValueError):
        Task("test", -1, Completion(), 'test')
