"""
Browser tests for hover_api.js using Playwright.

Run with:  pytest test/browser_tests/ --browser chromium
CI installs:  pip install pytest-playwright && playwright install --with-deps chromium
"""

import pytest
from playwright.sync_api import Page, expect

# Must match HOVER_DELAY_MS in hover_api.js (280 ms) plus a small margin.
TOOLTIP_TIMEOUT_MS = 2_000
# Grace period for tooltip hide (GRACE_MS = 80 ms) plus margin.
HIDE_TIMEOUT_MS = 500


@pytest.fixture(autouse=True)
def navigate(page: Page, docs_server: str):
    """Load the doxygen example index page before each test."""
    page.goto(f'{docs_server}/index.html')
    # Wait for JS to initialise (hover listeners attached on DOMContentLoaded)
    page.wait_for_load_state('domcontentloaded')


# ---------------------------------------------------------------------------
# Level-0 tooltip
# ---------------------------------------------------------------------------

def test_level0_tooltip_appears_on_hover(page: Page):
    """Hovering a C/C++ xref link shows a level-0 tooltip."""
    link = page.locator('a.reference.internal code.xref').first
    link.hover()
    expect(page.locator('.esp-hover-tooltip').first).to_be_visible(timeout=TOOLTIP_TIMEOUT_MS)


def test_level0_tooltip_contains_dl(page: Page):
    """The level-0 tooltip wraps the API symbol's <dl> definition block."""
    link = page.locator('a.reference.internal code.xref').first
    link.hover()
    tooltip = page.locator('.esp-hover-tooltip').first
    expect(tooltip).to_be_visible(timeout=TOOLTIP_TIMEOUT_MS)
    expect(tooltip.locator('dl').first).to_be_visible()


def test_level0_tooltip_hides_when_mouse_leaves(page: Page):
    """The tooltip disappears after the mouse moves away from both link and tooltip."""
    link = page.locator('a.reference.internal code.xref').first
    link.hover()
    tooltip = page.locator('.esp-hover-tooltip').first
    expect(tooltip).to_be_visible(timeout=TOOLTIP_TIMEOUT_MS)

    # Move to a neutral position far from the tooltip
    page.mouse.move(0, 0)
    expect(tooltip).not_to_be_visible(timeout=HIDE_TIMEOUT_MS)


# ---------------------------------------------------------------------------
# Level-1 recursive tooltip — this is the behaviour that was broken
# ---------------------------------------------------------------------------

def test_recursive_hover_shows_level1_tooltip(page: Page):
    """Hovering a link inside a level-0 tooltip shows a level-1 tooltip.

    This is the core recursive-hover regression test.  Two bugs had to be fixed:
      1. showTooltip used a selector that never matched Breathe-generated signature
         links (<a><span class="n">Type</span></a>, no code.xref child). Now fixed
         by matching on anchor ID prefix: [href*="#c."] and [href*="#_CPPv"].
      2. loadTooltip went through fetch() even when the target was the current
         page, which is blocked on file:// builds.
    """
    # Open level-0 tooltip
    link = page.locator('a.reference.internal code.xref').first
    link.hover()
    level0 = page.locator('.esp-hover-tooltip').nth(0)
    expect(level0).to_be_visible(timeout=TOOLTIP_TIMEOUT_MS)

    # The tooltip must contain at least one hoverable internal link
    inner_link = level0.locator('a.reference.internal[href*="#"]').first
    expect(inner_link).to_be_attached()  # must exist in DOM

    # Hovering it must produce a level-1 tooltip
    inner_link.hover()
    level1 = page.locator('.esp-hover-tooltip').nth(1)
    expect(level1).to_be_visible(timeout=TOOLTIP_TIMEOUT_MS)


def test_level1_tooltip_contains_dl(page: Page):
    """The level-1 tooltip also wraps a proper API <dl> block."""
    link = page.locator('a.reference.internal code.xref').first
    link.hover()
    level0 = page.locator('.esp-hover-tooltip').nth(0)
    expect(level0).to_be_visible(timeout=TOOLTIP_TIMEOUT_MS)

    inner_link = level0.locator('a.reference.internal[href*="#"]').first
    inner_link.hover()
    level1 = page.locator('.esp-hover-tooltip').nth(1)
    expect(level1).to_be_visible(timeout=TOOLTIP_TIMEOUT_MS)
    expect(level1.locator('dl').first).to_be_visible()


def test_level0_stays_visible_while_hovering_level1_link(page: Page):
    """The level-0 tooltip must stay open while the mouse is over a nested link."""
    link = page.locator('a.reference.internal code.xref').first
    link.hover()
    level0 = page.locator('.esp-hover-tooltip').nth(0)
    expect(level0).to_be_visible(timeout=TOOLTIP_TIMEOUT_MS)

    inner_link = level0.locator('a.reference.internal[href*="#"]').first
    inner_link.hover()
    # Level-0 must still be visible
    expect(level0).to_be_visible()
