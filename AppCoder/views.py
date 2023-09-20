from django.shortcuts import render
from AppCoder.models import Curso, Avatar
from django.template import loader
from django.http import HttpResponse
from AppCoder.forms import Curso_form , UserEditForm
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.



def inicio(request):
    return render( request , "padre.html")

def quienes_somos(request):
    return render(request, "quienes_somos.html")


def cursos(request):
    cursos = Curso.objects.all()
    return render (request, "cursos.html", {"cursos":cursos})

def alta_curso(request , nombre , comision):
    curso = Curso(nombre=nombre, comision=comision)
    curso.save()
    texto = f"Se guardo en el BD el Curso: {curso.nombre} Comision{curso.comision}"
    return HttpResponse(texto)


def mis_compras(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "mis_compras.html", {"url":avatares[0].imagen.url})
    

def productos(request):
    print(request.user.id)
    if request.user.id != None: 
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, "productos.html", {"url":avatares[0].imagen.url})
    else:
        return render(request , "productos.html")

def curso_formulario(request):
    
    if request.method == "POST":

        mi_formulario = Curso_form( request.POST )

        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
             
            curso = Curso( nombre=datos['nombre'], comision=datos['comision'])
            curso.save()
            return render(request, "formulario.html")
        
    return render( request, "formulario.html" )


def buscar_curso(request):
    return render( request, "buscar_curso.html")

def buscar(request):
    
    if request.GET['nombre']:
        nombre = request.GET['nombre']
        cursos = Curso.objects.filter(nombre__icontains = nombre)
        return render( request, "resultado_busqueda.html", {"cursos":cursos})
    else:
        return HttpResponse("Campo vacio")
    
@login_required
def eliminar_curso(request, id):

    curso = Curso.objects.get(id=id)
    curso.delete()

    curso = Curso.objects.all()

    return render (request, "cursos.html" , {"cursos": cursos})

@login_required
def editar(request, id):

    curso = Curso.objects.get(id=id)

    if request.method == "POST":

        mi_formulario = Curso_form( request.POST )
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso.nombre = datos['nombre']
            curso.comision = datos['comision']
            curso.save()

            cursos = Curso.objects.all()
            return render(request, "cursos.html", {"cursos":cursos})
    else:
        mi_formulario = Curso_form(initial={"nombre":curso.nombre , "comision": curso.comision})
        
        return render(request, "editar_curso.html", {"mi_formulario": mi_formulario, "curso": curso})


def login_request(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data= request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")

            user = authenticate(username=usuario , password=contra)
            if user is not None:
                login(request, user)
                avatares = Avatar.objects.filter(user=request.user.id)
                return render(request, "inicio.html", {"url":avatares[0].imagen.url})
            else:
                return HttpResponse(f"Usuario incorrecto")
        else:
            return HttpResponse(f"FORM INCORRECTO {form}" )
            


    form = AuthenticationForm()
    return render (request, "login.html" , {"form": form})

def register(request):

    if request.method == "POST":
        form= UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse("Usuario creado")
    else:
        form = UserCreationForm()
    return render(request, "registro.html" , {"form": form})


def editarPerfil(request):

    usuario = request.user
    if request.method == "POST":

        miFormulario = UserEditForm(request.POST)
        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            usuario.email = informacion['email']
            password = informacion['password1']
            usuario.set_password(password)
            usuario.save()
            return render (request, "inicio.html")
    
    else:
        miFormulario  = UserEditForm(initial={'email': usuario.email})
        return render (request, 'editar_perfil.html', {"miFormulario":miFormulario, "usuario":usuario})






          

          

        