from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ChatRequestSerializer, HandoffRequestSerializer
from .models import QuestionLog
from .services.fqa_matcher import detect_lang, best_faq_match_semantic

CONF_THRESHOLD = 0.78  # embeddings threshold (à ajuster après tests)


class ChatView(APIView):
    def post(self, request):
        ser = ChatRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        message = ser.validated_data["message"]
        lang = (ser.validated_data.get("lang") or "").strip() or detect_lang(message)

        faq, score = best_faq_match_semantic(message)


        if faq and score >= CONF_THRESHOLD:
            reply = faq.answer_ar if lang == "ar" else (faq.answer_fr or faq.answer_ar)
            matched_id = faq.id
        else:
            # fallback (sans LLM pour le moment)
            if lang == "ar":
                reply = (
                    "لم أفهم سؤالك بدقة. هل يمكنك إعادة صياغته؟ "
                    "أو اختر موضوعًا: التسجيل، القبول، التخصصات، الرسوم، التواصل."
                )
            else:
                reply = (
                    "Je n’ai pas bien compris. Pouvez-vous reformuler ? "
                    "Ou choisir un sujet : inscription, admission, filières, frais, contact."
                )
            matched_id = None

        # log
        QuestionLog.objects.create(
            message=message,
            detected_lang=lang,
            matched_faq=faq if matched_id else None,
            matched_score=float(score),
        )

        return Response(
            {
                "reply": reply,
                "lang": lang,
                "matched_faq_id": matched_id,
                "confidence": float(score),
            },
            status=status.HTTP_200_OK,
        )


class HandoffView(APIView):
    def post(self, request):
        ser = HandoffRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response({"ok": True, "id": obj.id}, status=status.HTTP_201_CREATED)
