#pragma once

#include <stdbool.h>
#include <stdint.h>

/**
 * @brief   Upper bound constant for range-based operations
 */
#define BIG_NUMBER 124356

/**
 * @brief   Default seed value used when no seed is provided
 */
#define DEFAULT_SEED 42

/**
 * @brief   Return codes for API functions
 */
typedef enum {
    MY_API_OK       = 0,  /**< Operation completed successfully */
    MY_API_ERR_ARG  = 1,  /**< Invalid argument provided */
    MY_API_ERR_FAIL = 2,  /**< Operation failed */
} my_api_err_t;

/**
 * @brief   Configuration for the random number generator
 */
typedef struct {
    uint32_t seed;    /**< Initial seed value */
    bool     bounded; /**< Whether to enforce min/max bounds strictly */
} my_rng_config_t;

/**
 * @brief   Returns a random number inside a range
 *
 * @param[in]   min   Lower end of the range
 * @param[in]   max   Upper end of the range
 *
 * @note    Not cryptographically secure
 *
 * @return      random integer
 */
int random_number(int min, int max);

/**
 * @brief   Initialize the random number generator with a configuration
 *
 * Call this before using :c:func:`random_number` or :c:func:`random_number_seeded`.
 *
 * @param[in]   config  Pointer to a :c:type:`my_rng_config_t` configuration struct
 *
 * @return
 *  - :c:macro:`MY_API_OK` on success
 *  - :c:macro:`MY_API_ERR_ARG` if config is NULL
 */
my_api_err_t random_number_init(const my_rng_config_t *config);

/**
 * @brief   Returns a seeded random number inside a range
 *
 * Unlike :c:func:`random_number`, this function uses the seed configured
 * via :c:func:`random_number_init` to produce a deterministic sequence.
 *
 * @param[in]   min   Lower end of the range
 * @param[in]   max   Upper end of the range
 *
 * @return      deterministic random integer, or -1 on error
 */
int random_number_seeded(int min, int max);