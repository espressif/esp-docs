#!/usr/bin/env bash
# This test expects lang-linkcheck to fail because:
# - incorrect_page.rst has incorrect links (English file links to English, Chinese file links to Chinese)
# - multiple_links_page.rst has multiple links (should only have one)
# - page_without_link.rst is missing translation links
#
# This test also verifies:
# - page_ignored_by_warnings.rst should be ignored (via lang-linkcheck-warnings.txt)
# - page_no_translation.rst should pass (translation doesn't exist)
# - page_placeholder_translation.rst should pass (translation is a placeholder with .. include::)

build-docs --source-dir . lang-linkcheck

output=$(build-docs --source-dir . lang-linkcheck 2>&1)
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "ERROR: lang-linkcheck should have failed with incorrect and multiple links"
    exit 1
fi

echo "SUCCESS: lang-linkcheck correctly failed with incorrect and multiple links"

# Extract only the error lines (files with ✗)
error_lines=$(echo "$output" | grep "✗")

# Verify that ignored files are not reported in errors
if echo "$error_lines" | grep -q "page_ignored_by_warnings"; then
    echo "ERROR: page_ignored_by_warnings.rst should be ignored but was reported"
    exit 1
fi

# Verify that page_no_translation is not reported in errors (translation doesn't exist)
if echo "$error_lines" | grep -q "page_no_translation"; then
    echo "ERROR: page_no_translation.rst should not be reported (translation doesn't exist)"
    exit 1
fi

# Verify that page_placeholder_translation is not reported in errors (translation is placeholder)
if echo "$error_lines" | grep -q "page_placeholder_translation"; then
    echo "ERROR: page_placeholder_translation.rst should not be reported (translation is placeholder)"
    exit 1
fi

    echo "SUCCESS: All new features (config exclude, missing translation, placeholder) work correctly"
exit 0
