can_create_guild = 0b1000
can_review_guild = 0b0100
can_delete_guild = 0b0010
can_edit_guild = 0b0001


def get_create_bits(user_permissions):
    if can_create_guild & user_permissions == can_create_guild:
        return True
    return False


def get_review_bits(user_permissions):
    if can_review_guild & user_permissions == can_review_guild:
        return True
    return False


def get_delete_bits(user_permissions):
    if can_delete_guild & user_permissions == can_delete_guild:
        return True
    return False


def get_edit_bits(user_permissions):
    if can_edit_guild & user_permissions == can_edit_guild:
        return True
    return False


print(can_create_guild & 0b0110 == can_create_guild)
