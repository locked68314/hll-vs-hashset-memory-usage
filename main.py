from memory_tests import test_memory_usage_hll, test_memory_usage_hset, \
    profile_memory_usage_comparer

if __name__ == "__main__":

    INITIAL_MAX_REGISTER_COUNT = 200_000
    END_MAX_REGISTER_COUNT = 2_000_000
    UNIQUE_VALUES_PERCENT = 0.5
    LOOP_STEP = 200_000
    HYPERLOGLOG_p = 15

    profile_memory_usage_comparer(
        test_memory_usage_hll,
        test_memory_usage_hset,
        INITIAL_MAX_REGISTER_COUNT,
        END_MAX_REGISTER_COUNT,
        LOOP_STEP,
        UNIQUE_VALUES_PERCENT,
        p=HYPERLOGLOG_p
    )



