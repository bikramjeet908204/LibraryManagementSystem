from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AuthorSerializer, BookSerializer, SeriesSerializer, PublisherSerializer, PersonSerializer, LocationSerializer, BookAvailableSerializer, BookUnavailableSerializer, StudentSerializer, ProfessorSerializer, RegistrationSerializer
from .models import Author, Location, Book, Available_Book, Series, Unavailable_Book, Publisher, Person, Student, Professor

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm, RegisterForm

# Create your views here.


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer


class BookAvailableViewSet(viewsets.ModelViewSet):
    queryset = Available_Book.objects.all()
    serializer_class = BookAvailableSerializer


class BookUnavailableViewSet(viewsets.ModelViewSet):
    queryset = Unavailable_Book.objects.all()
    serializer_class = BookUnavailableSerializer


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all().order_by('id')
    serializer_class = PublisherSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class ProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorSerializer
    queryset = Professor.objects.all()


class searchForPerson(APIView):
    def get(self, request):
        if(request.method != 'GET'):
            return Response({'Error': 'Method not GET'}, status=status.HTTP_400_BAD_REQUEST)
        query_name = request.query_params.get('query_name', None)
        if ((query_name is None)):
            return Response({'Error': 'Query must include name as query_name'}, status=status.HTTP_400_BAD_REQUEST)
        person_list = Person.objects.filter(name=query_name)
        if not person_list.exists():
            return Response({'Error': 'No Person with requested id exists'}, status=status.HTTP_204_NO_CONTENT)
        results = []
        for x in person_list:
            results.append(PersonSerializer(x).data)
        return Response(results)


def index(request):
    return render(request, 'api/index.html')


def register(request):
    if(request.method == 'POST'):
        form = RegisterForm(request.POST)
        if form.is_valid():
            ucid = form.cleaned_data['ucid']
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            faculty = form.cleaned_data['faculty']
            print(ucid)
            print(name)
            print(password)
            print(password2)

            if(password != password2):
                return HttpResponseRedirect('/register/')

            user_instance = Person.objects.create(
                ucid=ucid, password=password, name=name, faculty=faculty)
            user_instance.save()

            return HttpResponseRedirect('/login/')
    else:
        form = RegisterForm()

    return render(request, 'api/register.html', {'form': form})


person = None


def login(request):
    if(request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            ucid = form.cleaned_data['ucid']
            password = form.cleaned_data['password']

            person_list = Person.objects.all()
            found = False
            for p in person_list:
                if (p.ucid == ucid and p.password == password):
                    found = True
                    global person
                    person = p
                    break

            if (found == False):
                return HttpResponseRedirect('notSuccess/')

            return HttpResponseRedirect('/welcome/')
    else:
        form = LoginForm()

    return render(request, 'api/login.html', {'form': form})


def welcome(request):
    print(person.ucid)
    return render(request, 'api/welcome.html')


def unsuccessful(request):
    return render(request, 'api/notSuccess.html')


def display_books(request):
    books = Book.object.all()
    return render(request, 'api/viewBooks.html', {'books': books})


'''
def search_book(request):
    if (request.method != 'GET'):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = SearchBookForm(request.GET)
        if form.is_valid:
            query_name = form.cleaned_data["book_name"]
            print(query_name)

            res = []
            books = Book.object.filter(title=query_name)

            for b in books:
                res.append(BookSerializer(b).data)

            return Response(res)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

'''
@api_view(['POST', ])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid:
            person = serializer.save()
            data['response'] = "success"
            data['ucid'] = person.ucid
            data['password'] = person.password
            else:
                data = serializer.errors
                return Response(data)
'''
