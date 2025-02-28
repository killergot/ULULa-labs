from pydantic import BaseModel, ValidationError, field_validator
import phonenumbers

class PhoneModel(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    def validate_and_format_phone_number(cls, value):
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError('Invalid phone number')
            # Нормализация номера телефона
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            return formatted_number
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError('Invalid phone number format')

# Пример использования
try:
    phone = PhoneModel(phone_number='+1234567890')
    print(phone)
except ValidationError as e:
    print(e)