import cv2
import numpy as np
from django.shortcuts import render
from django.core.files.storage import default_storage
from .forms import ImageUploadForm
from PIL import Image

def pencil_sketch_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            image_path = default_storage.save(image_file.name, image_file)
            img = Image.open(default_storage.open(image_path)).convert('RGB')
            open_cv_image = np.array(img)  
            open_cv_image = open_cv_image[:, :, ::-1].copy()  
            gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            inverted_image = 255 - gray_image
            blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
            inverted_blurred = 255 - blurred
            pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
            sketch_image_path = 'sketch_' + image_file.name
            cv2.imwrite(default_storage.path(sketch_image_path), pencil_sketch)

            return render(request, 'output.html', {'sketch_image': sketch_image_path})
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})
