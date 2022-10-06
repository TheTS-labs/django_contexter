from operator import attrgetter

from django.contrib.auth.models import Permission
from django.test import TestCase

from ...change_result import ChangeResult
from ...errors.reject_error import RejectError
from ...method_types import ALL_METHODS, ALL_SAFE_METHODS, ALL_UNSAFE_METHODS


class ChangeResultConfigTestCase(TestCase):
    def test_no_changes_empty_dict(self):
        changer = ChangeResult({}, Permission, None)
        self.assertEqual(changer.fix_fields(Permission.objects), Permission.objects)

    def test_no_changes_None(self):
        changer = ChangeResult(None, Permission, None)
        self.assertEqual(changer.fix_fields(Permission.objects), Permission.objects)
