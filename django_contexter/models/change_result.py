"""Change result with custom Access Policy."""


class ChangeResult(object):
    """Change result with custom Access Policy."""

    def __init__(self, props, model, request):
        """
        Save args.

        Args:
            props: Writed Extended props
            model: Model instance
            request: Django request object
        """
        self.model = model
        self.props = props
        self.request = request

    def fix_fields(self, full_result):
        """
        Fix fields accroding to Access Policy.

        Args:
            full_result: Full request QuerySet

        Returns:
            Changed QuerySet
        """
        if not self.props:
            return full_result

        for field in self.model._meta.get_fields():  # noqa: WPS437
            if field.name in self.props["hidden_fields"]:
                field_config = self.props["hidden_fields"].get(field.name)
                if callable(field_config):
                    function_result = field_config(
                        full_result=full_result,
                        model=self.model,
                        props=self.props,
                        field=field,
                        request=self.request,
                    )

                    full_result = self._update(
                        field.name,
                        function_result,
                        full_result,
                    )
                else:
                    full_result = self._update(
                        field.name, field_config, full_result,
                    )

        return full_result

    def _update(self, field_name, update_value, full_result):
        if isinstance(full_result, self.model):
            setattr(full_result, field_name, update_value)
        else:
            for record in full_result:
                setattr(record, field_name, update_value)

        return full_result
