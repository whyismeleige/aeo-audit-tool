import pytest
from bs4 import BeautifulSoup

from app.core.parser import _extract_title, _extract_sections, _extract_meta_description, _extract_meta_robots, _extract_canonical_url, _extract_headers, _extract_body_text, _extract_word_count, _extract_internal_links, _extract_images_without_alt, parse
from app.core.crawler import CrawlResult

def make_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")

@pytest.mark.parametrize("html, expected",[
    ('''
        <html>
            <head>
                <title>Title of the Page</title>
            </head>
        </html>
    ''', "Title of the Page"),
    ('''
        <html>
            <head>
                <title></title>
            </head>
        </html>
    ''', None),
    ('''
        <html>
            <head>
            </head>
        </html>
    ''', None),
]) 
def test_extract_title(html, expected):
    soup = make_soup(html)
    result = _extract_title(soup)
    assert result == expected

@pytest.mark.parametrize("html, expected",[
    ('''
        <html>
            <head>
                <meta name="description" content="Meta Description Content" />
            </head>
        </html>
    ''', "Meta Description Content"),
    ('''
        <html>
            <head>
                <meta name="description" />
            </head>
        </html>
    ''', None),
    ('''
        <html>
            <head>
            </head>
        </html>
    ''', None),
]) 
def test_extract_meta_description(html, expected):
    soup = make_soup(html)
    result = _extract_meta_description(soup)
    assert result == expected
    
@pytest.mark.parametrize("html, expected",[
    ('''
        <html>
            <head>
                <meta name="robots" content="Meta Robots Content" />
            </head>
        </html>
    ''', "Meta Robots Content"),
    ('''
        <html>
            <head>
                <meta name="robots" />
            </head>
        </html>
    ''', None),
    ('''
        <html>
            <head>
            </head>
        </html>
    ''', None),
]) 
def test_extract_meta_robots(html, expected):
    soup = make_soup(html)
    result = _extract_meta_robots(soup)
    assert result == expected

@pytest.mark.parametrize("html, expected",[
    ('''
        <html>
            <head>
                <link rel="canonical" href="https://example.com/blog" />
            </head>
        </html>
    ''', "https://example.com/blog"),
    ('''
        <html>
            <head>
                <link rel="canonical" />
            </head>
        </html>
    ''', None),
    ('''
        <html>
            <head>
            </head>
        </html>
    ''', None),
]) 
def test_extract_canonical_url(html, expected):
    soup = make_soup(html)
    result = _extract_canonical_url(soup)
    assert result == expected
    
@pytest.mark.parametrize("html, expected",[
    ('''
        <html>
            <body>
                <h1>Heading 1</h1>
                <h2>Heading 2</h2>
                <h3>Heading 3</h3>
                <h4>Heading 4</h4>
                <h5>Heading 5</h5>
                <h6>Heading 6</h6>                
            </body>
        </html>
    ''', [{"h1": "Heading 1"}, 
          {"h2": "Heading 2"}, 
          {"h3": "Heading 3"}, 
          {"h4": "Heading 4"},
          {"h5": "Heading 5"}, 
          {"h6": "Heading 6"}]),
    ('''
        <html>
            <body>
                <h1>     Heading 1     </h1>
            </body>
        </html>
    ''', [{"h1": "Heading 1"}]),
    ('''
        <html>
            <body>
                <h1>Heading 1</h1>
                <h2>Heading 2</h2>
                <h2>Heading 2</h2>
                <h3>Heading 3</h3>
                <h4>Heading 4</h4>
                <h5>Heading 5</h5>
                <h5>Heading 5</h5>
                <h6>Heading 6</h6>                
            </body>
        </html>
    ''', [{"h1": "Heading 1"}, 
          {"h2": "Heading 2"}, 
          {"h2": "Heading 2"}, 
          {"h3": "Heading 3"}, 
          {"h4": "Heading 4"},
          {"h5": "Heading 5"}, 
          {"h5": "Heading 5"}, 
          {"h6": "Heading 6"}]),
    ('''
        <html>
            <body>
                <h1>Heading 1</h1>
                    <h2>Heading 2</h2>
                <h1>Heading 1</h1>
                    <h2>Heading 2</h2>
                        <h3>Heading 3</h3>
                    <h2>Heading 2</h2>
                        <h3>Heading 3</h3>
                <h1>Heading 1</h1>
                    <h2>Heading 2</h2>                
            </body>
        </html>
    ''', [{"h1": "Heading 1"}, 
          {"h2": "Heading 2"},
          {"h1": "Heading 1"}, 
          {"h2": "Heading 2"},  
          {"h3": "Heading 3"}, 
          {"h2": "Heading 2"}, 
          {"h3": "Heading 3"},
          {"h1": "Heading 1"}, 
          {"h2": "Heading 2"}, 
          ]),
    ("", []),
    ('''
        <html>
            <body>
                <h1>Heading 1</h1>
                <div>
                    <h2>Heading 2</h2>
                </div>
                <section>
                    <h3>Heading 3</h3>
                    <h4>Heading 4</h4>
                </section>
                <h5>Heading 5</h5>
                <h6>Heading 6</h6>                
            </body>
        </html>
    ''', [{"h1": "Heading 1"}, 
          {"h2": "Heading 2"}, 
          {"h3": "Heading 3"}, 
          {"h4": "Heading 4"},
          {"h5": "Heading 5"}, 
          {"h6": "Heading 6"}]),
]) 
def test_extract_headers(html, expected):
    soup = make_soup(html)
    result = _extract_headers(soup)
    assert result == expected
    

@pytest.mark.parametrize("html, expected",[
    ('''
        <html>
            <body>
                <p>Content Outside Main</p>
                <main>Content Inside Main</main>                
            </body>
        </html>
    ''', "Content Inside Main"),
    ('''
        <html>
            <body>
                <p>Content Example 1</p>
                <p>Content Example 2</p>                
            </body>
        </html>
    ''', "Content Example 1 Content Example 2"),
    ('''
        <html>
            <head>
                <title>Title of the page</title>                
            </head>
        </html>
    ''', None),
    ('''
        <html>
            <body>
                <main>
                    <header>Header Content</header>
                    <p>Example Content in Main</p>
                    <nav>Navbar Content</nav>
                    <h1>Heading 1 Content</h1>
                    <footer>Footer Content</footer>
                    <script>Script Tag Content</script>
                </main>                
            </body>
        </html>
    ''', "Example Content in Main Heading 1 Content"),
    ('''
        <html>
            <body>
                <main>
                    <p>Example Content in Main</p>
                    <p class="ad">Sample Ad Class in Main</p>
                    <h1>Heading 1 Content</h1>
                    <div class="sponsored" >Sponsored Content in Content</div>
                    <span>Span Tag Content</span>
                </main>                
            </body>
        </html>
    ''', "Example Content in Main Heading 1 Content Span Tag Content"),
    ('''
        <html>
            <body>
                <main>
                    <h1>         Heading Content with whitespace       </h1>
                    <p>    Paragraph Content with extra space          </p>
                </main>                
            </body>
        </html>
    ''', "Heading Content with whitespace Paragraph Content with extra space"),
]) 
def test_extract_body_text(html, expected):
    soup = make_soup(html)
    result = _extract_body_text(soup)
    assert result == expected
    
@pytest.mark.parametrize("body_text, expected", [
    ("Hello World, This is a Sample Text", 7),
    ("", 0),
    (None, 0)
])
def test_extract_word_count(body_text, expected):
    result = _extract_word_count(body_text)
    assert result == expected
    
@pytest.mark.parametrize("html, base_url, expected", [
    ("""
    <html>
        <body>
            <a href="/about">About</a>
            <a href="/blog">Blog</a>
        </body>
    </html>
    """, "https://example.com", ["https://example.com/about", "https://example.com/blog"]),
    ("""
    <html>
        <body>
            <a href="/about">About</a>
            <a href="/blog">Blog</a>
            <a href="https://google.com">Google</a>
        </body>
    </html>
    """, "https://example.com", ["https://example.com/about", "https://example.com/blog"]),
    ("""
    <html>
        <body>
            <a href="/about">About</a>
            <a href="">Blog</a>
        </body>
    </html>
    """, "https://example.com", ["https://example.com/about", "https://example.com"]),
    ("""
    <html>
        <body>
        </body>
    </html>
    """, "https://example.com", []),
])    
def test_internal_links(html, base_url, expected):
    soup = make_soup(html)
    result = _extract_internal_links(soup, base_url)
    assert result == expected
    
@pytest.mark.parametrize("html, expected", [
    ("""
    <html>
        <body>
            <img alt="Alt Text 1" />
            <img alt="Alt Text 2" />
            <img alt="Alt Text 3" />
        </body>
    </html>
    """, 0),
    ("""
    <html>
        <body>
            <img alt="" />
            <img alt="" />
            <img alt="" />
            <img alt="Image with Alt text" />
        </body>
    </html>
    """, 3),
    ("""
    <html>
        <body>
            <img />
            <img />
            <img />
            <img alt="Image with Alt text" />
        </body>
    </html>
    """, 3),
    ("""
    <html>
        <body>
        </body>
    </html>
    """, 0),
])    
def test_images_without_alt(html, expected):
    soup = make_soup(html)
    result = _extract_images_without_alt(soup)
    assert result == expected

@pytest.mark.parametrize("html, expected", [
    # Simple case: one heading with paragraphs
    (
        """
        <html>
            <body>
                <h1>Title</h1>
                <p>Paragraph 1</p>
                <p>Paragraph 2</p>
            </body>
        </html>
        """,
        [
            {"heading": "Title", "content": "Paragraph 1 Paragraph 2"}
        ],
    ),

    # Multiple headings, each section should stop at next heading
    (
        """
        <html>
            <body>
                <h1>Section 1</h1>
                <p>Content 1</p>

                <h2>Section 2</h2>
                <p>Content 2</p>
                <p>More Content 2</p>
            </body>
        </html>
        """,
        [
            {"heading": "Section 1", "content": "Content 1"},
            {"heading": "Section 2", "content": "Content 2 More Content 2"},
        ],
    ),

    # Nested elements inside siblings (div/span)
    (
        """
        <html>
            <body>
                <h1>Main</h1>
                <div>
                    <p>Inside div</p>
                    <span>Span text</span>
                </div>
            </body>
        </html>
        """,
        [
            {"heading": "Main", "content": "Inside div Span text"}
        ],
    ),

    # Should stop when next heading appears even if nested structure exists
    (
        """
        <html>
            <body>
                <h1>First</h1>
                <p>A</p>
                <div>Still A</div>

                <h2>Second</h2>
                <p>B</p>
            </body>
        </html>
        """,
        [
            {"heading": "First", "content": "A Still A"},
            {"heading": "Second", "content": "B"},
        ],
    ),

    # Empty content between headings
    (
        """
        <html>
            <body>
                <h1>Only Heading</h1>
            </body>
        </html>
        """,
        [
            {"heading": "Only Heading", "content": ""}
        ],
    ),

    # Multiple headings at same level
    (
        """
        <html>
            <body>
                <h1>A</h1>
                <p>1</p>
                <h1>B</h1>
                <p>2</p>
            </body>
        </html>
        """,
        [
            {"heading": "A", "content": "1"},
            {"heading": "B", "content": "2"},
        ],
    ),
])
def test_extract_sections(html, expected):
    soup = make_soup(html)
    result = _extract_sections(soup)

    assert len(result) == len(expected)

    for r, e in zip(result, expected):
        assert r.heading == e["heading"]
        assert r.content == e["content"]

html_content = """
    <html>
        <head>
            <title>Title of the Page</title>
            <meta name="description" content="Meta Description Content" />
            <meta name="robots" content="Meta Robots Content" />
            <link rel="canonical" href="https://example.com" />
        </head>
        <body>
            <h1>Heading 1</h1>
            <h2>Heading 2</h2>
            
            <img alt="" />
            <img alt="" />
            <img alt="" />
            <img alt="Image with Alt text" />
            
            <a href="/about">About</a>
            <a href="/blog">Blog</a>
            
            <header>Header Content</header>
            <p>Example Content in Main</p>
            <nav>Navbar Content</nav>
            <footer>Footer Content</footer>
            <script>Script Tag Content</script>
        </body>
    </html>
"""

crawl_result = CrawlResult("https://example.com", html_content, 200)

def test_parse():
    parsed_result = parse(crawl_result)
    
    assert parsed_result.title == "Title of the Page"
    assert parsed_result.word_count == 10
    assert parsed_result.images_without_alt == 3
    assert parsed_result.internal_links == ["https://example.com/about", "https://example.com/blog"]
    assert parsed_result.canonical_url == "https://example.com"
    assert parsed_result.body_text_content ==  "Heading 1 Heading 2 About Blog Example Content in Main"
    assert parsed_result.headings == [{"h1": "Heading 1"}, {"h2": "Heading 2"}]
    
