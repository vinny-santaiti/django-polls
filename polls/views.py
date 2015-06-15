from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from polls.models import Poll, Choice, Answer

from django.views import generic

# generic class based views
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.filter(published__lte=timezone.now()).order_by("-published")[:5]

class DetailView(generic.DetailView):
    model = Poll
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Poll
    template_name = "polls/results.html"


# regular views
def index(request):
    latest_poll_list = Poll.objects.order_by('-published')
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)
   
def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
    """ capture vote """    
    poll = get_object_or_404(Poll, pk=poll_id)
    import pdb; pdb.set_trace()
    for question in poll.question_set.all():
        form_choice_id = request.POST.get('choice%s' % question.id) 
        if form_choice_id:      
            try:
                selected_choice = question.choice_set.get(pk=form_choice_id) # access POST data
            except (KeyError, Choice.DoesNotExist) as e:
                # redisplay the poll voting form
                return render(request, 'polls/detail.html', {
                    'poll': poll,
                    'error_message': "Error: Please select a choice",
                })
            else:
                Answer.objects.create(choice=selected_choice)
        # selected_choice.votes += 1
        # selected_choice.save()
        # always return HttpResponseRedirect after success of POST data, 
        # this prevents data from being posted twice, if user hits back button.
    return HttpResponseRedirect(reverse('results', args=[poll.id]))

#def results(request, poll_id):
#    return HttpResponse("looking at results of poll %s " % poll_id)
    
#def vote(request, poll_id):
#    return HttpResponse("voting on poll %s " % poll_id)

