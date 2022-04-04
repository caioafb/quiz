from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Label, Userr, Question, Option, Quiz, Result

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        quizzes = Quiz.objects.all().order_by('-pub_date')
        results = Result.objects.all().order_by('-pub_date')[:10]
        context = {
            'quizzes':quizzes,
            'results':results
        }
        return render(request, 'quiz/index.html', context)

@method_decorator(login_required, name='dispatch')
class QuizView(generic.View):
    def get(self, request, *args, **kwargs):
        quiz_id = kwargs['pk']
        quiz = Quiz.objects.get(pk=quiz_id)
        context = {
            'quiz':quiz
        }
        return render(request, 'quiz/quiz.html', context)

    def post(self, request, *args, **kwargs):
        quiz_id = kwargs['pk']
        quiz = Quiz.objects.get(pk=quiz_id)
        userr = request.user.userr
        count = 0
        max_score = 0
        score = 0
        answers = []
        for field in request.POST:
            if count > 0:
                key = request.POST[field]
                option = Option.objects.get(pk=key)
                answers.append(option.id)
                max_score = max_score + option.question.score
                if option.correct:
                    score = score + option.question.score
            count = count + 1

        result = (10 * score)/max_score
        grade = Result(grade = result, quiz = quiz, userr = userr, pub_date = timezone.now())
        grade.save()

        context = {
            'result':result,
            'answers':answers,
            'quiz':quiz
        }

        return render(request, 'quiz/result.html', context)

class ProfileView(generic.View):
    def get(self, request, *args, **kwargs):
        userr = request.user.userr
        context = {
            'userr':userr
        }
        return render(request, 'quiz/profile.html', context)


class NewQuizView(generic.View):
    def get(self, request, *args, **kwargs):
        themes = Label.objects.all().order_by("theme")
        context = {
            'themes':themes
        }
        return render(request, 'quiz/new_quiz.html', context)
    def post(self, request, *args, **kwargs):
        text = request.POST['text']
        userr = request.user.userr

        if Quiz.objects.filter(title=text).exists():
            return render(request, 'quiz/index.html', {'error': 'Quiz with the same title already registered.'})

        quiz = Quiz(title=text, pub_date = timezone.now(), author=userr)
        quiz.save()

        count = 0
        for field in request.POST:
            if count > 1:
                question = Question.objects.get(pk=field)
                if question:
                    quiz.question.add(question)
            count = count + 1
        quiz.save()
        quizzes = Quiz.objects.all().order_by('-pub_date')
        context = {
            'quizzes':quizzes,
            'msg': 'Quiz registered successfully!'
        }
        return render(request, 'quiz/index.html', context)

class NewQuestionView(generic.View):
    def get(self, request, *args, **kwargs):
        themes = Label.objects.all().order_by("theme")
        context = {
            'themes': themes
        }
        return render(request, 'quiz/new_question.html', context)

    def post(self, request, *args, **kwargs):
        text = request.POST['text']
        op1 = request.POST['op1']
        op2 = request.POST['op2']
        op3 = request.POST['op3']
        op4 = request.POST['op4']
        op5 = request.POST['op5']
        score = request.POST['score']
        answer = request.POST['correct']
        themeid = request.POST['theme']
        userr = request.user.userr

        if Question.objects.filter(text=text).exists():
            return render(request, 'quiz/index.html', {'error': 'Question with same text already registered.'})

        if themeid:
            theme = Label.objects.get(pk=themeid)
        else:
            return render(request, 'quiz/new_question.html', {'error': 'A theme must be selected.'})

        if not resposta:
            return render(request, 'quiz/new_question.html', {'error': 'An option must be correct.'})

        question = Question(text=text, pub_date = timezone.now(), label=theme, author=userr, score=score)
        option1 = Option(text = op1, question = question)
        option2 = Option(text = op2, question = question)
        question.save()
        option1.save()
        option2.save()
        if op3:
            option3 = Option(text = op3, question = question)
            option3.save()
        if op4:
            option4 = Option(text = op4, question = question)
            option4.save()
        if op5:
            option5 = Option(text = op5, question = question)
            option5.save()

        if answer == "1":
            option1.correct = True
            option1.save()
        elif answer == "2":
            option2.correct = True
            option2.save()
        elif answer == "3":
            option3.correct = True
            option3.save()
        elif answer == "4":
            option4.correct = True
            option4.save()
        elif answer == "5":
            option5.correct = True
            option5.save()

        themes = Label.objects.all().order_by("theme")
        context = {
            'themes': themes,
            'msg': 'Question registered successfully!'
        }
        return render(request, 'quiz/new_question.html', context)

class NewThemeView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'quiz/new_theme.html')

    def post(self, request, *args, **kwargs):
        theme = request.POST['theme']
        if not Label.objects.filter(theme=theme).exists():
            theme = Label(theme=theme)
            theme.save()
        else:
            return render(request, 'quiz/new_theme.html', {'error': 'Theme already registered.'})
        themes = Label.objects.all().order_by("theme")
        context = {
            'theme': theme
        }
        return render(request, 'quiz/new_question.html', context)

class NewUserView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'quiz/new_user.html')

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['login']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        quizzes = Quiz.objects.all().order_by('-pub_date')
        results = Result.objects.all().order_by('-pub_date')[:10]
        context = {
            'quizzes':quizzes,
            'results':results,
            'msg':'User registered successfully!'
        }

        if (name and lastname and email and username and password1 and password2):
            if password1 == password2:
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(username, email, password1)
                        user.first_name = name
                        user.last_name = lastname
                        user.save()
                        userr = Userr(name = name, user = user)
                        userr.save()
                    else:
                        return render(request, 'quiz/new_user.html', {'error': 'E-mail already registered.'})
                else:
                    return render(request, 'quiz/new_user.html', {'error': 'Login already registered.'})
            else:
                return render(request, 'quiz/new_user.html', {'error': 'Passwords are not the same.'})
        else:
            return render(request, 'quiz/new_user.html', {'error': 'All parameters must be filled in.'})
        login(request, user)
        return render(request, 'quiz/new_user.html', context)





