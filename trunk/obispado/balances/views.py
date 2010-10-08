from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    # get_object_or_404(Poll, pk=poll_id)
    return render_to_response('balances/index.html')