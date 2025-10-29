import streamlit as st
import pandas as pd
import requests
from pathlib import Path
import io
import zipfile
from PIL import Image
from urllib.parse import urlparse
import time

st.set_page_config(
    page_title="Bulk Image Downloader",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Bulk Image Downloader from Excel")
st.markdown("Upload an Excel file with image URLs and download all images as a ZIP file.")

def get_file_extension(url, content_type=None):
    """Determine file extension from URL or content type."""
    # Try to get extension from URL
    parsed_url = urlparse(url)
    path = parsed_url.path
    if path:
        ext = Path(path).suffix
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg']:
            return ext

    # Try to determine from content type
    if content_type:
        content_type = content_type.lower()
        if 'jpeg' in content_type or 'jpg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'webp' in content_type:
            return '.webp'
        elif 'bmp' in content_type:
            return '.bmp'
        elif 'tiff' in content_type:
            return '.tiff'
        elif 'svg' in content_type:
            return '.svg'

    # Default to .jpg
    return '.jpg'

def download_image(url, timeout=30):
    """Download a single image from URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=timeout, headers=headers, stream=True)
        response.raise_for_status()

        # Get content type
        content_type = response.headers.get('Content-Type', '')

        # Verify it's an image
        if not content_type.startswith('image/'):
            return None, f"Not an image (content-type: {content_type})"

        # Get image content
        image_data = response.content

        # Try to open with PIL to verify it's a valid image
        try:
            img = Image.open(io.BytesIO(image_data))
            img.verify()
            return image_data, None
        except Exception as e:
            return None, f"Invalid image data: {str(e)}"

    except requests.exceptions.Timeout:
        return None, "Timeout"
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def create_download_report(results):
    """Create a summary report of the download process."""
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    failed = total - successful

    report = f"""
### Download Summary
- **Total URLs**: {total}
- **Successfully Downloaded**: {successful}
- **Failed**: {failed}
- **Success Rate**: {(successful/total*100):.1f}%
"""

    if failed > 0:
        report += "\n### Failed Downloads:\n"
        for result in results:
            if not result['success']:
                report += f"- Row {result['row']}: {result['url'][:50]}... - {result['error']}\n"

    return report

# File uploader
uploaded_file = st.file_uploader(
    "Choose an Excel file (.xlsx or .xls)",
    type=['xlsx', 'xls'],
    help="Upload an Excel file containing image URLs"
)

if uploaded_file is not None:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)

        st.success(f"✅ File loaded successfully! Found {len(df)} rows and {len(df.columns)} columns.")

        # Show preview
        with st.expander("📊 Preview Data (first 5 rows)", expanded=True):
            st.dataframe(df.head())

        # Column selection
        st.subheader("🔍 Select URL Column")
        url_column = st.selectbox(
            "Which column contains the image URLs?",
            options=df.columns.tolist(),
            help="Select the column that contains the image URLs"
        )

        # Additional options
        col1, col2 = st.columns(2)
        with col1:
            start_row = st.number_input(
                "Start from row (1-based)",
                min_value=1,
                max_value=len(df),
                value=1,
                help="Start downloading from this row number"
            )
        with col2:
            end_row = st.number_input(
                "End at row (1-based)",
                min_value=start_row,
                max_value=len(df),
                value=len(df),
                help="Stop downloading at this row number"
            )

        timeout_setting = st.slider(
            "Request timeout (seconds)",
            min_value=5,
            max_value=60,
            value=30,
            help="Maximum time to wait for each image download"
        )

        # Download button
        if st.button("🚀 Download All Images", type="primary"):
            # Filter dataframe based on row selection
            df_filtered = df.iloc[start_row-1:end_row].copy()
            df_filtered = df_filtered.reset_index(drop=True)

            # Get URLs
            urls = df_filtered[url_column].dropna().tolist()

            if len(urls) == 0:
                st.error("❌ No URLs found in the selected column and row range!")
            else:
                st.info(f"🔄 Processing {len(urls)} URLs...")

                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Results storage
                results = []
                downloaded_images = []

                # Download images
                for idx, url in enumerate(urls):
                    # Update progress
                    progress = (idx + 1) / len(urls)
                    progress_bar.progress(progress)
                    status_text.text(f"Downloading {idx + 1}/{len(urls)}: {url[:50]}...")

                    # Skip empty or invalid URLs
                    if not isinstance(url, str) or url.strip() == '':
                        results.append({
                            'row': start_row + idx,
                            'url': url,
                            'success': False,
                            'error': 'Empty or invalid URL'
                        })
                        continue

                    # Download image
                    image_data, error = download_image(url.strip(), timeout=timeout_setting)

                    if image_data:
                        # Determine file extension
                        ext = get_file_extension(url)
                        filename = f"image_{start_row + idx:04d}{ext}"

                        downloaded_images.append({
                            'filename': filename,
                            'data': image_data
                        })

                        results.append({
                            'row': start_row + idx,
                            'url': url,
                            'success': True,
                            'error': None
                        })
                    else:
                        results.append({
                            'row': start_row + idx,
                            'url': url,
                            'success': False,
                            'error': error
                        })

                progress_bar.progress(1.0)
                status_text.text("✅ Download complete!")

                # Show results
                st.markdown(create_download_report(results))

                # Create ZIP file if we have images
                if downloaded_images:
                    st.subheader("📦 Download Images")

                    # Create ZIP in memory
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for img in downloaded_images:
                            zip_file.writestr(img['filename'], img['data'])

                    zip_buffer.seek(0)

                    # Download button for ZIP
                    st.download_button(
                        label=f"⬇️ Download {len(downloaded_images)} Images (ZIP)",
                        data=zip_buffer,
                        file_name=f"downloaded_images_{time.strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip"
                    )

                    st.success(f"✅ Successfully downloaded {len(downloaded_images)} images!")
                else:
                    st.error("❌ No images were successfully downloaded.")

    except Exception as e:
        st.error(f"❌ Error reading Excel file: {str(e)}")
        st.exception(e)

else:
    # Instructions when no file is uploaded
    st.info("""
    ### 📝 Instructions:

    1. **Prepare your Excel file** with a column containing image URLs
    2. **Upload the file** using the file uploader above
    3. **Select the column** that contains the URLs
    4. **Configure options** (optional):
       - Choose which rows to download
       - Set timeout for downloads
    5. **Click 'Download All Images'** to start the process
    6. **Download the ZIP file** containing all images

    ### 📋 Excel File Format:

    Your Excel file should have at least one column with image URLs. For example:

    | Product Name | Image URL | Price |
    |--------------|-----------|-------|
    | Product 1 | https://example.com/image1.jpg | $10 |
    | Product 2 | https://example.com/image2.png | $20 |

    The app will automatically detect the file type and download images accordingly.

    ### ⚙️ Supported Image Formats:
    - JPG/JPEG
    - PNG
    - GIF
    - WebP
    - BMP
    - TIFF
    - SVG
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | For issues or suggestions, please create an issue on GitHub")
