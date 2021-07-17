def handle_file(f):
    with open('vehicle/data/'+f.name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            

            