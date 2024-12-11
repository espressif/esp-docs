build-docs -t esp32 -l en
# Check for the existence of a zip file
if ls _build/**/**/html/*.zip 1> /dev/null 2>&1; then
    echo "Zip file exists."
else
    echo "No zip file found." >&2
    exit 1 # Exit with a non-zero status to indicate failure
fi
