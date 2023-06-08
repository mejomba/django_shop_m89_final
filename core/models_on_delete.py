from django.db import connections
from django.utils import timezone
from collections import defaultdict


def SOFT_CASCADE(collector, field, sub_objs, using):
    collector.data = defaultdict(set)

    collector.collect(
        sub_objs,
        source=field.remote_field.model,
        source_attr=field.name,
        nullable=field.null,
        fail_on_restricted=False,
    )

    collector.data = defaultdict(set)

    for item in sub_objs:
        item.is_deleted = True
        item.delete_date = timezone.now()
        item.save()

    if field.null and not connections[using].features.can_defer_constraint_checks:
        collector.add_field_update(field, None, sub_objs)

