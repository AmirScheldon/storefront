from django.core.exceptions import ValidationError

def validate_image_size(file):
    max_file_size = 6000
    
    if file.size > max_file_size * 1024:
        raise ValidationError(f'Your file size is greater than {max_file_size}KB!')

