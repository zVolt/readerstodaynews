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
        parser.add_argument(
            '--dry_run',
            action='store_true',
            dest='dry_run',
            help='Dry run',
            default=False,
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        post_eol = datetime.now() - timedelta(days=int(days))
        # delete all posts
        post_queryset = Post.objects.filter(last_modified_on__lt=post_eol)
        print("deleting {} posts".format(post_queryset.count()))
        if not dry_run:
            post_queryset.delete()

        # delete all media which are not referred in posts
        media_item_ids = [media_item.id for post in Post.objects.all() for media_item in post.media_items.all()]
        orphan_media = Media.objects.exclude(id__in=media_item_ids)
        print("deleting {} media items".format(orphan_media.count()))
        # delete the media from cloudinary also
        if not dry_run:
            orphan_media.delete()
