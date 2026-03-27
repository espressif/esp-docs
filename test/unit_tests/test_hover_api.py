#!/usr/bin/env python3

import os
import re
import subprocess
import unittest
from urllib.parse import urljoin
from unittest.mock import MagicMock

from esp_docs.generic_extensions import hover_api

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DOXYGEN_EXAMPLE_DIR = os.path.realpath(os.path.join(CURRENT_DIR, '../../examples/doxygen'))
JS_FILE = os.path.realpath(os.path.join(CURRENT_DIR, '../../src/esp_docs/_static/hover_api.js'))


class TestHoverApiSetup(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()

    def test_setup_registers_config_value(self):
        hover_api.setup(self.app)
        self.app.add_config_value.assert_called_once_with('esp_hover_api_enable', False, 'html')

    def test_setup_connects_config_inited(self):
        hover_api.setup(self.app)
        self.app.connect.assert_called_once_with('config-inited', hover_api._add_assets)

    def test_setup_returns_metadata(self):
        result = hover_api.setup(self.app)
        self.assertTrue(result['parallel_read_safe'])
        self.assertTrue(result['parallel_write_safe'])
        self.assertIn('version', result)


class TestAddAssets(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()

    def test_assets_added_when_enabled(self):
        config = MagicMock()
        config.esp_hover_api_enable = True
        hover_api._add_assets(self.app, config)
        self.app.add_js_file.assert_called_once_with('hover_api.js')
        self.app.add_css_file.assert_called_once_with('hover_api.css')

    def test_assets_not_added_when_disabled(self):
        config = MagicMock()
        config.esp_hover_api_enable = False
        hover_api._add_assets(self.app, config)
        self.app.add_js_file.assert_not_called()
        self.app.add_css_file.assert_not_called()

    def test_assets_not_added_when_not_set(self):
        config = MagicMock()
        config.esp_hover_api_enable = None
        hover_api._add_assets(self.app, config)
        self.app.add_js_file.assert_not_called()
        self.app.add_css_file.assert_not_called()


class TestHoverApiJsRecursiveTooltips(unittest.TestCase):
    """Regression tests for the recursive-tooltip URL resolution bug.

    The bug: hrefs inside fetched tooltip content were left relative, so when a
    level-1 tooltip tried to fetch them it resolved against the current page URL
    instead of the source page — giving the wrong fetch target.

    The fix lives entirely in hover_api.js (extractFragment and loadTooltip).
    We test it here by:
      1. Asserting the JS source contains the fix patterns.
      2. Verifying the URL resolution arithmetic with Python's urljoin, which has
         identical semantics to the browser's `new URL(href, base).href`.
    """

    @classmethod
    def setUpClass(cls):
        with open(JS_FILE) as f:
            cls.js_source = f.read()

    # ------------------------------------------------------------------
    # Source-level checks — catch regressions if the fix is ever reverted
    # ------------------------------------------------------------------

    def test_extract_fragment_rewrites_hrefs_with_base_url(self):
        """extractFragment must call new URL(href, baseUrl) to make hrefs absolute."""
        self.assertIn(
            'new URL(href, baseUrl)',
            self.js_source,
            'extractFragment must rewrite hrefs to absolute URLs using baseUrl; '
            'recursive tooltips will fetch the wrong page if this is missing.',
        )

    def test_load_tooltip_normalises_page_url(self):
        """loadTooltip must normalise the page URL to absolute before caching/fetching."""
        self.assertIn(
            'new URL(href.slice(0, hashIdx), window.location.href).href',
            self.js_source,
            'loadTooltip must normalise pageUrl to an absolute URL; '
            'the cache key will be unstable and relative hrefs will resolve wrong otherwise.',
        )

    def test_load_tooltip_passes_base_url_for_same_page_anchors(self):
        """loadTooltip must pass window.location.href as baseUrl when extracting same-page
        anchors so that relative hrefs inside the dl are rewritten to absolute URLs,
        making them work correctly when followed at level > 0."""
        self.assertIn(
            'extractFragment(document, anchorId, window.location.href)',
            self.js_source,
        )

    def test_show_tooltip_attaches_listeners_via_anchor_id_prefix_selector(self):
        """showTooltip must attach recursive listeners using the anchor ID prefix selector.

        Sphinx C domain generates anchor IDs with the prefix "c." (e.g. "#c.my_func"),
        and C++ domain uses "_CPPv" (e.g. "#_CPPv413random_numberii"). Matching on these
        href substrings works for both Sphinx-prose xref links and Breathe function-
        signature type links (which have no code.xref child), and naturally excludes
        non-API internal links such as prose sections, glossary entries, and Python docs."""
        self.assertIn(
            'href*="#c."',
            self.js_source,
            'showTooltip must select C-domain links via [href*="#c."]',
        )
        self.assertIn(
            'href*="#_CPPv"',
            self.js_source,
            'showTooltip must select C++-domain links via [href*="#_CPPv"]',
        )

    # ------------------------------------------------------------------
    # URL resolution arithmetic (Python urljoin == browser new URL(rel, base))
    # ------------------------------------------------------------------

    def test_relative_href_resolves_against_source_page_not_current_page(self):
        """A relative href from fetched content must be resolved against that page's URL."""
        source_page = 'https://example.com/en/esp32/api-reference/myapi.html'
        href_in_content = 'other.html#other_func'

        resolved = urljoin(source_page, href_in_content)

        self.assertEqual(resolved, 'https://example.com/en/esp32/api-reference/other.html#other_func')
        # Contrast: if incorrectly resolved against the current page in a subdir:
        wrong_base = 'https://example.com/en/esp32/html/index.html'
        self.assertNotEqual(urljoin(wrong_base, href_in_content), resolved,
                            'Resolution against the wrong base must produce a different (wrong) URL')

    def test_dotdot_relative_href_resolves_correctly(self):
        source_page = 'https://example.com/en/esp32/api/module.html'
        href_in_content = '../other-section/page.html#sym'
        resolved = urljoin(source_page, href_in_content)
        self.assertEqual(resolved, 'https://example.com/en/esp32/other-section/page.html#sym')

    def test_absolute_href_is_unchanged_by_resolution(self):
        source_page = 'https://example.com/en/esp32/api/module.html'
        href_in_content = 'https://example.com/en/esp32/other.html#sym'
        self.assertEqual(urljoin(source_page, href_in_content), href_in_content)

    def test_load_tooltip_short_circuits_fetch_for_current_page(self):
        """loadTooltip must use document directly when pageUrl equals the current page,
        not go through fetch().

        Broken scenario without this fix:
          1. Level-0: user hovers a same-page link (#anchor) on index.html.
                hashIdx === 0  →  uses document directly, does NOT populate pageCache.
          2. extractFragment rewrites the tooltip's inner hrefs to absolute:
                #TypeId  →  https://docs.example.com/index.html#TypeId
          3. Level-1: user hovers that rewritten link.
                loadTooltip receives "https://docs.example.com/index.html#TypeId".
                hashIdx > 0  →  cross-page branch.
                pageUrl = "https://docs.example.com/index.html" — not in pageCache.
                fetch("https://docs.example.com/index.html") is attempted.
                On file:// builds this is blocked by the browser; no tooltip appears.

        The fix: before the fetch, detect that pageUrl is the current page and use
        document directly (same as the hashIdx === 0 branch does for raw same-page anchors).
        """
        self.assertIn(
            "window.location.href.split('#')[0]",
            self.js_source,
            'loadTooltip must derive the current page URL via '
            "window.location.href.split('#')[0] and short-circuit to document "
            'when pageUrl matches, instead of going through fetch(). '
            'Without this, level-1 hover on a same-page link fails silently on '
            'file:// builds because fetch() is blocked for local files.',
        )

    def test_level1_tooltip_reuses_level0_cache_entry(self):
        """After extractFragment rewrites hrefs to absolute, the level-1 fetch key
        must be identical to the absolute key used by the level-0 fetch."""
        current_page = 'https://example.com/en/esp32/html/index.html'
        source_page = 'https://example.com/en/esp32/api/module.html'

        # Level-0: relative href on the current page → normalised to absolute cache key
        level0_relative = '../api/module.html'
        level0_key = urljoin(current_page, level0_relative)
        self.assertEqual(level0_key, source_page)

        # extractFragment rewrites child hrefs to absolute using source_page as base.
        # A same-page link "#func_b" becomes absolute:
        child_href_after_rewrite = urljoin(source_page, '#func_b')
        # Level-1 calls loadTooltip with this absolute href; page part is source_page itself.
        level1_page_part = child_href_after_rewrite.split('#')[0]
        level1_key = urljoin(current_page, level1_page_part)  # new URL(abs, base) == abs

        self.assertEqual(level1_key, level0_key,
                         'Level-1 must hit the same cache entry as level-0')


class TestHoverApiHtmlOutput(unittest.TestCase):
    """Build the doxygen example and verify the HTML contains the CSS selectors
    that hover_api.js relies on to find API reference links."""

    BUILD_DIR = os.path.join(DOXYGEN_EXAMPLE_DIR, '_build/test_hover_api')
    HTML_FILE = os.path.join(BUILD_DIR, 'en/esp32/html/index.html')

    # Matches <a class="reference internal" href="...#c.SYMBOL"> (C domain)
    # or      <a class="reference internal" href="...#_CPPvNNN"> (C++ domain)
    # This is what hover_api.js targets with: [href*="#c."] and [href*="#_CPPv"]
    C_DOMAIN_HREF_PATTERN = re.compile(
        r'<a\b[^>]*\bclass="[^"]*\breference\s+internal\b[^"]*"[^>]*'
        r'\bhref="[^"]*#c\.[^"]*"',
    )
    CPP_DOMAIN_HREF_PATTERN = re.compile(
        r'<a\b[^>]*\bclass="[^"]*\breference\s+internal\b[^"]*"[^>]*'
        r'\bhref="[^"]*#_CPPv[^"]*"',
    )

    @classmethod
    def setUpClass(cls):
        ret = subprocess.call(
            ['build-docs', '-b', cls.BUILD_DIR, '-t', 'esp32', '-l', 'en', '--project-path', 'src/'],
            cwd=DOXYGEN_EXAMPLE_DIR
        )
        cls.build_failed = ret != 0

    def setUp(self):
        if self.build_failed:
            self.fail('Doxygen example build failed')

    def test_api_links_have_c_or_cpp_domain_anchor_hrefs(self):
        """hover_api.js selects links by href prefix: [href*="#c."] for C domain and
        [href*="#_CPPv"] for C++ domain — verify Sphinx/Breathe still emits these anchor
        ID patterns so tooltips will be attached."""
        with open(self.HTML_FILE) as f:
            content = f.read()
        has_c = self.C_DOMAIN_HREF_PATTERN.search(content) is not None
        has_cpp = self.CPP_DOMAIN_HREF_PATTERN.search(content) is not None
        self.assertTrue(
            has_c or has_cpp,
            'No a.reference.internal with href containing "#c." or "#_CPPv" found in '
            'built HTML. hover_api.js will not attach tooltips to any links.'
        )

    # ------------------------------------------------------------------
    # Helpers — simulate extractFragment and querySelectorAll in Python
    # ------------------------------------------------------------------

    def _extract_dl_html(self, html, anchor_id):
        """Return the outer HTML of the <dl> enclosing the element with anchor_id."""
        m = re.search(r'<[^>]+\bid="' + re.escape(anchor_id) + r'"[^>]*>', html)
        if not m:
            return None
        before = html[:m.start()]
        dl_start = max(before.rfind('<dl '), before.rfind('<dl>'))
        if dl_start < 0:
            return None
        chunk = html[dl_start:]
        depth = i = 0
        while i < len(chunk):
            if chunk[i:i + 3] == '<dl':
                depth += 1
                i += 3
            elif chunk[i:i + 5] == '</dl>':
                depth -= 1
                if depth == 0:
                    return chunk[:i + 5]
                i += 5
            else:
                i += 1
        return None

    def _css_count(self, html, selector):
        """Count elements matching a CSS selector (stdlib-only implementation).
        Handles tag.class1.class2[attr*="val"] and comma-separated groups."""
        total = 0
        for simple in selector.split(','):
            simple = simple.strip()
            tag_m = re.match(r'^(\w+)', simple)
            tag = tag_m.group(1) if tag_m else r'\w+'
            classes = re.findall(r'\.([a-zA-Z][\w-]*)', simple)
            attr_subs = re.findall(r'\[(\w+)\*="([^"]+)"\]', simple)
            for open_tag in re.finditer(r'<' + tag + r'\b([^>]*)>', html):
                attrs = open_tag.group(1)
                cls_m = re.search(r'\bclass="([^"]*)"', attrs)
                elem_cls = cls_m.group(1).split() if cls_m else []
                if not all(c in elem_cls for c in classes):
                    continue
                if all(
                    (am := re.search(r'\b' + an + r'="([^"]*)"', attrs)) and val in am.group(1)
                    for an, val in attr_subs
                ):
                    total += 1
        return total

    # ------------------------------------------------------------------
    # Behavioral test: selector must find targets in real tooltip content
    # ------------------------------------------------------------------

    def test_show_tooltip_selector_finds_targets_in_breathe_dl(self):
        """The querySelectorAll selector used in showTooltip must match at least one
        element inside a real Breathe-generated tooltip dl.

        This is the end-to-end proof: if no elements match, attachHoverListeners is
        never called inside any tooltip and recursive hover silently does nothing.

        Breathe renders function-signature type links as:
            <a class="reference internal" href="#..."><span class="n">TypeName</span></a>
        These have NO code.xref child. The old selector 'code.xref.cpp, code.xref.c'
        returned 0 matches everywhere — recursive hover was broken for every tooltip.
        """
        # The selector is defined by the two href-prefix patterns used in showTooltip.
        selector = 'a.reference.internal[href*="#c."], a.reference.internal[href*="#_CPPv"]'

        with open(self.HTML_FILE) as f:
            html = f.read()

        # random_number_init returns my_api_err_t and takes my_rng_config_t —
        # both appear as <a class="reference internal" href="#..."> in the signature.
        func_id = '_CPPv418random_number_initPK15my_rng_config_t'
        dl_html = self._extract_dl_html(html, func_id)
        self.assertIsNotNone(dl_html, f'Could not find <dl> for {func_id} in built HTML')

        # Simulate extractFragment's href rewriting (relative → absolute)
        base_url = 'https://test.local/en/esp32/html/index.html'
        dl_html = re.sub(
            r'href="([^"]*)"',
            lambda m: 'href="' + urljoin(base_url, m.group(1)) + '"',
            dl_html,
        )

        count = self._css_count(dl_html, selector)
        self.assertGreater(
            count, 0,
            f'Selector "{selector}" matched 0 elements in the tooltip <dl> for '
            f'{func_id}. Recursive hover silently does nothing.\n'
            f'Breathe emits <a class="reference internal"> for type cross-references '
            f'in function signatures — the selector must match those elements.',
        )


if __name__ == '__main__':
    unittest.main()
