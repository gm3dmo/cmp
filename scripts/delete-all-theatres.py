from cmp.models import Theatre

def run():
    Theatres = Theatre.objects.all()
    Theatres.delete()
