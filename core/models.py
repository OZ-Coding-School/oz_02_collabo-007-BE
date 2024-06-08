from django.db import models

from core.manager import SoftDeleteManager


class TimeStampedModel(models.Model):  # 테이블에 생성시간 , 수정시간 기능을 넣어주기 위한 공통 모델
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# soft delete 모델 (레코드를 실제로 데이터베이스에서 삭제하지 않고, 삭제된 것으로 표시하여 나중에 복구할 수 있는 기능을 구현할 수 있음)
class SoftDeleteModel(models.Model):
    # 대회 생성했다가 삭제, 경기기록 삭제, 유저 탈퇴, admin 부분에서 삭제기능 진행 (soft delete)
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True
