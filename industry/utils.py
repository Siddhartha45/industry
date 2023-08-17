def get_choice_display_value(value, choices):
    """returns the display name of choices ex: for MALE returns its display value which is पुरुष (Male)"""
    choice_dict = dict(choices)
    display_value = choice_dict.get(value, value)
    return display_value