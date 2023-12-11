from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    # types of content that users are liked
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE )
    # id of content that liked
    object_id = models.PositiveIntegerField()
    #connection between items. ID and type of contents
    content_object = GenericForeignKey()
