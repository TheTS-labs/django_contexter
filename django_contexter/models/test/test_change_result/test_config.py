from django.contrib.auth.models import Permission
from django.test import TestCase

from django_contexter.models.change_result import ChangeResult
from django_contexter.models.method_types import ALL_SAFE_METHODS


class ChangeResultConfigTestCase(TestCase):
    """Sus? Test Configs."""

    def test_no_changes_empty_dict(self):
        """Except no changes in records with empty dict config."""
        changer = ChangeResult({}, Permission, None)
        self.assertEqual(changer.fix_fields(Permission.objects), Permission.objects)

    def test_no_changes_none(self):
        """Except no changes in records with None config."""
        changer = ChangeResult(None, Permission, None)
        self.assertEqual(changer.fix_fields(Permission.objects), Permission.objects)

    def test_no_changes_in_simple_and_extended(self):
        """Except no changes in record if field in hidden_fields AND recorded extended."""
        changer = ChangeResult(
            {"allow_methods": ALL_SAFE_METHODS, "hidden_fields": ["codename"], "codename": {}},
            Permission,
            None,
        )

        self.assertEqual(changer.fix_fields(Permission.objects), Permission.objects)
