def if_debug(if_true, if_false = []):
    return select({
        "//ext:debug": if_true,
        "//conditions:default": if_false,
    })
