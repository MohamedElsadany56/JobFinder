from django import template


register = template.Library()

@register.filter
def calculate_duration(task):
    if task.deadline and task.publishedAt:
        duration = task.deadline - task.publishedAt
        return f"{duration.days} days, {duration.seconds // 3600} hours"
    return "N/A"