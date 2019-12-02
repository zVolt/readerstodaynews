from django.core.management.base import BaseCommand, CommandError
from api.models import Post, Media
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'remove posts older than number of days provided'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--days',
            action='store_true',
            dest='days',
            help='No of days for which the posts are kept',
            default=31,
        )

    def handle(self, *args, **options):
        days = options['days']
        post_eol = datetime.now() - timedelta(days=int(days))
        # delete all posts
        post_queryset = Post.objects.filter(last_modified_on__lt=post_eol)
        print("deleting {} posts".format(post_queryset.count()))
        post_queryset.delete()

        # delete all media which are not referred in posts
        media_item_ids = [media_item.id for post in Post.objects.all() for media_item in post.media_items.all()]
        orphan_media = Media.objects.exclude(id__in=media_item_ids)
        print("deleting {} media items".format(orphan_media.count()))
        orphan_media.delete()
