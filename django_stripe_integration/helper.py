service_fee_percentage = 2.9 / 100
service_fee_fixed = 30


def add_service_fee(price):
    return (price + service_fee_fixed) / (1 - service_fee_percentage)
