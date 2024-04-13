from django.shortcuts import render, redirect
from .models import Survey, Question, Answer
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

# Create your views here.
def home_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age_group = request.POST.get('age_group')
        survey = Survey.objects.create(name=name, gender=gender, age_group=age_group)
        request.session['survey_id'] = survey.id
        return redirect('question')
    return render(request, 'home.html')



def question_view(request):
    if 'survey_id' not in request.session:
        return redirect('home')  # Ensure survey is active or redirect

    survey_id = request.session['survey_id']
    survey = Survey.objects.get(id=survey_id)
    questions = Question.objects.filter(is_active=True)  # Ensure ordering
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page', 1)

    if request.method == 'POST':
        current_page_number = request.POST.get('page', page_number)

        question_id = request.POST.get('question_id')
        current_question = Question.objects.get(id=question_id)
        response = request.POST.get('response')
        
        Answer.objects.create(survey=survey, question=current_question, chosen_answer=response)

        # Attempt to go to the next page
        page_obj = paginator.get_page(current_page_number)
        print(page_obj)
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()
            return HttpResponseRedirect(f'?page={next_page_number}')
        else:
            del request.session['survey_id']
            return redirect('survey_complete')

    else:
        page_obj = paginator.get_page(page_number)
    
    return render(request, 'question.html', {'questions': page_obj})


def survey_complete_view(request):
    return render(request, 'survey_complete.html')


import plotly.express as px
import plotly.io as pio
from django.db.models import Count
# pip install plotly, pandas

def result_view(request):
    # data = {
    #     "fruits": ["Apples", "Bananas", "Cherries", "Dates"],
    #     "counts": [10, 15, 7, 5]
    # }

    age_group_counts = Survey.objects.values('age_group').annotate(count=Count('age_group')).order_by('age_group')
    # Plotly 차트 데이터 생성
    data = {
        'age_groups': [item['age_group'] for item in age_group_counts],
        'counts': [item['count'] for item in age_group_counts]
    }

    fig = px.pie(data, values='counts', names='age_groups', title='age groups Chart')

    # 차트를 HTML로 변환
    pie_chart_html = pio.to_html(fig, full_html=False, default_height='500px', default_width='700px')


    return render(request, 'result.html', {'pie_chart_html': pie_chart_html})
