from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    label = models.CharField(max_length = 255)
    
    def __str__(self) -> str:
        return self.label

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):    
        # get id of product from db and store it in this variable
        content_type = ContentType.objects.get_for_model(obj_type)
        # to reduce proceccess preload "tag"(because tag in TaggedItem is foreign key to Tag) 
        # and then filter products with id 1.
        return TaggedItem.objects. \
            select_related('tag'). \
                filter(
                    content_type = content_type,
                    object_id = obj_id
                    )
                
class TaggedItem(models.Model):
    # override new 'objects' with our custom behaviour 
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete = models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()