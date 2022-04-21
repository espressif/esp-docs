#pragma once

#define BIG_NUMBER 124356

/**
 * @brief   Returns a random number inside a range
 *
 *
 * @param[in]   min   Lower end of the range
 * @param[in]   max   Upper end of the range
 *
 * @note    Not cryptographically secure
 *
 * @return      random integer
 */
int random_number(int min, int max);