from django.shortcuts import render


# Здесь прописывается рендер страниц, нужен шаблон, запрос

# Create your views here.
def test_view(request):
    return render(request, 'base.html', {})
