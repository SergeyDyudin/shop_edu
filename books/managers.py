from django.db import models


class AdultFiltered(models.Manager):

    def adult_control(self, user):
        if hasattr(user, 'profile') and user.profile.age >= 18:
            return super(AdultFiltered, self).get_queryset()
        return super(AdultFiltered, self).get_queryset().exclude(category__name='18+')
