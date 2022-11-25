from django.core.exceptions import ValidationError

def file_size(value):
    filesize = value.size
    if filesize > 10000000:
        raise ValidationError('maximun size is 10mb')