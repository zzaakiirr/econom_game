from django.urls import reverse


def make_transaction_request_url(sender, recipient, bet_amount):
    url = (
        "{reverse_url}?sender={sender}&recipient={recipient}".format(
                reverse_url=reverse("make_transaction"),
                sender=sender,
                recipient=recipient
            ) + "&amount=%s" % str(bet_amount)
    )
    return url
