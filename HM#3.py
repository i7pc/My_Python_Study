from datetime import datetime, timedelta

# cловник для налагодження
users = [
    {"name": "Monday_emp.", "birthday": datetime(year=1986, month=11, day=6)},
    {"name": "Thusday_emp.", "birthday": datetime(year=1986, month=11, day=5)},
    {"name": "Wednesday_emp.", "birthday": datetime(
        year=1986, month=11, day=5)},
    {"name": "Thersday_emp.", "birthday": datetime(
        year=1986, month=11, day=6)},
    {"name": "Friday_emp.", "birthday": datetime(year=1986, month=11, day=4)}
]


def _dict_dates(date_: datetime):
    """ф-ція перевірки дня тижня і умови дії
    вхідні дані день(datetime) та перелік дат іменинників
    """
    weekday = date_.strftime("%A")  # передаємо назву дня

    if weekday == 'Monday':  # якщо понеділок, маємо захопити last weekend
        return (weekday, [
            date_,
            date_ + timedelta(days=-1),
            date_ + timedelta(days=-2),
        ])
    elif weekday in ('Saturday', 'Sunday'):  # якшо вихідні, то привітати в понеділок
        return (None, [])
    else:
        return (weekday, [date_])  # якшо інші дні, то будуємо тиждень вперед


def _print_results(results):
    """ф-ція виводу інформації
    ввідн дані - словник. ключ - день, значення - ім"я 
    """
    for day, names in results.items():
        if names:
            print(f"{day}: {', '.join(names)}")


def get_birthdays_per_week(users):
    """ ф-ція отримання тижня іменинників від початкової дати 
    """
    dates = [
        # cтворюємо перелік дат від сьогоднішньої дати
        _dict_dates(datetime.now().date() + timedelta(days=x))
        for x in range(7)
    ]

    dates_dict = {
        # створюємо словник з ключами - по дням і пустими значеннями.
        x: y
        for x, y in dates
        # умова виключення дня якщо нема іменинників
        if x is not None
    }
    # створюємо словник із ключами по дням, перебираючи
    result_dict = {x: [] for x in dates_dict.keys()}

    # перебираємо перелік іменинників.
    for user in users:
        for weekday, birthdays_dates in dates_dict.items():
            if any([
                user["birthday"].day == x.day and user["birthday"].month == x.month
                for x in birthdays_dates
            ]):
                result_dict[weekday].append(user["name"])
    _print_results(result_dict)


if __name__ == "__main__":
    get_birthdays_per_week(users)
