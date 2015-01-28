def is_valid_date(str):
    try:
        datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
        return True
    except Exception, e:
        return False
