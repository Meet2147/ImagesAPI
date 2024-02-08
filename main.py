from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

@app.post("/convert/png_to_jpg/")
async def png_to_jpg(png_file: UploadFile = File(...)):
    # Check if the uploaded file is a PNG file
    if not png_file.filename.lower().endswith('.png'):
        return {"error": "Please upload a PNG file."}
    
    # Read the image file
    image_data = await png_file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # Convert the image to RGB (necessary step before saving as JPEG)
    rgb_im = image.convert('RGB')
    
    # Save the image to a bytes buffer instead of file on disk
    buf = io.BytesIO()
    rgb_im.save(buf, format='JPEG')
    buf.seek(0)
    
    # Prepare the headers for file download
    headers = {
        'Content-Disposition': 'attachment; filename="converted_image.jpg"'
    }
    
    # Create a StreamingResponse with the buffer and headers for download
    return StreamingResponse(buf, media_type="image/jpeg", headers=headers)

@app.post("/convert/webp_to_png/")
async def webp_to_png(webp_file: UploadFile = File(...)):
    # Check if the uploaded file is a WebP file
    if not webp_file.filename.lower().endswith('.webp'):
        return {"error": "Please upload a WebP file."}
    
    # Read the image file
    image_data = await webp_file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # Convert the image to PNG by saving it to a bytes buffer
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    
    # Prepare the headers for file download
    headers = {
        'Content-Disposition': 'attachment; filename="converted_image.png"'
    }
    
    # Create a StreamingResponse with the buffer and headers for download
    return StreamingResponse(buf, media_type="image/png", headers=headers)

@app.post("/convert/jpg_to_png/")
async def jpg_to_png(jpg_file: UploadFile = File(...)):
    # Check if the uploaded file is a JPG file
    if not jpg_file.filename.lower().endswith(('.jpg', '.jpeg')):
        return {"error": "Please upload a JPG file."}
    
    # Read the image file
    image_data = await jpg_file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # No need to convert to RGB as JPG files are already in this format
    
    # Save the image to a bytes buffer as PNG
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    
    # Prepare the headers for file download
    headers = {
        'Content-Disposition': 'attachment; filename="converted_image.png"'
    }
    
    # Create a StreamingResponse with the buffer and headers for download
    return StreamingResponse(buf, media_type="image/png", headers=headers)

@app.post("/resize/")
async def resize_image(
        image_file: UploadFile = File(...),
        width: int = Form(...),
        height: int = Form(...)
    ):
    # Check if the uploaded file is an image
    if not image_file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        return {"error": "Please upload an image file."}
    
    # Read the image file
    image_data = await image_file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # Define the new size
    new_size = (width, height)
    
    # Resize the image
    resized_img = image.resize(new_size)
    
    # Save the resized image to a bytes buffer
    buf = io.BytesIO()
    format = 'JPEG' if image_file.filename.lower().endswith(('.jpg', '.jpeg')) else 'PNG'
    resized_img.save(buf, format=format)
    buf.seek(0)
    
    # Prepare the headers for file download
    filename = f"resized_image.{format.lower()}"
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    
    # Create a StreamingResponse with the buffer and headers for download
    return StreamingResponse(buf, media_type=f"image/{format.lower()}", headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
