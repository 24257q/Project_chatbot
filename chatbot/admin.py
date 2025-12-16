from django.contrib import admin
from .models import FQA, QuestionLog, HandoffRequest

@admin.register(FQA)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "is_active", "updated_at")
    search_fields = ("question_ar", "question_fr", "keywords", "answer_ar", "answer_fr")
    list_filter = ("category", "is_active")

@admin.register(QuestionLog)
class QuestionLogAdmin(admin.ModelAdmin):
    list_display = ("id", "detected_lang", "matched_score", "created_at")
    search_fields = ("message",)

@admin.register(HandoffRequest)
class HandoffRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_at")
    search_fields = ("name", "contact", "message")
    list_filter = ("status",)
