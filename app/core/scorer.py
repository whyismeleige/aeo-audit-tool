from dataclasses import dataclass


@dataclass
class CategoryScore:
    score: int
    max_possible: int
    metrics: dict[str, int]
    findings: list[str]
    recommendations: list[str]


@dataclass
class ScoreResult:
    overall_score: int
    metadata: CategoryScore
    content_quality: CategoryScore
    structured_data: CategoryScore
    connectivity: CategoryScore
    technical_compliance: CategoryScore


def _score_title(title: str | None) -> tuple[int, list[str], list[str]]:
    if not title:
        return (
            0,
            ["Title tag is not present", "Title is not present in the website"],
            [
                "Title is required for your website",
                "Title is heavily important for AI Citations",
            ],
        )

    word_count = len(title.split())

    upper_limit = 15
    lower_limit = 5

    max_score = 30
    
    if word_count < lower_limit:
        score = round((word_count / lower_limit) * max_score)
        return (
            score,
            ["Title is too short"],
            [
                "Lengthen your Title of your website",
                "Make your Title descriptive and definitive",
            ],
        )
    elif lower_limit <= word_count <= upper_limit:
        return (max_score, ["Title is properly defined"], [])
    else:
        score = max(max_score - (word_count - upper_limit) * 2, 10)
        return (score, ["Title is too long"], ["Make the title short and consise."])


def _score_meta_description(
    description: str | None,
) -> tuple[int, list[str], list[str]]:
    if not description:
        return (
            0,
            [
                "Meta Description is not present",
                "Meta Description is not present in the website",
            ],
            [
                "Meta Description is required for your website",
                "Meta Description is heavily important for your citations",
            ],
        )

    word_count = len(description.split())

    upper_limit = 20
    lower_limit = 15
    
    max_score = 30

    if word_count < lower_limit:
        score = round((word_count / lower_limit) * max_score)
        return (
            score,
            ["Meta Description is too short"],
            [
                "Lengthen your Meta Description of your website.",
                "Make your Meta Description descriptive and definitive.",
            ],
        )
    elif lower_limit <= word_count <= upper_limit:
        return (max_score, ["Meta Description is properly defined"], [])
    else:
        score = max(max_score - (word_count - upper_limit) * 2, 10)
        return (
            score,
            ["Meta Description is too long"],
            ["Make the description short and consise."],
        )
