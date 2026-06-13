import pytest
from app.core.scorer import _score_title, _score_meta_description


@pytest.mark.parametrize(
    "title, expected",
    [
        (
            None,
            (
                0,
                ["Title tag is not present", "Title is not present in the website"],
                [
                    "Title is required for your website",
                    "Title is heavily important for AI Citations",
                ],
            ),
        ),
        (
            "Word Count is 4",
            (
                24,
                ["Title is too short"],
                [
                    "Lengthen your Title of your website",
                    "Make your Title descriptive and definitive",
                ],
            ),
        ),
        ("Word Count is more than 5 words", (30, ["Title is properly defined"], [])),
        (
            "Title is really too long because it more than 15 words so the score is going down for this one",
            (20, ["Title is too long"], ["Make the title short and consise."]),
        ),
    ],
)
def test_score_title(title, expected):
    result = _score_title(title)
    assert result == expected


@pytest.mark.parametrize(
    "description, expected",
    [
        (
            None,
            (
                0,
                [
                    "Meta Description is not present",
                    "Meta Description is not present in the website",
                ],
                [
                    "Meta Description is required for your website",
                    "Meta Description is heavily important for your citations",
                ],
            ),
        ),
        (
            "Meta Description is too short",
            (
                10,
                ["Meta Description is too short"],
                [
                    "Lengthen your Meta Description of your website.",
                    "Make your Meta Description descriptive and definitive.",
                ],
            ),
        ),
        (
            "Meta Description is properly defined with well definitive description which is easily understandable by Crawlers and Bots",
            (30, ["Meta Description is properly defined"], []),
        ),
        (
            "Meta Description is really too long because it more than 20 words so the score is going down for this one because excessive content disposition.",
            (
                20,
                ["Meta Description is too long"],
                ["Make the description short and consise."],
            ),
        ),
    ],
)
def test_score_meta_description(description, expected):
    result = _score_meta_description(description)
    assert result == expected
