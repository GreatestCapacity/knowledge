def filter_by_name(param, source):
    return list(
        map(lambda x: x.name,
            filter(lambda x: x.name.startswith(param), source))
    )


def filter_by_title(param, source):
    return list(
        map(lambda x: x.title,
            filter(lambda x: x.title.startswith(param), source))
    )
