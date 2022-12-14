ESP-Docs & Espressif Server v.s. Sphinx & Read the Docs
=======================================================

Among all Espressif software documentation, some are built with :doc:`ESP-Docs </introduction/what-is-esp-docs>` and deployed to Espressif server (recommended), such as `ESP-IDF Programming Guide <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/index.html>`__, and some are built with `Sphinx <http://www.sphinx-doc.org/>`__ and deployed to `Read the Docs <https://readthedocs.org>`__ (RTD), such as `ESP-ADF Guide <https://docs.espressif.com/projects/esp-adf/en/latest/index.html>`__.

This document compares the above two ways of building and deploying Espressif documentation and explains why the former is recommended for new Espressif software documentation. If your documentation has already adopted the latter, you can choose whether to switch to ESP-Docs for building and Espressif server for hosting based on your needs.


.. list-table::
  :header-rows: 1
  :widths: 10 20 20

  * - Dimension
    - ESP-Docs & Espressif Server
    - Sphinx & Read the Docs
  * - Feature
    - ✅ More :ref:`features <esp-docs-features>`, including 1) those provided by Sphinx 2) those provided by Sphinx third-party extensions, which are standardized to fixed versions to reduce build or deploy issues 3) those developed only for Espressif documentation, such as support for multiple targets. They are actively maintained and contribution to new or existing extensions is very welcome.
    - ❌ Fewer features, including 1) those provided by Sphinx 2) those provided by Sphinx third-party extensions, some of which are not set to fixed versions, thus causing build or deploy issues from time to time.
  * - Configuring deployment
    - ❌ More workload. For deployment information, see :ref:`update-ci-conf-file`.
    - ✅ Easier. For deployment information, see Documentation Team Site > Section ESP-Docs User Guide > Read the Docs Configuration Notes for Espressif doc.
  * - Debugging deployment issues
    - ✅ Independent debugging without engaging third parties, thus quicker.
    - ❌ Needing support from RTD team, because RTD often breaks in ways we can not debug ourselves.
  * - Debugging build issues caused by dependent packages
    - ✅ The project or documentation owner can get help and support internally from Documentation Team and ESP-Docs developers.
    - ❌ The project or documentation owner should fix them.
  * - Access to documentation
    - ✅ Quicker access
    - ❌ Slow access to RTD servers from China. A caching reverse proxy at ``docs.espressif.com`` is provided to speed up the access, but if the cache is cold, the page load time can be high (>= 0.5 s).