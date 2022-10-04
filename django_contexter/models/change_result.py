class ChangeResult:
    """Change result with custom Access Policy"""

    def __init__(self, props, model, request):
        self.model = model
        self.props = props
        self.request = request

    def _update(self, field_name, value, full_result):
        if isinstance(full_result, self.model):
            setattr(full_result, field_name, value)
        else:
            for record in full_result:
                setattr(record, field_name, value)

        return full_result

    def fix_fields(self, full_result):
        if self.props is None or self.props == {}:
            return full_result

        for field in self.model._meta.get_fields():
            if (
                field.name in self.props["hidden_fields"]
                and field.name not in self.props
            ):
                full_result = self._update(
                    field.name, "*" * len(field.name), full_result
                )
            elif (
                field.name in self.props
                and field.name not in self.props["hidden_fields"]
            ):
                full_result = self._update(
                    field.name,
                    self.props[field.name](
                        full_result=full_result,
                        model=self.model,
                        props=self.props,
                        field=field,
                        request=self.request,
                    ),
                    full_result,
                )

        return full_result
