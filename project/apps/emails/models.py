import sendgrid
from django.conf import settings
from django.db import models
from sendgrid.helpers.mail import Email, Mail, MailSettings, SandBoxMode

from project.core.models import BaseModel


class SendGridEmail(BaseModel):
    title = models.CharField(max_length=32, unique=True, verbose_name="title")
    template_id = models.CharField(max_length=64, verbose_name="template ID")

    class Meta:
        ordering = ['title']
        verbose_name = "SendGrid email"
        verbose_name_plural = "SendGrid emails"

    def send(self, to_email, from_email=settings.DEFAULT_FROM_EMAIL, data={}):
        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
        mail = Mail(to_email=Email(to_email), from_email=Email(from_email))
        mail.mail_settings = self._build_mail_settings()
        mail.template_id = self.template_id

        # https://github.com/sendgrid/sendgrid-python/issues/591
        request_body = mail.get()
        request_body['personalizations'][0]['dynamic_template_data'] = data

        try:
            response = sg.client.mail.send.post(request_body=request_body)
        except Exception as e:
            raise e
        else:
            if response.status_code not in [200, 202]:
                raise Exception("Unexpected status code.")

    def _build_mail_settings(self):
        mail_settings = MailSettings()
        mail_settings.sandbox_mode = SandBoxMode(settings.SENDGRID_SANDBOX_MODE)
        return mail_settings
