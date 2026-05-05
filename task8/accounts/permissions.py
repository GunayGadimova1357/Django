def is_editor(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_not_banned(user):
    return user.is_authenticated and not getattr(getattr(user, "profile", None), "is_banned", False)


def can_manage_article(user, article):
    return is_editor(user) or (user.is_authenticated and article.author_id == user.id)
