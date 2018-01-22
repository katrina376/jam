from django.core.exceptions import ValidationError
from django.db import models

from .. import settings


class VoteManager(models.Manager):
    """Manager of Vote model."""

    def create(self, *args, **kwargs):
        """Overrided create method with validations.

        Check if the user has already voted on the comment.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Instance of the created vote.

        Raises:
            ValidationError: If `user` has already voted on `comment`.
        """

        validate = {
            'user': kwargs.get('user'),
            'comment': kwargs.get('comment'),
        }

        if self.get_queryset().filter(**validate).exists():
            raise ValidationError(
                """User<{user}>has already voted on \
                Comment<{comment}>""".format(**validate))

        return super().create(*args, **kwargs)

    def ups(self):
        """Method of filtering only up votes.

        Returns:
            Queryset of up votes.
        """

        return self.get_queryset().filter(kind='U')

    def downs(self):
        """Method of filtering only down votes.

        Returns:
            Queryset of down votes.
        """

        return self.get_queryset().filter(kind='D')


class Vote(models.Model):
    """Vote to a comment.

    Use `Vote.object.create(*args, **kwargs)` to create an instance.
    Arguments are listed below.

    Arguments:
        kind (str): Type of the vote. Should be a symbol of the vote types.
        user (:obj:`User`): Creator of the vote.
        comment (:obj:`Comment`): Target of the vote.

    Attributes:
        UP (str): Symbol of up vote type.
        DOWN (str): Symbol of down vote type.
        KIND_CHOICES (tuple): Tuple of choices for `kind`.
        create_time (datetime): Create time of the vote.
        kind (str): Type of the vote. Limited to up or down.
        user (:obj:`User`): Creator of the vote.
        comment (:obj:`Comment`): Target of the vote.
        objects (:obj:`VoteManager`): Manager of Vote model.
    """

    UP = 'U'
    DOWN = 'D'
    KIND_CHOICES = (
        (UP, 'up vote'),
        (DOWN, 'down vote'),
    )

    create_time = models.DateTimeField(auto_now=True)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='polls',
    )

    comment = models.ForeignKey(
        'core.Comment', on_delete=models.CASCADE, related_name='polls')

    objects = VoteManager()
