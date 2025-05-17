import os
from unittest.mock import patch, Mock

import pytest

from solution2 import WikipediaAnimals, count_animals, write_data_to_csv

html_pages = [
    """
<div class="mw-category mw-category-columns">
А
Аист
Акула
Б
Бегемот
Бабочка
В
Волк
Воробей
</div>
<a href="next_page">Следующая страница</a>
""",
    """
<div class="mw-category mw-category-columns">
Г
Гусь
Ж
Жираф
</div>
<a href="next_page">Следующая страница</a>
""",
    """
<div class="mw-category mw-category-columns">
A
Abax
</div>
<a href="next_page">Следующая страница</a>
""",
]


@patch("requests.get")
def test_wikipedia_animals_iter(mock_get):
    mock_get.side_effect = [
        Mock(status_code=200, text=html_pages[0]),
        Mock(status_code=200, text=html_pages[1]),
        Mock(status_code=200, text=html_pages[2]),
    ]
    animals_iter = WikipediaAnimals()

    assert next(animals_iter) == [
        "Аист",
        "Акула",
        "Бегемот",
        "Бабочка",
        "Волк",
        "Воробей",
    ]
    assert next(animals_iter) == ["Гусь", "Жираф"]

    with pytest.raises(StopIteration):
        next(animals_iter)


def test_count_animals():
    iter_return_value = [
        ["Аист", "Акула", "Бегемот"],
        ["Волк", "Воробей", "Гусь"],
    ]
    with patch("solution2.WikipediaAnimals", return_value=iter(iter_return_value)):
        result = count_animals()
        assert result["А"] == 2
        assert result["Б"] == 1
        assert result["В"] == 2
        assert result["Г"] == 1


def test_write_data_to_csv():
    data = {"А": 5, "Б": 3}
    filepath = "beasts2.csv"
    write_data_to_csv(filepath, data)
    with open(filepath, "r") as file:
        content = file.read()
    os.remove(filepath)
    expected_result = "А,5\nБ,3\n"
    assert expected_result == content
