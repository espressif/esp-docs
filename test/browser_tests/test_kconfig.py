"""Browser tests for the Kconfig reference page enhancements."""

import os

from playwright.sync_api import Page, expect


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
KCONFIG_JS_FILE = os.path.realpath(
    os.path.join(CURRENT_DIR, '../../src/esp_docs/_static/kconfig.js')
)


def load_nested_kconfig_page(page: Page):
    page.set_content(
        """
        <style>.kconfig-option-hidden { display: none; }</style>
        <section id="configuration-options-reference">
          <h1>Configuration Options Reference</h1>
          <section id="component-config">
            <h2>Component config</h2>
            <span id="config-parent"></span>
            <section id="config-parent-1">
              <h3>CONFIG_PARENT</h3>
              <p>Parent option</p>
              <span id="config-child"></span>
              <section id="config-child-1">
                <h4>CONFIG_CHILD</h4>
                <p>Nested child option</p>
              </section>
            </section>
          </section>
        </section>
        """
    )
    page.add_script_tag(path=KCONFIG_JS_FILE)


def test_nested_options_are_flattened_into_sibling_cards(page: Page):
    load_nested_kconfig_page(page)

    cards = page.locator('.kconfig-card-list > .kconfig-option')
    expect(cards).to_have_count(2)
    expect(cards.nth(0).locator('h3')).to_have_text('CONFIG_PARENT')
    expect(cards.nth(1).locator('h4')).to_have_text('CONFIG_CHILD')


def test_nested_option_can_be_filtered_independently(page: Page):
    load_nested_kconfig_page(page)

    search = page.locator('.kconfig-filter')
    search.fill('nested child')
    page.wait_for_timeout(200)

    visible_cards = page.locator('.kconfig-card-list > .kconfig-option:visible')
    expect(visible_cards).to_have_count(1)
    expect(visible_cards.locator('h4')).to_have_text('CONFIG_CHILD')
