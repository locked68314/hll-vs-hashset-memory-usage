from typing import TypedDict

from pympler import asizeof
from datasketch import HyperLogLog

from data_generator import generar_ips
from utills import format_bytes_size, transpose_data, tabla_comparativa


class MemoryTestResults(TypedDict):
    memory_usage: int
    count: float

def test_memory_usage_hll(values, p=12):
    hll = HyperLogLog(p=p)
    for i in values:
        hll.update(str(i).encode())
    return MemoryTestResults(memory_usage=asizeof.asizeof(hll), count=hll.count())

def test_memory_usage_hset(values):
    hset = set()
    for i in values:
        hset.add(i)
    return MemoryTestResults(memory_usage=asizeof.asizeof(hset), count=len(hset))

class ProfileData(TypedDict):
    values_count: list[int]
    unique_values: list[int]
    performance: list[int]
    estimated_count: list[float]

def profile_memory_usage(
        test_memory_function,
        initial_values_count,
        end_values_count,
        step,
        unique_values_percentage,
        **test_memory_function_kwargs
    ):
    profiling_data = ProfileData(values_count=[], unique_values=[], performance=[], estimated_count=[])
    loop_controller = initial_values_count
    while loop_controller <= end_values_count:
        unique_values_count = int(loop_controller*unique_values_percentage)
        memory_test_result = test_memory_function(
            (generar_ips(loop_controller, unique_values_count)),
            **test_memory_function_kwargs
        )
        profiling_data["values_count"].append(loop_controller)
        profiling_data["unique_values"].append(unique_values_count)
        profiling_data["performance"].append(memory_test_result["memory_usage"])
        profiling_data["estimated_count"].append(memory_test_result["count"])
        loop_controller += step
    return profiling_data

def profile_memory_usage_comparer(
        hll_test,
        hset_test,
        initial_values_count,
        end_values_count,
        step,
        unique_values_percentage,
        **hll_test_kwargs
    ):
    loop_controller = initial_values_count
    count_loop = 1
    while loop_controller <= end_values_count:
        print(f"=== LOOP {count_loop} ===")
        unique_values_count = int(loop_controller*unique_values_percentage)
        print(f"Datos totales: {loop_controller} | Unicos: {unique_values_count}")
        hll_test_results = hll_test(
            (generar_ips(loop_controller, unique_values_count)),
            **hll_test_kwargs
        )
        print(f"HyperLogLog:\n\t"
              f"- Elementos estimados: {hll_test_results['count']}\n\t"
              f"- Memoria utilizada: {format_bytes_size(hll_test_results["memory_usage"])}")
        hset_test_results = hset_test(
            (generar_ips(loop_controller, unique_values_count)),
        )
        print(f"HashSet:\n\t"
              f"- Elementos estimados: {hset_test_results['count']}\n\t"
              f"- Memoria utilizada: {format_bytes_size(hset_test_results["memory_usage"])}")
        print(f"Ratio de memoria: {hset_test_results["memory_usage"]/hll_test_results["memory_usage"]}x (HashSet/HyperLogLog)")
        loop_controller += step
        count_loop += 1

def generate_compare_table_image(
    INITIAL_MAX_REGISTER_COUNT,
    END_MAX_REGISTER_COUNT,
    UNIQUE_VALUES_PERCENT,
    LOOP_STEP,
    HYPERLOGLOG_p):
    hll_profile_data = profile_memory_usage(
        test_memory_usage_hll,
        INITIAL_MAX_REGISTER_COUNT,
        END_MAX_REGISTER_COUNT,
        LOOP_STEP,
        UNIQUE_VALUES_PERCENT,
        p=HYPERLOGLOG_p
    )

    hset_profile_data = profile_memory_usage(
        test_memory_usage_hset,
        INITIAL_MAX_REGISTER_COUNT,
        END_MAX_REGISTER_COUNT,
        LOOP_STEP,
        UNIQUE_VALUES_PERCENT
    )

    data = {
        "Total values": ["{:,}".format(value) for value in hll_profile_data["values_count"]],
        "Unique Total Values": ["{:,}".format(value) for value in hll_profile_data["unique_values"]],
        "HashSet Memory Usage": [format_bytes_size(value) for value in hset_profile_data["performance"]],
        f'HLL Memory Usage (p={HYPERLOGLOG_p})': [format_bytes_size(value) for value in hll_profile_data["performance"]],
        "HLL Estimated Count": ["{:,.2f}".format(value) for value in hll_profile_data["estimated_count"]],
    }
    transposed_data = transpose_data(data)
    tabla_comparativa(
        columns=transposed_data['columns'],
        data=transposed_data['values'],
        image_name="tabla_comparativa_hset_hll.png"
    )

def test_relation_memory_error_with_p(
    p_values,
    max_register_count = 200_000,
    unique_values_percent = 0.5,
):
    data = {
        "REGISTER_COUNT": max_register_count,
        "UNIQUE_VALUES": max_register_count*unique_values_percent,
        "test_data": {
            "p_value": [],
            "count": [],
            "memory_usage": []
        }
    }
    for p_value in p_values:
        hll_test_results = test_memory_usage_hll(
            generar_ips(max_register_count, int(max_register_count * unique_values_percent)),
            p_value
        )
        data["test_data"]["p_value"].append(p_value)
        data["test_data"]["count"].append(hll_test_results["count"])
        data["test_data"]["memory_usage"].append(hll_test_results["memory_usage"])
    return data

def save_table_trmewp(
    p_values,
    max_register_count = 200_000,
    unique_values_percent = 0.5,
):
    data = test_relation_memory_error_with_p(
        p_values, max_register_count, unique_values_percent )
    data = {
        "P Values": data["test_data"]["p_value"],
        "Estimated Count": ["{:,.2f}".format(value) for value in data["test_data"]["count"]],
        "Real Count": ["{:,.2f}".format(data["UNIQUE_VALUES"]) for _ in p_values],
        f'HLL Memory Usage': [format_bytes_size(value) for value in data["test_data"]["memory_usage"]],
    }
    transposed_data = transpose_data(data)
    tabla_comparativa(
        columns=transposed_data['columns'],
        data=transposed_data['values'],
        image_name="tabla_comparativa_hll_with_p_values.png"
    )