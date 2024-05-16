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

Blockdiag Example
-----------------

.. blockdiag::
    :scale: 100%
    :caption: Blockdiagram
    :align: center

    blockdiag esp-docs-block-diag {
        Start -> Middle
        Middle -> End
    }

For documentation about esp-docs please see https://github.com/espressif/esp-docs/tree/master/docs

.. toctree::
    :maxdepth: 1

    Subpage <subpage>
