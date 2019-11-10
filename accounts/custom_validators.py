from django.utils.translation import ngettext  # https://docs.python.org/2/library/gettext.html#gettext.ngettext
from django.core.exceptions import ValidationError
import functools
import gzip
import os
import re
from difflib import SequenceMatcher

from django.conf import settings
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.functional import lazy
from django.utils.html import format_html
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _, ngettext


@functools.lru_cache(maxsize=None)
def get_default_password_validators():
    return get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)


def get_password_validators(validator_config):
    validators = []
    for validator in validator_config:
        try:
            klass = import_string(validator['NAME'])
        except ImportError:
            msg = "The module in NAME could not be imported: %s. Check your AUTH_PASSWORD_VALIDATORS setting."
            raise ImproperlyConfigured(msg % validator['NAME'])
        validators.append(klass(**validator.get('OPTIONS', {})))

    return validators



def validate_password(password, user=None, password_validators=None):
    """
    Validate whether the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        raise ValidationError(errors)



def password_changed(password, user=None, password_validators=None):
    """
    Inform all validators that have implemented a password_changed() method
    that the password has been changed.
    """
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        password_changed = getattr(validator, 'password_changed', lambda *a: None)
        password_changed(password, user)



def password_validators_help_texts(password_validators=None):
    """
    Return a list of all help texts of all configured validators.
    """
    help_texts = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        help_texts.append(validator.get_help_text())
    return help_texts



def _password_validators_help_text_html(password_validators=None):
    """
    Return an HTML string with all help texts of all configured validators
    in an <ul>.
    """
    help_texts = password_validators_help_texts(password_validators)
    help_items = [format_html('<li>{}</li>', help_text) for help_text in help_texts]
    return '<ul>%s</ul>' % ''.join(help_items) if help_items else ''


password_validators_help_text_html = lazy(_password_validators_help_text_html, str)


#https://github.com/django/django/blob/master/django/contrib/auth/common-passwords.txt.gz
#https://docs.djangoproject.com/en/2.0/_modules/django/contrib/auth/password_validation/#MinimumLengthValidator
#https://stackoverflow.com/questions/45786879/override-password-validation-messages

# https://docs.djangoproject.com/en/2.0/_modules/django/contrib/auth/password_validation/#MinimumLengthValidator
class MyCustomMinimumLengthValidator(object):
    def __init__(self, min_length=8):  # put default min_length here
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    # silly, I know, but if your min length is one, put your message here
                    "Túl rövid jelszó, legalább  %(min_length)d karakterből kell állnia.",
                    # if it's more than one (which it probably is) put your message here
                    "Túl rövid jelszó, legalább  %(min_length)d karakterből kell állnia.",
                    self.min_length
                ),
            code='password_too_short',
            params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            # you can also change the help text to whatever you want for use in the templates (password.help_text)
            "Túl rövid jelszó, legalább  %(min_length)d karakterből kell állnia.",
            "Túl rövid jelszó, legalább  %(min_length)d karakterből kell állnia.",
            self.min_length
        ) % {'min_length': self.min_length}


class MyCustomCommonPasswordValidator:
    DEFAULT_PASSWORD_LIST_PATH = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'common-passwords.txt.gz'
    )

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        try:
            with gzip.open(password_list_path) as f:
                common_passwords_lines = f.read().decode().splitlines()
        except IOError:
            with open(password_list_path) as f:
                common_passwords_lines = f.readlines()

        self.passwords = {p.strip() for p in common_passwords_lines}

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                ("Ez a jelszó túl gyakori."),
                code='password_too_common',
            )

    def get_help_text(self):
        return ("Ez a jelszó túl gyakori.")


class MyCustomNumericPasswordValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                ("A jelszó nem állhat kizárólag numerikus karakterekből."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return ("A jelszó nem állhat kizárólag numerikus karakterekből.")

class MyCustomUserAttributeSimilarityValidator:
    DEFAULT_USER_ATTRIBUTES = ('username', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        ("A jelszavad túlságosan hasonlít ehhez: %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return ("A jelszavad ne hasonlítson más, megadott felhasználói adataidhoz.")