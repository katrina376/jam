from django.core.exceptions import ValidationError
from django.db import models

from .. import settings


class CommentManager(models.Manager):
    """Manager of Comment model."""

    def create(self, *args, **kwargs):
        talk = kwargs.get('talk', None)
        comment = kwargs.get('comment', None)

        if talk is None and comment is None:
            raise ValidationError('Either talk or comment should not be null.')
        elif talk is not None and comment is not None:
            raise ValidationError('Either talk or comment should be null.')

        return super().create(*args, **kwargs)


class Comment(models.Model):
    """Comment to a talk or another comment."""

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
