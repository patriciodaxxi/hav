import os
from pathlib import Path
from collections import namedtuple
from itertools import chain

from apps.whav.models import MediaOrdering, ImageCollection

AbstractPath = namedtuple('AbstractPath', ['id', 'name'])

ResolvedIngestionItems = namedtuple('IngestionItemsByPath', ['path', 'items'])


def recurse_folder(root_folder):
    root_path = Path(root_folder).parent
    found = []
    for root, dirs, files in os.walk(root_folder):
        rel_path = Path(root).relative_to(root_path)
        paths = [AbstractPath(id=root, name=p) for p in rel_path.parts]
        items = ResolvedIngestionItems(path=paths, items=[Path(os.path.join(root, f)) for f in files])
        found.append(items)

    return found


def recurse_whav(collection):
    descendants = chain(
        collection.get_descendants()
    )

    # build a root path
    root_path = [AbstractPath(id=ic.pk, name=ic.name) for ic in collection.get_ancestors()]

    mediaordering_items = []

    for imagecollection in descendants:
        parents = [AbstractPath(id=ic.pk, name=ic.name) for ic in imagecollection.get_ancestors()]
        relative_parents = parents[:len(root_path)]
        items = ResolvedIngestionItems(path=relative_parents, items=MediaOrdering.objects.filter(collection=imagecollection))


    return mediaordering_items




def resolveIngestionItems(unresolved_items):

    items = []

    for item in unresolved_items:
        if isinstance(item, MediaOrdering):
            items.append(ResolvedIngestionItems(path=[], items=[item]))
        elif isinstance(item, ImageCollection):
            items.expand(recurse_whav(item))
        elif isinstance(item, Path):
            if item.is_dir():
                items.extend(recurse_folder(item))
            else:
                items.append(ResolvedIngestionItems(path=[], items=[item]))
        else:
            raise NotImplementedError('Unknown object: %s' % item)

    return items
