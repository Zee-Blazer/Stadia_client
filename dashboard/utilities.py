def day_prefix_setter(day):
    if str(day).endswith('1'):
        return 'st'
    elif str(day).endswith('2'):
        return 'nd'
    elif str(day).endswith('3'):
        return 'rd'
    else:
        return 'th'


def month_setter(month):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November',
              'December']

    setter = {num: name for num, name in zip(range(1, 13), months)}

    return setter[month]
