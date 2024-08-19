from cmp.models import Acknowledgement

def run():
    Acknowledgements = Acknowledgement.objects.all()
    Acknowledgements.delete()
