import braintree
from django.conf import settings
from users.models import UserProfile
from dashboard.models import Ticket, Event
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404


# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    order_id = request.session.get('order_id')
    order = get_object_or_404(Ticket, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)

        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            event_id = request.session.get('event')
            seats = request.session.get('seats')

            event = Event.objects.get(id=event_id)

            # store the unique transaction id
            order.braintree_id = result.transaction.id

            event.attendance += seats
            event.save()

            return redirect('payment:done')
        else:
            order.delete()

            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()

        context = {
            'user': user,
            'user_profile': user_profile,
            'order': order,
            'client_token': client_token,
        }

        return render(request, 'payment/files/process.html', context)


def payment_done(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)

    context = {
        'user': user,
        'user_profile': user_profile,
    }

    return render(request, 'payment/files/done.html', context)


def payment_canceled(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)

    context = {
        'user': user,
        'user_profile': user_profile,
    }

    return render(request, 'payment/files/canceled.html', context)
