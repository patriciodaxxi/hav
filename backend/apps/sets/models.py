from django.db import models
from treebeard.mp_tree import MP_Node


class Node(MP_Node):

    name = models.CharField(max_length=200)

    @staticmethod
    def get_collection_roots():
        return Node._default_manager.filter(collection__isnull=False)

    def __str__(self):
        return self.name

#
