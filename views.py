from django.shortcuts import render

def histories(request):
    return render(request, 'cmp/histories.html')
