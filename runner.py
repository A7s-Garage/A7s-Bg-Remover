import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import os

st.set_page_config(page_title="A7's Background Remover", page_icon="🖼️", layout="wide")

st.write("## A7's Image Background Remover")

st.write(
    "Welcome to A7's Background Remover, **No need to pay**, **No need to download in Lower quality**, **No size limit** , Enjoy Pandagow !"
)

def convert_image(img, format_type):
    buf = BytesIO()

    if format_type == "JPEG" and img.mode == "RGBA":
        img = img.convert("RGBA")
        img_with_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img_with_bg.paste(img, (0, 0), img)
        img = img_with_bg.convert("RGB")

    img.save(buf, format=format_type)
    byte_im = buf.getvalue()
    return byte_im

def fix_image(upload):
    try:
        image = Image.open(upload)
        col1.write("Original Image 🖼️")
        col1.image(image, use_container_width=True)

        with st.spinner("Removing background..."):
            fixed = remove(image)
        
        col2.write("Background Removed Image :wrench:")
        col2.image(fixed, use_container_width=True)
        
        return fixed
    except Exception as e:
        st.error(f"Error during background removal: {e}")
        return None

col1, col2 = st.columns(2)

supported_formats = ["png", "jpg", "jpeg", "bmp", "webp"]

my_upload = st.file_uploader("Upload an image", type=supported_formats)

processed_image = None

if my_upload is not None:
    file_ext = my_upload.name.split('.')[-1].lower()
    if file_ext not in supported_formats:
        st.error("Please upload a valid image file (e.g., PNG, JPG, JPEG, BMP, TIFF).")
    else:
        processed_image = fix_image(upload=my_upload)

        original_file_name = os.path.splitext(my_upload.name)[0]

        col3, col4 = st.columns([2, 2])

        with col3:
            if processed_image:
                st.download_button(
                    label="Download Background Removed Image as PNG",
                    data=convert_image(processed_image, "PNG"),
                    file_name=f"{original_file_name}_background_removed.png",
                    mime="image/png"
                )

        with col4:
            if processed_image:
                st.download_button(
                    label="Download Background Removed Image as TIFF",
                    data=convert_image(processed_image, "TIFF"),
                    file_name=f"{original_file_name}_background_removed.tiff",
                    mime="image/tiff"
                )

else:
    st.warning("Please upload an image to remove the background!")

st.write("\n\n")

st.write("Having problems viewing images in different formats? Use **A7's Image Viewer** that supports **25+** image formats: [A7's Image Viewer](https://a7s-image-viewer.streamlit.app/)")
st.write("---")
st.write("Made by **A7 Nostalgic** under **A7's Garage**\n\nFor any bugs or suggestions, feel free to reach out at: [a7sgarage@gmail.com](mailto:a7sgarage@gmail.com) or [patnamkannabhiram@gmail.com](mailto:patnamkannabhiram@gmail.com)")

