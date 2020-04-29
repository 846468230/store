from .models import Video
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from store.settings import VOD_SECRETID,VOD_SECRETKEY
from qcloud_vod.vod_upload_client import VodUploadClient
from qcloud_vod.model import VodUploadRequest
import os

upload_file = Signal(providing_args=["path","instance"])
@receiver(upload_file, sender=Video)
def save_video(sender, **kwargs):
    path = kwargs['path']
    instance = kwargs['instance']
    client = VodUploadClient(VOD_SECRETID,VOD_SECRETKEY)
    request = VodUploadRequest()
    request.MediaFilePath = path
    try:
        response = client.upload("ap-beijing",request)
        instance.vod_id = response.FileId
        instance.url = response.MediaUrl
        instance.save()
    except Exception as e:
        print(e)


# @receiver(post_save, sender=Video, dispatch_uid="video_updated")
# def create_video(sender, instance=None, created=False, **kwargs):
#     if created:
#         name = instance.video_file.field.generate_filename(instance.video_file.instance,instance.video_file.name)
#         base_locaton = instance.video_file.storage.base_location
#         path = os.path.join(base_locaton,name)
#         client = VodUploadClient(VOD_SECRETID, VOD_SECRETKEY)
#         request = VodUploadRequest()
#         request.MediaFilePath = path
#         try:
#             response = client.upload("ap-beijing", request)
#             instance.vod_id = response.FileId
#             instance.url = response.MediaUrl
#             instance.save()
#         except Exception as e:
#             print(e)