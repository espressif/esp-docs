if build-docs --project-path api_warning -l en; then
    echo "build-docs should have failed with doxygen warning"
    exit 1
else
    echo "build-docs failed with warning (expected result)"
fi

build-docs --project-path api_no_warning -l en
