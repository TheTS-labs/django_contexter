from operator import attrgetter

from django.contrib.auth.models import Permission
from django.test import TestCase

from ..change_result import ChangeResult
from ..errors.reject_error import RejectError
from ..method_types import ALL_METHODS, ALL_SAFE_METHODS, ALL_UNSAFE_METHODS


class ChangeResultTestCase(TestCase):
    def test_no_changes_empty_dict(self):
        changer = ChangeResult({}, Permission, None)
        self.assertEqual(changer.fix_fields(Permission.objects), Permission.objects)

    def test_no_changes_None(self):
        changer = ChangeResult(None, Permission, None)
        self.assertEqual(changer.fix_fields(Permission.objects), Permission.objects)

    def test_hide_one(self):
        hide = ["codename"]
        changer = ChangeResult(
            {"allow_methods": ALL_SAFE_METHODS, "hidden_fields": hide},
            Permission,
            None,
        )

        records = Permission.objects
        fixed_fields = changer.fix_fields(records.all().first())

        fields_list = [field.name for field in Permission._meta.fields]
        del fields_list[fields_list.index(hide[0])]

        self.assertNotEqual(fixed_fields.codename, records.first().codename)
        self.assertEqual(fixed_fields.codename, "*" * len(hide[0]))
        self.assertEqual(
            attrgetter(*fields_list)(fixed_fields),
            attrgetter(*fields_list)(records.first()),
        )

    def test_hide_many(self):
        hide = ["codename"]
        changer = ChangeResult(
            {"allow_methods": ALL_SAFE_METHODS, "hidden_fields": hide},
            Permission,
            None,
        )

        records = Permission.objects
        fixed_fields = changer.fix_fields(records.all())

        fields_list = [field.name for field in Permission._meta.fields]
        del fields_list[fields_list.index(hide[0])]

        for i, record in enumerate(records.all()):
            self.assertNotEqual(fixed_fields[i].codename, record.codename)
            self.assertEqual(fixed_fields[i].codename, "*" * len(hide[0]))
            self.assertEqual(
                attrgetter(*fields_list)(fixed_fields[i]),
                attrgetter(*fields_list)(record),
            )

    def test_multiple_hide(self):
        hide = ["codename", "name"]
        changer = ChangeResult(
            {"allow_methods": ALL_SAFE_METHODS, "hidden_fields": hide},
            Permission,
            None,
        )

        records = Permission.objects
        fixed_fields = changer.fix_fields(records.all().first())

        fields_list = [field.name for field in Permission._meta.fields]
        del fields_list[fields_list.index(hide[0])]
        del fields_list[fields_list.index(hide[1])]

        self.assertNotEqual(fixed_fields.codename, records.first().codename)
        self.assertNotEqual(fixed_fields.name, records.first().name)
        self.assertEqual(fixed_fields.codename, "*" * len(hide[0]))
        self.assertEqual(fixed_fields.name, "*" * len(hide[1]))
        self.assertEqual(
            attrgetter(*fields_list)(fixed_fields),
            attrgetter(*fields_list)(records.first()),
        )

    def test_custom_hide(self):
        def hide(full_result, model, props, field, request):
            return "HIDED"

        changer = ChangeResult(
            {"allow_methods": ALL_SAFE_METHODS, "codename": hide, "hidden_fields": []},
            Permission,
            None,
        )

        records = Permission.objects
        fixed_fields = changer.fix_fields(records.all().first())

        fields_list = [field.name for field in Permission._meta.fields]
        del fields_list[fields_list.index("codename")]

        self.assertEqual(fixed_fields.codename, "HIDED")
        self.assertEqual(
            attrgetter(*fields_list)(fixed_fields),
            attrgetter(*fields_list)(records.first()),
        )
