import cloudinary
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError
from fastapi import HTTPException
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

# Connects to cloudinary to upload a photo and handles any errors
async def upload_image(file) -> str:
    try:
        result = cloudinary.uploader.upload(file)
        return result["secure_url"]
    except CloudinaryError as e:
        raise HTTPException(status_code=502, detail=f"Cloudinary upload failed: {e}")
    except KeyError:
        raise HTTPException(status_code=502, detail="Upload succeeded but response was malformed")