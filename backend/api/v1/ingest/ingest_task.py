from channels.layers import get_channel_layer
from django_rq import get_queue, job

from apps.archive.tasks import archive
from apps.webassets.tasks import create_webassets_after_archive_task as create_webassets

channel_layer = get_channel_layer()

from asgiref.sync import async_to_sync

def send_progress(msg, media_id, channel_group):
    async_to_sync(channel_layer.group_send)(
        channel_group,
        {
            "type": "ingest.progress",
            "msg": msg,
            "media_id": media_id
        })

def archive_and_create_webassets(filename, media_id, user_id, channel_group='ingest'):

    progress_args = [media_id, channel_group]

    archive_queue = get_queue('archive')
    webasset_queue = get_queue('webassets')
    default_queue = get_queue('default')

    default_queue.enqueue(send_progress, "started", *progress_args)

    archive_job = archive_queue.enqueue(
        archive,
        filename,
        media_id,
        user_id,
        result_ttl=3600*72,
        timeout=600
    )

    default_queue.enqueue(send_progress, "archived", *progress_args, depends_on=archive_job)

    webasset_job = webasset_queue.enqueue(
        create_webassets,
        depends_on=archive_job,
        timeout=3600 * 5
    )

    default_queue.enqueue(send_progress, "webassets_created", *progress_args, depends_on=webasset_job)

    return archive_job, webasset_job
