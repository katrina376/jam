from django.core.exceptions import ValidationError
from django.db import models

from .. import settings


class CommentManager(models.Manager):
    """Manager of Comment model."""

    def create(self, *args, **kwargs):
        """Overrided create method with validations.

        Check if either `talk` or `comment` is null. Only one of them can be
        null. If `talk` is not null, which means the comment is directly to a
        talk, it makes the created instance a root comment. On the other hand,
        if `comment` is not null, which means it is a reply to another comment,
        it makes the created instance a leaf comment.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Instance of the created vote.

        Raises:
            ValidationError: If `user` has already voted on `comment`.
        """

        talk = kwargs.get('talk', None)
        comment = kwargs.get('comment', None)

        if talk is None and comment is None:
            raise ValidationError('Either talk or comment should not be null.')
        elif talk is not None and comment is not None:
            raise ValidationError('Either talk or comment should be null.')

        return super().create(*args, **kwargs)


class Comment(models.Model):
    """Comment to a talk or another comment.

    Use `Comment.object.create(*args, **kwargs)` to create an instance.
    Arguments are listed below.

    Args:
        content (str):
        user (:obj:`User`):
        talk (:obj:`User`, optional): Talk of the comment. Should be null if
            `comment` is not null.
        comment (:obj:`Comment`, optional): Target comment of the comment.
            Should be null if `talk` is not null.

    Attributes:
        content (str):
        create_time (datetime): Create time of the comment.
        last_update (datetime): Last update time of the comment.
        user (:obj:`User`):
        talk (:obj:`User`): Talk of the comment. Should be null if `comment` is
            not null.
        comment (:obj:`Comment`): Target comment of the comment. Should be null
            if `talk` is not null.
        objects (:obj:`CommentManager`): Manager of Comment model.
    """

    content = models.TextField()
    create_time = models.DateTimeField(auto_now=True)
    last_update = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    talk = models.ForeignKey(
        'Talk', on_delete=models.CASCADE, related_name='comments', null=True)
    comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='replies', null=True)

    objects = CommentManager()

    @property
    def is_root(self):
        """Whether the comment is a root comment or leaf comment.

        If the comment is directly to a talk, it is a root comment. If the
        comment is to another comment instead, it is a leaf comment.

        Returns:
            True if the comment is root. False if not.
        """
        return self.comment is None
