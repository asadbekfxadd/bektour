"""
ImageKit.io integration for BekTour
Handles all file uploads - properties, tours, media, profiles
"""
import os

def get_imagekit():
    from imagekitio import ImageKit
    return ImageKit(
        public_key=os.environ.get('IMAGEKIT_PUBLIC_KEY', ''),
        private_key=os.environ.get('IMAGEKIT_PRIVATE_KEY', ''),
        url_endpoint=os.environ.get('IMAGEKIT_URL_ENDPOINT', '')
    )

def upload_file(file_obj, filename, folder='/bektour'):
    """Upload a file, return (url, file_id) or (None, None)."""
    try:
        from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
        ik = get_imagekit()
        file_bytes = file_obj.read()
        options = UploadFileRequestOptions(
            folder=folder,
            use_unique_file_name=True,
            is_private_file=False,
        )
        result = ik.upload_file(file=file_bytes, file_name=filename, options=options)
        return result.url, result.file_id
    except Exception as e:
        print(f"ImageKit upload error: {e}")
        return None, None

def delete_file(file_id):
    """Delete a file from ImageKit by file_id."""
    try:
        ik = get_imagekit()
        ik.delete_file(file_id)
        return True
    except Exception as e:
        print(f"ImageKit delete error: {e}")
        return False

def optimized_url(url, width=800, height=600, quality=80):
    """Return WebP-optimized URL with resize params."""
    if not url or 'imagekit.io' not in url:
        return url
    return f"{url}?tr=w-{width},h-{height},q-{quality},f-webp"
