from django.dispatch import receiver
from store.signals.signal import order_created


@receiver(order_created)
def order_created_signal(sender, **kwargs):
    print(kwargs['order'])