import pytest

from app.core.scorer import (
    _score_title,
    _score_meta_description,
    _score_canonical_url,
    _score_meta_robots,
    _score_metadata,
    _score_word_count,
    _score_headings,
    _score_body_content,
    _score_content_quality,
    _score_faq_items,
    _score_has_schema,
    _score_schema_types,
    _score_schema_quality,
    _score_internal_links,
    _score_connectivity,
    _score_images_without_alt,
    _score_technical_compliance,
    CategoryScore,
)
from app.core.parser import ParsedPage, FAQItem


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


@pytest.mark.parametrize(
    "canonical_url, expected",
    [
        (
            None,
            (
                0,
                ["Canonical URL is not present in your website"],
                [
                    "Canonical URL is required for proper citation and indexing of your website."
                ],
            ),
        ),
        (
            "",
            (
                0,
                ["Canonical URL is not present in your website"],
                [
                    "Canonical URL is required for proper citation and indexing of your website."
                ],
            ),
        ),
        (
            "https://example.com/about",
            (20, ["Canonical URL is present in your website"], []),
        ),
    ],
)
def test_score_canonical_url(canonical_url, expected):
    result = _score_canonical_url(canonical_url)
    assert result == expected


@pytest.mark.parametrize(
    "meta_robots, expected",
    [
        (
            None,
            (
                12,
                ["Meta robots not explicitly optimized"],
                ["Consider setting to index, follow"],
            ),
        ),
        (
            "INDEX, FOLLOW",
            (20, ["Meta robots fully permits indexing and following"], []),
        ),
        (
            "none",
            (
                0,
                ["Meta robots heavily restricts AI/crawler access"],
                ["Remove restrictive directives like noindex/nofollow"],
            ),
        ),
        (
            "noindex",
            (
                2,
                ["Meta robots contains restrictive directives"],
                ["Review and remove unneccessary restrictions"],
            ),
        ),
        (
            "all, none",
            (
                12,
                ["Meta robots not explicitly optimized"],
                ["Consider setting to index, follow"],
            ),
        ),
        (
            "max-snippet:-1",
            (
                12,
                ["Meta robots not explicitly optimized"],
                ["Consider setting to index, follow"],
            ),
        ),
    ],
)
def test_score_meta_robots(meta_robots, expected):
    result = _score_meta_robots(meta_robots)
    assert result == expected


@pytest.mark.parametrize(
    "page, expected",
    [
        (
            # Everything missing
            ParsedPage(
                url="https://example.com",
                status_code=200,
            ),
            CategoryScore(
                score=12,
                max_possible=100,
                metrics={
                    "title": 0,
                    "meta_description": 0,
                    "canonical_url": 0,
                    "meta_robots": 12,
                },
                findings=[
                    "Title tag is not present",
                    "Title is not present in the website",
                    "Meta Description is not present",
                    "Meta Description is not present in the website",
                    "Canonical URL is not present in your website",
                    "Meta robots not explicitly optimized",
                ],
                recommendations=[
                    "Title is required for your website",
                    "Title is heavily important for AI Citations",
                    "Meta Description is required for your website",
                    "Meta Description is heavily important for your citations",
                    "Canonical URL is required for proper citation and indexing of your website.",
                    "Consider setting to index, follow",
                ],
            ),
        ),
        (
            # Everything optimized
            ParsedPage(
                url="https://example.com",
                status_code=200,
                title="This title contains more than five words",
                meta_description=(
                    "This meta description contains enough words to satisfy "
                    "the optimal length requirements easily and is proper."
                ),
                canonical_url="https://example.com",
                meta_robots="index, follow",
            ),
            CategoryScore(
                score=100,
                max_possible=100,
                metrics={
                    "title": 30,
                    "meta_description": 30,
                    "canonical_url": 20,
                    "meta_robots": 20,
                },
                findings=[
                    "Title is properly defined",
                    "Meta Description is properly defined",
                    "Canonical URL is present in your website",
                    "Meta robots fully permits indexing and following",
                ],
                recommendations=[],
            ),
        ),
        (
            # Mixed quality page
            ParsedPage(
                url="https://example.com",
                status_code=200,
                title="Too short",
                meta_description="Short description",
                canonical_url=None,
                meta_robots="noindex",
            ),
            CategoryScore(
                score=18,
                max_possible=100,
                metrics={
                    "title": 12,
                    "meta_description": 4,
                    "canonical_url": 0,
                    "meta_robots": 2,
                },
                findings=[
                    "Title is too short",
                    "Meta Description is too short",
                    "Canonical URL is not present in your website",
                    "Meta robots contains restrictive directives",
                ],
                recommendations=[
                    "Lengthen your Title of your website",
                    "Make your Title descriptive and definitive",
                    "Lengthen your Meta Description of your website.",
                    "Make your Meta Description descriptive and definitive.",
                    "Canonical URL is required for proper citation and indexing of your website.",
                    "Review and remove unneccessary restrictions",
                ],
            ),
        ),
    ],
)
def test_score_metadata(page, expected):
    result = _score_metadata(page)
    assert result == expected


@pytest.mark.parametrize(
    "word_count, expected",
    [
        (  # No Word Content in Website
            0,
            (
                0,
                ["Body Content is too short"],
                [
                    "Lengthen your Content of your website",
                    "Make your Content of your website descriptive and definitive",
                ],
            ),
        ),
        (  # Very Short Word Content in Website
            200,
            (
                5,
                ["Body Content is too short"],
                [
                    "Lengthen your Content of your website",
                    "Make your Content of your website descriptive and definitive",
                ],
            ),
        ),
        (  # Proper Word Content in Website
            850,
            (20, ["Body Content of your website is of correct length"], []),
        ),
        (  # Long Word Content in Website
            3000,
            (
                7,
                ["Body Content of your website is too long."],
                [
                    "Make your website content specific and properly defined",
                    "Long Content is often classified as spam by AI Retrieval systems",
                ],
            ),
        ),
    ],
)
def test_score_word_count(word_count, expected):
    result = _score_word_count(word_count)
    assert result == expected


@pytest.mark.parametrize(
    "headings, expected",
    [
        (
            # Empty headings — all sub-checks fail
            [],
            (
                0,
                [
                    "Page has no H1 heading",
                    "Page has no headings",
                    "Page has no heading hierarchy",
                    "Headings are too long or empty",
                ],
                [
                    "Add a single descriptive H1 heading to define the page topic",
                    "Add headings (H1-H3) to structure your content for AI retrieval",
                    "Add H1 and H2 headings to establish content structure",
                    "Keep headings concise and focused (5-10 words)",
                ],
            ),
        ),
        (
            # Well-structured page
            [
                {"h1": "Complete Guide to Technical SEO Audits"},
                {"h2": "How to Analyze Website Structure"},
                {"h2": "Best Practices for Content Optimization"},
                {"h3": "Common Technical SEO Mistakes"},
            ],
            (
                40,
                [
                    "Page has a single well-defined H1 heading",
                    "Page has sufficient heading structure",
                    "Page has adequate heading hierarchy",
                    "Headings are well-defined and descriptive",
                ],
                [],
            ),
        ),
        (
            # Poorly structured page
            [
                {"h1": "Home"},
                {"h1": "About"},
            ],
            (
                20,
                [
                    "Page has multiple H1 headings",
                    "Page has minimal heading structure",
                    "Page lacks H2 hierarchy",
                    "Headings are too brief",
                ],
                [
                    "Use only one H1 heading per page for clear topic signaling",
                    "Add more headings to break content into scannable sections",
                    "Add H2 headings to create content sections for better chunking",
                    "Make headings more descriptive (aim for 5-10 words)",
                ],
            ),
        ),
    ],
)
def test_score_headings(headings, expected):
    result = _score_headings(headings)
    assert result == expected


@pytest.mark.parametrize(
    "body_text, expected",
    [
        (
            # No content
            None,
            (
                0,
                ["There is no content available on your website"],
                [
                    "You need to write content on your website",
                    "Without meaningful content you won't be placed in AI visibility",
                ],
            ),
        ),
        (
            # Low vocabulary diversity (ratio < 0.4)
            "seo seo seo seo seo seo content content content content",
            (
                8,
                ["Content is thin or repetitive"],
                [
                    "Rewrite content to be more substantive",
                    "Avoid keyword stuffing and repetitive phrases",
                ],
            ),
        ),
        (
            # Moderate vocabulary diversity (0.4 <= ratio <= 0.7)
            "seo content optimization ranking visibility retrieval ai content ranking and ranking in ai",
            (
                28,
                ["Content has moderate vocabulary diversity"],
                ["Enrich your content with more varied vocabulary and topics"],
            ),
        ),
        (
            # High vocabulary diversity (ratio > 0.7)
            "seo content optimization ranking visibility retrieval artificial intelligence systems",
            (
                40,
                ["Content is rich and diverse, ideal for AI retrieval"],
                [],
            ),
        ),
    ],
)
def test_score_body_content(body_text, expected):
    result = _score_body_content(body_text)
    assert result == expected


@pytest.mark.parametrize(
    "page, expected",
    [
        (
            # Everything missing
            ParsedPage(
                url="https://example.com",
                status_code=200,
                word_count=0,
                headings=[],
                body_text_content=None,
            ),
            CategoryScore(
                score=0,
                max_possible=100,
                metrics={
                    "word_count": 0,
                    "headings": 0,
                    "body_text_content": 0,
                },
                findings=[
                    "Body Content is too short",
                    "Page has no H1 heading",
                    "Page has no headings",
                    "Page has no heading hierarchy",
                    "Headings are too long or empty",
                    "There is no content available on your website",
                ],
                recommendations=[
                    "Lengthen your Content of your website",
                    "Make your Content of your website descriptive and definitive",
                    "Add a single descriptive H1 heading to define the page topic",
                    "Add headings (H1-H3) to structure your content for AI retrieval",
                    "Add H1 and H2 headings to establish content structure",
                    "Keep headings concise and focused (5-10 words)",
                    "You need to write content on your website",
                    "Without meaningful content you won't be placed in AI visibility",
                ],
            ),
        ),
        (
            # Everything optimized
            ParsedPage(
                url="https://example.com",
                status_code=200,
                word_count=850,
                headings=[
                    {"h1": "Complete Guide to Technical SEO Audits"},
                    {"h2": "How to Analyze Website Structure"},
                    {"h2": "Best Practices for Content Optimization"},
                    {"h3": "Common Technical SEO Mistakes"},
                ],
                body_text_content="seo content optimization ranking visibility retrieval",
            ),
            CategoryScore(
                score=100,
                max_possible=100,
                metrics={
                    "word_count": 20,
                    "headings": 40,
                    "body_text_content": 40,
                },
                findings=[
                    "Body Content of your website is of correct length",
                    "Page has a single well-defined H1 heading",
                    "Page has sufficient heading structure",
                    "Page has adequate heading hierarchy",
                    "Headings are well-defined and descriptive",
                    "Content is rich and diverse, ideal for AI retrieval",
                ],
                recommendations=[],
            ),
        ),
        (
            # Mixed quality page
            ParsedPage(
                url="https://example.com",
                status_code=200,
                word_count=200,
                headings=[
                    {"h1": "Home"},
                    {"h1": "About"},
                ],
                body_text_content="seo content optimization ranking visibility retrieval ai content ranking and ranking in ai",
            ),
            CategoryScore(
                score=53,
                max_possible=100,
                metrics={
                    "word_count": 5,
                    "headings": 20,
                    "body_text_content": 28,
                },
                findings=[
                    "Body Content is too short",
                    "Page has multiple H1 headings",
                    "Page has minimal heading structure",
                    "Page lacks H2 hierarchy",
                    "Headings are too brief",
                    "Content has moderate vocabulary diversity",
                ],
                recommendations=[
                    "Lengthen your Content of your website",
                    "Make your Content of your website descriptive and definitive",
                    "Use only one H1 heading per page for clear topic signaling",
                    "Add more headings to break content into scannable sections",
                    "Add H2 headings to create content sections for better chunking",
                    "Make headings more descriptive (aim for 5-10 words)",
                    "Enrich your content with more varied vocabulary and topics",
                ],
            ),
        ),
    ],
)
def test_score_content_quality(page, expected):
    result = _score_content_quality(page)
    assert result == expected


@pytest.mark.parametrize(
    "has_schema, expected",
    [
        (
            False,
            (
                0,
                ["No structured schema markup found"],
                ["Add JSON-LD schema markup to your pages"],
            ),
        ),
        (
            True,
            (
                20,
                ["Page has structured schema markup"],
                [],
            ),
        ),
    ],
)
def test_score_has_schema(has_schema, expected):
    result = _score_has_schema(has_schema)
    assert result == expected


@pytest.mark.parametrize(
    "schema_types, expected",
    [
        (
            # No schema types
            [],
            (
                0,
                ["No recognized schema types found"],
                ["Add high-value schema types like Article, Organization, or Product"],
            ),
        ),
        (
            # Basic coverage (score <= 10)
            ["WebPage", "Event"],
            (
                6,
                ["Basic schema types present"],
                ["Add more specific schema types to improve AI visibility"],
            ),
        ),
        (
            # Good coverage (10 < score <= 25)
            ["Organization", "Article", "BreadcrumbList", "WebPage"],
            (
                16,
                ["Good schema type coverage"],
                [],
            ),
        ),
        (
            # Excellent coverage (> 25)
            [
                "Product",
                "Organization",
                "Article",
                "BreadcrumbList",
                "LocalBusiness",
                "Person",
                "WebPage",
                "Event",
            ],
            (
                30,
                ["Excellent schema type coverage"],
                [],
            ),
        ),
    ],
)
def test_score_schema_types(schema_types, expected):
    result = _score_schema_types(schema_types)
    assert result == expected


@pytest.mark.parametrize(
    "faq_items, expected",
    [
        (
            # No FAQs
            [],
            (
                0,
                ["No FAQ schema found"],
                ["Add FAQPage schema to answer common questions directly"],
            ),
        ),
        (
            # Limited FAQs + short answers
            [
                FAQItem(
                    question="What is SEO?",
                    answer="Improves rankings",
                ),
                FAQItem(
                    question="Why use schema?",
                    answer="Better visibility",
                ),
            ],
            (
                18,
                [
                    "Limited FAQ coverage",
                    "FAQ answers are too brief",
                ],
                [
                    "Add more FAQ items to improve answer coverage",
                    "Expand FAQ answers to at least 10 words for AI citability",
                ],
            ),
        ),
        (
            # Good FAQ coverage + well-structured answers
            [
                FAQItem(
                    question=f"Question {i}",
                    answer="This answer contains exactly ten meaningful words for testing purposes.",
                )
                for i in range(6)
            ],
            (
                34,
                [
                    "Good FAQ Coverage",
                    "FAQ answers are well-structured",
                ],
                [],
            ),
        ),
        (
            # Excessive FAQ count + overly long answers
            [
                FAQItem(
                    question=f"Question {i}",
                    answer=" ".join(["word"] * 60),
                )
                for i in range(12)
            ],
            (
                36,
                [
                    "Excessive FAQ items",
                    "FAQ answers are too long",
                ],
                [
                    "Keep FAQ items focused and under 10 for best results",
                    "Keep FAQ answers concise (10-50 words) for better AI extraction",
                ],
            ),
        ),
    ],
)
def test_score_faq_items(faq_items, expected):
    result = _score_faq_items(faq_items)
    assert result == expected


@pytest.mark.parametrize(
    "page, expected",
    [
        (
            # Everything missing
            ParsedPage(
                url="https://example.com",
                status_code=200,
                has_schema=False,
                schema_types=[],
                faq_items=[],
            ),
            CategoryScore(
                score=0,
                max_possible=100,
                metrics={
                    "has_schema": 0,
                    "schema_types": 0,
                    "faq_items": 0,
                },
                findings=[
                    "No structured schema markup found",
                    "No recognized schema types found",
                    "No FAQ schema found",
                ],
                recommendations=[
                    "Add JSON-LD schema markup to your pages",
                    "Add high-value schema types like Article, Organization, or Product",
                    "Add FAQPage schema to answer common questions directly",
                ],
            ),
        ),
        (
            # Everything optimized
            ParsedPage(
                url="https://example.com",
                status_code=200,
                has_schema=True,
                schema_types=[
                    "Product",
                    "Organization",
                    "Article",
                    "BreadcrumbList",
                    "LocalBusiness",
                    "Person",
                    "WebPage",
                ],
                faq_items=[
                    FAQItem(
                        question=f"Question {i}",
                        answer="This answer contains exactly ten meaningful words for testing purposes.",
                    )
                    for i in range(6)
                ],
            ),
            CategoryScore(
                score=83, 
                max_possible=100,
                metrics={
                    "has_schema": 20,
                    "schema_types": 29,
                    "faq_items": 34,
                },
                findings=[
                    "Page has structured schema markup",
                    "Excellent schema type coverage",
                    "Good FAQ Coverage",
                    "FAQ answers are well-structured",
                ],
                recommendations=[],
            ),
        ),
        (
            # Mixed quality page
            ParsedPage(
                url="https://example.com",
                status_code=200,
                has_schema=True,
                schema_types=["WebPage", "Event"],
                faq_items=[
                    FAQItem(
                        question="What is SEO?",
                        answer="Improves rankings",
                    ),
                    FAQItem(
                        question="Why use schema?",
                        answer="Better visibility",
                    ),
                ],
            ),
            CategoryScore(
                score=44, 
                max_possible=100,
                metrics={
                    "has_schema": 20,
                    "schema_types": 6,
                    "faq_items": 18,
                },
                findings=[
                    "Page has structured schema markup",
                    "Basic schema types present",
                    "Limited FAQ coverage",
                    "FAQ answers are too brief",
                ],
                recommendations=[
                    "Add more specific schema types to improve AI visibility",
                    "Add more FAQ items to improve answer coverage",
                    "Expand FAQ answers to at least 10 words for AI citability",
                ],
            ),
        ),
    ],
)
def test_score_schema_quality(page, expected):
    result = _score_schema_quality(page)
    assert result == expected

@pytest.mark.parametrize(
    "internal_links, expected",
    [
        (
            # No internal links
            [],
            (
                0,
                ["Page has no internal links"],
                [
                    "Add internal links to connect your content and improve crawlability"
                ],
            ),
        ),
        (
            # Minimal internal linking
            [
                "/about",
                "/contact",
                "/services",
            ],
            (
                30,
                ["Page has minimal internal linking"],
                ["Add more internal links to improve site connectivity"],
            ),
        ),
        (
            # Good internal link coverage
            [f"/page-{i}" for i in range(10)],
            (
                50,  # round((10 / 20) * 100)
                ["Page has good internal link coverage"],
                [],
            ),
        ),
        (
            # Excessive internal links
            [f"/page-{i}" for i in range(25)],
            (
                90,  # round(100 - (25 - 20) * 2)
                ["Page has excessive internal links"],
                ["Keep internal links focused and relevant"],
            ),
        ),
    ],
)
def test_score_internal_links(internal_links, expected):
    result = _score_internal_links(internal_links)
    assert result == expected
    
@pytest.mark.parametrize(
    "page, expected",
    [
        (
            # No internal links
            ParsedPage(
                url="https://example.com",
                status_code=200,
                internal_links=[],
            ),
            CategoryScore(
                score=0,
                max_possible=100,
                metrics={
                    "internal_links": 0,
                },
                findings=[
                    "Page has no internal links",
                ],
                recommendations=[
                    "Add internal links to connect your content and improve crawlability",
                ],
            ),
        ),
        (
            # Healthy internal linking
            ParsedPage(
                url="https://example.com",
                status_code=200,
                internal_links=[f"/page-{i}" for i in range(10)],
            ),
            CategoryScore(
                score=50,
                max_possible=100,
                metrics={
                    "internal_links": 50,
                },
                findings=[
                    "Page has good internal link coverage",
                ],
                recommendations=[],
            ),
        ),
        (
            # Excessive internal linking
            ParsedPage(
                url="https://example.com",
                status_code=200,
                internal_links=[f"/page-{i}" for i in range(25)],
            ),
            CategoryScore(
                score=90,
                max_possible=100,
                metrics={
                    "internal_links": 90,
                },
                findings=[
                    "Page has excessive internal links",
                ],
                recommendations=[
                    "Keep internal links focused and relevant",
                ],
            ),
        ),
    ],
)
def test_score_connectivity(page, expected):
    result = _score_connectivity(page)
    assert result == expected
    
@pytest.mark.parametrize(
    "images_without_alt, expected",
    [
        (
            # All images have alt text
            0,
            (
                100,
                ["All images have alt text"],
                [],
            ),
        ),
        (
            # Small number missing alt text (<= 10)
            5,
            (
                75,  # round(100 - (5 / 10) * 50)
                ["5 images are missing alt text"],
                [
                    "Add descriptive alt text to all images for accessibility and AI understanding"
                ],
            ),
        ),
        (
            # Significant number missing alt text (11-20)
            15,
            (
                25,  # round(50 - ((15 - 10) / 10) * 50)
                ["15 images are missing alt text"],
                [
                    "Urgently add alt text — missing alt text severely impacts AI image understanding"
                ],
            ),
        ),
        (
            # Critical level (>20)
            25,
            (
                0,
                [
                    "Critical: majority of images missing alt text",
                    "25 images are missing alt text",
                ],
                [
                    "Audit all images and add descriptive alt text immediately"
                ],
            ),
        ),
    ],
)
def test_score_images_without_alt(images_without_alt, expected):
    result = _score_images_without_alt(images_without_alt)
    assert result == expected
    
@pytest.mark.parametrize(
    "page, expected",
    [
        (
            # Fully compliant
            ParsedPage(
                url="https://example.com",
                status_code=200,
                images_without_alt=0,
            ),
            CategoryScore(
                score=100,
                max_possible=100,
                metrics={
                    "images_without_alt": 100,
                },
                findings=[
                    "All images have alt text",
                ],
                recommendations=[],
            ),
        ),
        (
            # Moderate issues
            ParsedPage(
                url="https://example.com",
                status_code=200,
                images_without_alt=5,
            ),
            CategoryScore(
                score=75,
                max_possible=100,
                metrics={
                    "images_without_alt": 75,
                },
                findings=[
                    "5 images are missing alt text",
                ],
                recommendations=[
                    "Add descriptive alt text to all images for accessibility and AI understanding",
                ],
            ),
        ),
        (
            # Critical issues
            ParsedPage(
                url="https://example.com",
                status_code=200,
                images_without_alt=25,
            ),
            CategoryScore(
                score=0,
                max_possible=100,
                metrics={
                    "images_without_alt": 0,
                },
                findings=[
                    "Critical: majority of images missing alt text",
                    "25 images are missing alt text",
                ],
                recommendations=[
                    "Audit all images and add descriptive alt text immediately",
                ],
            ),
        ),
    ],
)
def test_score_technical_compliance(page, expected):
    result = _score_technical_compliance(page)
    assert result == expected