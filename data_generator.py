def generar_ips(count, expected_unique_values):
    total = 0
    while True:
        for ip in range(0, expected_unique_values):
            yield ip
            total += 1
            if total >= count:
                return