from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    # 실제 CustomUser 모델의 필드를 반영
    list_display = ('id', 'username', 'phone', 'gender', 'birth', 'club', 'team', 'get_tiers_display' ,'image_url')  
    filter_horizontal = ('tiers',)  # ManyToManyField를 사용하는 필드 이름
    ordering = ('-id',)  # 실제 CustomUser 모델의 USERNAME_FIELD를 사용
    
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
    
    def delete_queryset(self, request, queryset):
        # soft delete 기능 : db에서 삭제 하지 않고 불리언 타입으로 true 1 처리
        for obj in queryset:
            obj.is_deleted = True
            obj.save()
    

# 장고 어드민 사이트에 CustomUser 모델을 CustomUserAdmin 설정으로 등록
admin.site.register(CustomUser, CustomUserAdmin)