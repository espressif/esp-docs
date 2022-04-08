#pragma once

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief   Purpose of this class is to give an example
 * how we document the code
 */
class ForExample {
public:
    /**
     * @brief   Creates the ForExample class instance with the given example factor
     *
     * @param[in]   example_factor_arg   Incoming example factor argument
     */
    ForExample(double example_factor_arg);

    /**
     * @brief   Set example factor
     *
     *
     * @param[in]   example_factor_arg   Incoming example factor argument
     *
     * @return      true if the example factor updated successfully, false otherwise
     */
    bool set_example_factor(double example_factor_arg);

private:
    /**
     * @brief   Get example factor
     *
     * @return      Internally set example factor
     */
    double get_example_factor();

    /**
     * @brief Example factor value
     */
    double example_factor;
};

#ifdef __cplusplus
}
#endif
