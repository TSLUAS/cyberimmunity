import numpy as np

def find_outliers(data) -> list:
    # Расчет квартилей
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    # Адаптация коэффициента k в зависимости от размера выборки
    if len(data) < 20:
        k = 2.0  # Более мягкие границы при малой выборке
    elif len(data) > 100:
        k = 1.3  # Жёстче при большой выборке

    # Расчет границ
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return [x for x in data if x < lower or x > upper]

if __name__ == '__main__':
    # Пример использования
    example = [1, 1.2, 1.3, 5, 0.9, 3, 1.1, 1, 1.4]
    outliers = find_outliers(data=example)
    print(outliers)