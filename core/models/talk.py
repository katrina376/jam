from django.core.exceptions import ValidationError
from django.db import models

from .. import settings


class TalkManager(models.Manager):
    """Manager of Talk model."""

    def create(self, *args, **kwargs):
        """Overrided create method with validations.

        Check if at least one speaker is assigned to the talk. Also assign the
        talk to the speaker(s) with the creation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Instance of the created talk.

        Raises:
            ValidatioError: If no `user` is assigned.
        """

        speakers = set(kwargs.pop('speakers', []))
        if len(speakers) == 0:
            raise ValidationError(
                'The talk should at least be assigned to one speaker.')

        talk = super().create(*args, *kwargs)
        talk.speakers.add(*speakers)

        return talk


class Talk(models.Model):
    """Core model of all.

    Use `Talk.object.create(*args, **kwargs)` to create a Talk instance.
    Arguments are listed below.

    Args:
        title (str): Title of the talk.
        remark (str): Remark by the staff of the conference.
        description (str): Description of the talk by speakers themselves.
        order (int): Number of the order for talks in the same section.
            Defaults to 0.
        speakers (:obj:`User`): Speaker(s) of the talk.
        section (:obj:`Section`, optional): Section of the talk belonging to.

    Attributes:
        title (str): Title of the talk.
        remark (str): Remark by the staff of the conference.
        description (str): Description of the talk by speakers themselves.
        order (int): Number of the order for talks in the same section.
            Defaults to 0.
        speakers (:obj:`User`): Speaker(s) of the talk.
        section (:obj:`Section`, optional): Section of the talk belonging to.
        objects (:obj:`TalkManager`): Manager of Talk model.
    """

    title = models.CharField(max_length=128)
    remark = models.TextField()
    description = models.TextField()

    order = models.SmallIntegerField(default=0)

    speakers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='talks',
    )

    section = models.ForeignKey(
        settings.SECTION_MODEL,
        on_delete=models.SET_NULL,
        related_name='talks',
        null=True,
        default=None,
    )

    objects = TalkManager()
