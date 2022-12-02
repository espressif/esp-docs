ESP-Docs Simple Example
=========================
:link_to_translation:`zh_CN:[中文]`

This is a simple example for the esp-docs building system.

Wavedrom Example
----------------

.. wavedrom::

        { "signal": [
                { "name": "clk",  "wave": "P......" },
                { "name": "bus",  "wave": "x.==.=x", "data": ["head", "body", "tail", "data"] },
                { "name": "wire", "wave": "0.1..0." }
        ]}


.. wavedrom:: /../_static/periph_timing.json


For documentation about esp-docs please see https://github.com/espressif/esp-docs/tree/master/docs

.. toctree::
    :maxdepth: 1

    Subpage <subpage>