from django.db import models

# Create your models here.

class FQA(models.Model):
    category = models.CharField(max_length=80)
    question_ar = models.TextField()
    answer_ar = models.TextField()
    question_fr = models.TextField(blank=True, default="")
    answer_fr = models.TextField(blank=True, default="")
    keywords = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    embedding = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.category} | {self.question_fr[:40] or self.question_ar[:40]}"
    
class QuestionLog(models.Model):
    message = models.TextField()
    detected_lang = models.CharField(max_length=5, default="ar")
    matched_faq = models.ForeignKey(FQA, null=True, blank=True, on_delete=models.SET_NULL)
    matched_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)



class HandoffRequest(models.Model):
    name = models.CharField(max_length=120, blank=True, default="")
    contact = models.CharField(max_length=120, blank=True, default="")  # phone/email
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="new")  # new/processing/done