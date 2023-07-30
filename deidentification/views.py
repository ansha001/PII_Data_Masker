from django.shortcuts import render, HttpResponse
from .categorize import detect_document_type
from .categorize import extract_words_from_document
from .obfuscate_mask import replace_ners, ner_replacements, mask

from .image import overlay_ocr_text
import os

def index(request):
    return render(request, "index.html")

def detect(request):
    return render(request, "detection.html")

def textinput(request):
    result1 = "Unknown"

    text_input = request.GET.get("text_input")
    print(text_input)
    result1 = detect_document_type(text_input)
    return render(request, "detection.html", {"result1": result1, "text_input": text_input})

def fileinput(request):
    result2 = "Unknown"

    file = request.FILES.get('file')
    
    if file is not None:
            sample = extract_words_from_document(file)
            result2= detect_document_type(' '.join(sample))
    return render(request, 'detection.html', {'result2': result2})

    
def free_text(request):
    option = None
    output_text = None
    input_text = None

    if request.method == 'POST':
        input_text = request.POST.get('freetextinput', '')
        print(input_text)

        if 'mask' in request.POST:
            option = 'mask'
        elif 'obfuscate' in request.POST:
            option = 'obfuscate'
        else:
            option = None

        if option == 'mask':
            print("mask selected")
            output_text = mask(input_text)
        elif option == 'obfuscate':
            print("obfuscate selected")
            output_text = replace_ners(input_text, ner_replacements)

    context = {}
    if input_text is not None:
        context['input_text'] = input_text
    if output_text is not None:
        context['output_text'] = output_text

    return render(request, "freetext.html", context)

def table(request):
    return render(request, "table.html")

def document(request):
    option = None
    input_text = None
    output_text = None
    file = None

    if request.method == 'POST':
        file = request.FILES.get('documentinput')
        if file is not None:
            input_text = extract_words_from_document(file)
            input_text = " ".join(input_text)
            if 'mask' in request.POST:
                option = 'mask'
            elif 'obfuscate' in request.POST:
                option = 'obfuscate'
            else:
                option = None

            if option == 'mask':
                print("mask selected")
                output_text = mask(input_text)
            elif option == 'obfuscate':
                print("obfuscate selected")
                output_text = replace_ners(input_text, ner_replacements)
        else:
            pass

        

    context = {}
    if input_text is not None:
        context['input_text'] = input_text
    if output_text is not None:
        context['output_text'] = output_text

    return render(request, "document.html",context)

def image(request):
    file = None
    old_load = False
    if request.method == 'POST':
        file = request.FILES.get('dicominput')


        if "export-img" in request.POST:
            image_name = "masked_image.jpg"
            image_path = os.path.join('static/public',image_name)
            with open(image_path, 'rb') as image_file:
                response = HttpResponse(image_file.read(), content_type='image/jpeg')
                response['Content-Disposition'] = f'attachment; filename={image_name}'
                return response

    if file is not None:
            input_img_path = 'static/public/input_img.jpg'
            with open(input_img_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            overlay_ocr_text(input_img_path, vertical_offset=0)
            old_load = True

    context = {
        'old_load': old_load
    }

    return render(request, "image.html",context)
