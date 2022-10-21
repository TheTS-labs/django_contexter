from operator import attrgetter

from django.contrib.auth.models import Permission
from django.test import TestCase

from django_contexter.models.change_result import ChangeResult
from django_contexter.models.method_types import ALL_SAFE_METHODS

# ? Why need noqa: WPS437?
# * Because Django doesn't forbid the use of _meta
# https://docs.djangoproject.com/en/4.1/ref/models/meta/


def _to_be_hided(full_result, model, props, field, request):
    return "HIDED"


empty = frozenset()
codename_hide_str = "Hided"
standart_hide = {
    "codename": codename_hide_str,
}
fucntional_hide = {
    "codename": _to_be_hided,
}


class ChangeResultTestCase(TestCase):
    """Test result changing(hiding)."""

    def test_hide_one(self):
        """Easy Level: Hide only one field."""
        changer = ChangeResult(
            {"allow_methods": ALL_SAFE_METHODS, "hidden_fields": standart_hide},
            Permission,
            None,
        )

        records = Permission.objects
        fixed_fields = changer.fix_fields(records.all().first())

        self._check_hided_attrs(
            standart_hide,
            records.all().first(),
            fixed_fields,
            codename=codename_hide_str,
        )
        self._check_other_attrs(
            self._get_fileld_names_list(Permission, standart_hide),
            fixed_fields,
            records.first(),
        )

    def test_hide_many(self):
        """Intermediate Level: Hide only one field in many records."""
        changer = ChangeResult(
            {"allow_methods": ALL_SAFE_METHODS, "hidden_fields": standart_hide},
            Permission,
            None,
        )

        records = Permission.objects
        fixed_fields = changer.fix_fields(records.all())

        for fixed_field, record in zip(fixed_fields, records.all()):
            self._check_hided_attrs(
                standart_hide,
                record,
                fixed_field,
                codename=codename_hide_str,
            )
            self._check_other_attrs(
                self._get_fileld_names_list(Permission, standart_hide),
                fixed_field,
                record,
            )

    def test_multiple_hide(self):
        """Intermediate++ Level: Hide many fields."""
        hide = {"name": "Hided"}
        hide.update(standart_hide)
        changer = ChangeResult(
            {"allow_methods": ALL_SAFE_METHODS, "hidden_fields": hide},
            Permission,
            None,
        )

        records = Permission.objects
        fixed_fields = changer.fix_fields(records.all().first())

        self._check_hided_attrs(
            hide,
            records.all().first(),
            fixed_fields,
            codename=codename_hide_str,
            name="Hided",
        )
        self._check_other_attrs(
            self._get_fileld_names_list(Permission, hide),
            fixed_fields,
            records.first(),
        )

    def test_custom_hide(self):
        """Hard Level: Use custom hide function."""
        changer = ChangeResult(
            {"allow_methods": ALL_SAFE_METHODS, "hidden_fields": fucntional_hide},
            Permission,
            None,
        )

        records = Permission.objects
        fixed_fields = changer.fix_fields(records.all().first())

        self._check_hided_attrs(
            standart_hide,
            records.all().first(),
            fixed_fields,
            codename="HIDED",
        )
        self._check_other_attrs(
            self._get_fileld_names_list(Permission, standart_hide),
            fixed_fields,
            records.first(),
        )

    def _get_fileld_names_list(self, model_instance, except_fields=empty):
        field_names = [field.name for field in model_instance._meta.fields]

        for element in sorted(except_fields, reverse=True):
            field_names.remove(element)

        return field_names

    def _check_other_attrs(self, attrs, proper_attrs, testing_attrs):
        self.assertEqual(
            attrgetter(*attrs)(testing_attrs),
            attrgetter(*attrs)(proper_attrs),
        )

    def _check_hided_attrs(self, hide_attrs, initial_queryset, testing_queryset, **kwargs):
        for attr in hide_attrs:
            self.assertNotEqual(getattr(initial_queryset, attr), getattr(testing_queryset, attr))
            self.assertEqual(getattr(testing_queryset, attr), kwargs.get(attr))
