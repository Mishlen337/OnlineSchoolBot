
def get_discount(package_names):
    total_discount = 0
    based_count = grouped_count = individual_count = 0
    for pk in package_names:
        if pk == 'Based':
            based_count += 1
        if pk == 'Групповой':
            grouped_count += 1
        if pk == 'Индивидуальный':
            individual_count += 1

    if based_count >= 2:
        total_discount = max(3, total_discount)
    if based_count >= 1 and grouped_count >= 1:
        total_discount = max(4, total_discount)
    if based_count >= 3:
        total_discount = max(5, total_discount)
    if grouped_count >= 2:
        total_discount = max(6, total_discount)
    if grouped_count >= 3:
        total_discount = max(7, total_discount)
    if individual_count >= 2:
        total_discount = max(10, total_discount)
    return total_discount
