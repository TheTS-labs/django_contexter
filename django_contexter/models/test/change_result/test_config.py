from django.contrib.auth.models import Permission
from django.test import TestCase

from django_contexter.models.change_result import ChangeResult


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
