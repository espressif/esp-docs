###############################
 Deploying Documentation to S3
###############################

ESP-Docs provides CI helper scripts to upload built documentation artifacts to an S3-compatible storage backend.

This deployment flow is split into two steps:

- Upload build outputs to a commit-scoped prefix in a *staging* location.
- Promote the uploaded objects to the final *production* location.

The scripts live in:

- :project_file:`upload_docs_s3.py <src/esp_docs/upload_docs_s3.py>`
- :project_file:`deploy_docs_s3.py <src/esp_docs/deploy_docs_s3.py>`

**************
 How it works
**************

1. Build the documentation (HTML and optionally PDF) in your CI job, producing a directory pointed to by ``DOCS_BUILD_DIR``.
2. Run ``upload_docs_s3.py``.

   - It derives a deploy ``version`` from ``GIT_VER`` using ``sanitize_version``.
   - It collects artifacts under ``DOCS_BUILD_DIR``:

     - HTML directories matching ``**/html/``
     - PDF files matching ``**/latex/build/*.pdf``

   - It copies these artifacts into a temporary directory ``DOCS_BUILD_DIR/tmp_deploy`` using the deployed layout:

     - ``language/<version>/<target>/...`` (the ``<target>`` component is omitted when the target name is ``generic``)

   - It uploads the staged directory to S3 using a *commit-scoped* prefix:

     - ``<CI_COMMIT_SHA>/<DOCS_S3_DEPLOY_PATH>/...``

3. Run ``deploy_docs_s3.py``.

   - It lists objects under ``<CI_COMMIT_SHA>/<DOCS_S3_DEPLOY_PATH>/...`` in the staging bucket.
   - It copies them into the production bucket under the final prefix:

     - ``<DOCS_S3_DEPLOY_PATH>/...``

Stable version
==============

If ``DEPLOY_STABLE`` is set (to a truthy value) and the derived version is considered stable (see ``is_stable_version``), ``upload_docs_s3.py`` repeats the upload using ``stable`` as the version.

********************************
 Required environment variables
********************************

The scripts read configuration from environment variables (for example, GitLab CI/CD variables).

Common
======

- ``DOCS_S3_ACCESS_KEY_ID``: S3 access key.
- ``DOCS_S3_SECRET_ACCESS_KEY``: S3 secret key.
- ``DOCS_S3_ENDPOINT``: S3 endpoint URL.
- ``DOCS_S3_DEPLOY_PATH``: Remote base path, for example:

  .. code-block:: text

      /project/<project-name>

Upload step (``upload_docs_s3.py``)
===================================

- ``DOCS_S3_BUCKET_NAME``: Destination bucket (typically the staging bucket in CI).
- ``GIT_VER``: Git version string to derive the deploy version from.
- ``DOCS_BUILD_DIR``: Local directory where docs have already been built.
- ``CI_COMMIT_SHA``: Commit SHA used to namespace uploads in the staging prefix.

Promotion step (``deploy_docs_s3.py``)
======================================

- ``DOCS_S3_STAGING_BUCKET_NAME``: Bucket holding commit-scoped uploads.
- ``DOCS_S3_PRODUCTION_BUCKET_NAME``: Bucket used to serve docs.
- ``CI_COMMIT_SHA``: Commit SHA used to locate the staged objects.

********************************
 Optional environment variables
********************************

- ``DEPLOY_STABLE``: If set and the derived version is stable, also deploy under ``language/stable/...``.
