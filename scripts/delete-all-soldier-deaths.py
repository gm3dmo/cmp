from cmp.models import SoldierDecoration

def run():
    Decorations = SoldierDecoration.objects.all()
    Decorations.delete()
