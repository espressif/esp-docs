#pragma once

#include <stdint.h>
#include <stddef.h>
#include "my_api.h"

/**
 * @brief   Maximum capacity of a ring buffer instance
 */
#define BUFFER_MAX_SIZE 4096

/**
 * @brief   Sentinel value returned when the buffer is empty
 */
#define BUFFER_EMPTY_VAL -1

/**
 * @brief   Buffer operation flags
 */
typedef enum {
    BUFFER_FLAG_NONE      = 0x00,  /**< No flags set */
    BUFFER_FLAG_OVERWRITE = 0x01,  /**< Overwrite oldest data when full */
    BUFFER_FLAG_BLOCKING  = 0x02,  /**< Block caller until space is available */
} buffer_flag_t;

/**
 * @brief   Opaque handle to a ring buffer instance
 */
typedef struct my_buffer_t *my_buffer_handle_t;

/**
 * @brief   Configuration for a ring buffer
 */
typedef struct {
    size_t        capacity;  /**< Maximum number of bytes the buffer can hold */
    buffer_flag_t flags;     /**< Combination of :c:type:`buffer_flag_t` flags */
} my_buffer_config_t;

/**
 * @brief   Statistics snapshot for a buffer instance
 */
typedef struct {
    size_t   bytes_written;  /**< Total bytes written since creation */
    size_t   bytes_read;     /**< Total bytes read since creation */
    size_t   current_fill;   /**< Current number of bytes waiting to be read */
    uint32_t overflow_count; /**< Number of times the buffer overflowed */
} my_buffer_stats_t;

/**
 * @brief   Callback invoked when the buffer crosses the high-water mark
 *
 * @param[in]   handle   Buffer that triggered the callback
 * @param[in]   fill     Current fill level in bytes
 * @param[in]   user_ctx Pointer passed in :cpp:func:`my_buffer_register_callback`
 */
typedef void (*my_buffer_watermark_cb_t)(my_buffer_handle_t handle, size_t fill, void *user_ctx);

/**
 * @brief   Create a new ring buffer
 *
 * Allocates internal storage according to :cpp:member:`my_buffer_config_t::capacity`.
 * The caller must eventually call :cpp:func:`my_buffer_destroy` to release resources.
 *
 * @param[in]   config  Pointer to a filled :cpp:type:`my_buffer_config_t`
 * @param[out]  out     Receives the new :cpp:type:`my_buffer_handle_t` on success
 *
 * @return
 *  - :c:enumerator:`MY_API_OK` on success
 *  - :c:enumerator:`MY_API_ERR_ARG` if config or out is NULL, or capacity is 0
 *  - :c:enumerator:`MY_API_ERR_FAIL` if memory allocation failed
 */
my_api_err_t my_buffer_create(const my_buffer_config_t *config, my_buffer_handle_t *out);

/**
 * @brief   Destroy a ring buffer and free all resources
 *
 * After this call the handle is invalid and must not be used.
 *
 * @param[in]   handle  Buffer to destroy
 *
 * @return
 *  - :c:enumerator:`MY_API_OK` on success
 *  - :c:enumerator:`MY_API_ERR_ARG` if handle is NULL
 */
my_api_err_t my_buffer_destroy(my_buffer_handle_t handle);

/**
 * @brief   Write bytes into the buffer
 *
 * If :c:enumerator:`BUFFER_FLAG_OVERWRITE` is set and the buffer is full, the oldest
 * bytes are silently discarded to make room.
 *
 * @param[in]   handle  Target buffer
 * @param[in]   data    Pointer to the bytes to write
 * @param[in]   len     Number of bytes to write; must be <= :c:macro:`BUFFER_MAX_SIZE`
 *
 * @return
 *  - :c:enumerator:`MY_API_OK` on success
 *  - :c:enumerator:`MY_API_ERR_ARG` if handle or data is NULL, or len is zero
 *  - :c:enumerator:`MY_API_ERR_FAIL` if the buffer is full and overwrite is disabled
 */
my_api_err_t my_buffer_write(my_buffer_handle_t handle, const uint8_t *data, size_t len);

/**
 * @brief   Read bytes from the buffer
 *
 * Bytes are consumed; a subsequent read will not return the same data.
 *
 * @param[in]   handle  Source buffer
 * @param[out]  data    Destination for the bytes read
 * @param[in]   len     Maximum number of bytes to read
 * @param[out]  read    Actual number of bytes placed in data
 *
 * @return
 *  - :c:enumerator:`MY_API_OK` on success (check *read for actual count)
 *  - :c:enumerator:`MY_API_ERR_ARG` if any pointer is NULL
 */
my_api_err_t my_buffer_read(my_buffer_handle_t handle, uint8_t *data, size_t len, size_t *read);

/**
 * @brief   Peek at bytes without consuming them
 *
 * Identical to :cpp:func:`my_buffer_read` but the data remains in the buffer.
 *
 * @param[in]   handle  Source buffer
 * @param[out]  data    Destination for the bytes peeked
 * @param[in]   len     Maximum number of bytes to peek
 * @param[out]  peeked  Actual number of bytes placed in data
 *
 * @return
 *  - :c:enumerator:`MY_API_OK` on success
 *  - :c:enumerator:`MY_API_ERR_ARG` if any pointer is NULL
 */
my_api_err_t my_buffer_peek(my_buffer_handle_t handle, uint8_t *data, size_t len, size_t *peeked);

/**
 * @brief   Reset the buffer to empty, discarding all contents
 *
 * Statistics counters are preserved; only the read/write positions are reset.
 *
 * @param[in]   handle  Buffer to flush
 *
 * @return
 *  - :c:enumerator:`MY_API_OK` on success
 *  - :c:enumerator:`MY_API_ERR_ARG` if handle is NULL
 */
my_api_err_t my_buffer_flush(my_buffer_handle_t handle);

/**
 * @brief   Query current statistics for a buffer
 *
 * @param[in]   handle  Buffer to query
 * @param[out]  stats   Receives a snapshot of :cpp:type:`my_buffer_stats_t`
 *
 * @return
 *  - :c:enumerator:`MY_API_OK` on success
 *  - :c:enumerator:`MY_API_ERR_ARG` if handle or stats is NULL
 */
my_api_err_t my_buffer_get_stats(my_buffer_handle_t handle, my_buffer_stats_t *stats);

/**
 * @brief   Register a callback fired when fill level crosses a threshold
 *
 * Only one callback can be registered per buffer; calling this again replaces
 * the previous registration.
 *
 * @param[in]   handle      Buffer to monitor
 * @param[in]   cb          Callback function, or NULL to deregister
 * @param[in]   watermark   Fill level in bytes that triggers the callback
 * @param[in]   user_ctx    Opaque pointer forwarded to the callback
 *
 * @return
 *  - :c:enumerator:`MY_API_OK` on success
 *  - :c:enumerator:`MY_API_ERR_ARG` if handle is NULL or watermark exceeds capacity
 */
my_api_err_t my_buffer_register_callback(my_buffer_handle_t handle,
                                          my_buffer_watermark_cb_t cb,
                                          size_t watermark,
                                          void *user_ctx);
