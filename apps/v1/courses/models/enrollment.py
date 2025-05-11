# from django.contrib.auth import get_user_model
# from django.db import models
# from django_extensions.db.models import TimeStampedModel
# from ...groups.models import StudentGroup
#
# User = get_user_model()
#
# class Enrollment(TimeStampedModel):
#     group = models.ForeignKey(
#         StudentGroup,
#         on_delete=models.CASCADE,
#         related_name="enrollments"
#     )
#     student = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         limit_choices_to={
#             "role": "student"
#         }
#     )