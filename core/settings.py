_DEFAULT_AUTH_USER_MODEL = 'account.User'
_DEFAULT_SECTION_MODEL = 'section.Section'


try:
    from django.conf import settings as project_settings

    AUTH_USER_MODEL = getattr(
        project_settings, 'AUTH_USER_MODEL', _DEFAULT_AUTH_USER_MODEL)

    SECTION_MODEL = getattr(
        project_settings, 'SECTION_MODEL', _DEFAULT_SECTION_MODEL)

except ImportError:
    AUTH_USER_MODEL = _DEFAULT_AUTH_USER_MODEL
    SECTION_MODEL = _DEFAULT_SECTION_MODEL
