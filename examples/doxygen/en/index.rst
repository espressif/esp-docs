ESP-Docs Simple Example
=========================
:link_to_translation:`zh_CN:[中文]`

This is a simple example for the esp-docs building system.

Usage Overview
--------------

Before generating random numbers, initialize the generator by calling :cpp:func:`random_number_init`
with a :cpp:type:`my_rng_config_t` configuration struct. Set the :cpp:member:`my_rng_config_t::seed`
field to :c:macro:`DEFAULT_SEED` for reproducible results, or provide a custom seed value.

Once initialized, use :cpp:func:`random_number` for non-deterministic output, or
:cpp:func:`random_number_seeded` for a deterministic sequence based on the configured seed.
Both functions accept a ``min`` and ``max`` argument; the valid range is ``[0, BIG_NUMBER]``
where :c:macro:`BIG_NUMBER` is ``124356``.

All functions that can fail return a :cpp:type:`my_api_err_t` code. Check for
:cpp:enumerator:`MY_API_OK` to confirm success.

For object-oriented usage, see :cpp:class:`ForExample` and its
:cpp:func:`ForExample::set_example_factor` method.

Error Handling
--------------

Every API function returns a :cpp:type:`my_api_err_t` status code. The three possible
values are :cpp:enumerator:`MY_API_OK`, :cpp:enumerator:`MY_API_ERR_ARG`, and
:cpp:enumerator:`MY_API_ERR_FAIL`. Always check the return value before proceeding —
passing a NULL pointer typically yields :cpp:enumerator:`MY_API_ERR_ARG`, while a resource
exhaustion or internal failure returns :cpp:enumerator:`MY_API_ERR_FAIL`.

A typical error-checking pattern::

    my_api_err_t err = random_number_init(&cfg);
    if (err != MY_API_OK) {
        // handle error
    }

Ring Buffer
-----------

The ring buffer API provides a fixed-capacity byte queue suitable for producer/consumer
patterns. Create a buffer with :cpp:func:`my_buffer_create`, specifying capacity and flags
via :cpp:type:`my_buffer_config_t`. The :cpp:member:`my_buffer_config_t::capacity` field
must not exceed :c:macro:`BUFFER_MAX_SIZE`.

Writing and Reading
^^^^^^^^^^^^^^^^^^^

Use :cpp:func:`my_buffer_write` to enqueue bytes and :cpp:func:`my_buffer_read` to consume
them. If you want to inspect data without consuming it, use :cpp:func:`my_buffer_peek` instead.

When the buffer is full and :cpp:enumerator:`BUFFER_FLAG_OVERWRITE` is set in
:cpp:member:`my_buffer_config_t::flags`, the oldest bytes are silently discarded on each
write. Without that flag, :cpp:func:`my_buffer_write` returns :cpp:enumerator:`MY_API_ERR_FAIL`.

To discard all buffered data without destroying the instance, call :cpp:func:`my_buffer_flush`.
This preserves the counters inside :cpp:type:`my_buffer_stats_t`.

Monitoring
~~~~~~~~~~

Call :cpp:func:`my_buffer_get_stats` at any time to obtain a :cpp:type:`my_buffer_stats_t`
snapshot. The :cpp:member:`my_buffer_stats_t::overflow_count` field increments every time
a write had to discard data due to a full buffer.

For event-driven monitoring, register a high-water-mark callback with
:cpp:func:`my_buffer_register_callback`. The :cpp:type:`my_buffer_watermark_cb_t` callback
receives the :cpp:type:`my_buffer_handle_t` and current fill level each time the threshold
is crossed. Pass ``NULL`` as the callback to deregister.

Lifecycle
~~~~~~~~~

Always pair :cpp:func:`my_buffer_create` with :cpp:func:`my_buffer_destroy` to avoid memory
leaks. After :cpp:func:`my_buffer_destroy` the :cpp:type:`my_buffer_handle_t` is invalid.

Configuration Reference
-----------------------

The :cpp:type:`my_buffer_config_t` struct controls buffer behaviour:

- :cpp:member:`my_buffer_config_t::capacity` — number of bytes to allocate; must be > 0
  and <= :c:macro:`BUFFER_MAX_SIZE`.
- :cpp:member:`my_buffer_config_t::flags` — bitwise OR of :cpp:type:`buffer_flag_t` values.
  Use :cpp:enumerator:`BUFFER_FLAG_NONE` for default behaviour,
  :cpp:enumerator:`BUFFER_FLAG_OVERWRITE` to allow silent overwrites, or
  :cpp:enumerator:`BUFFER_FLAG_BLOCKING` for blocking writes.

The :cpp:type:`my_rng_config_t` struct controls the random number generator:

- :cpp:member:`my_rng_config_t::seed` — initial seed; use :c:macro:`DEFAULT_SEED` for
  reproducible results.

.. ---------------------------- API Reference ----------------------------------

API Reference
-------------

.. include-build-file:: inc/my_api.inc

.. include-build-file:: inc/my_cxx_api.inc

.. include-build-file:: inc/my_buffer_api.inc
