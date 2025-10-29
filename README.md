# Bulk Image Downloader from Excel

A Streamlit web application that allows you to download multiple images from URLs listed in an Excel file. Perfect for bulk downloading product images, media assets, or any collection of images from a spreadsheet.

## Features

- Upload Excel files (.xlsx, .xls) containing image URLs
- Select which column contains the URLs
- Choose specific row ranges to download
- Real-time progress tracking
- Automatic file type detection
- Error handling with detailed reports
- Download all images as a single ZIP file
- Support for multiple image formats (JPG, PNG, GIF, WebP, BMP, TIFF, SVG)

## Demo

You can try the live demo on Streamlit Cloud: [Coming Soon]

## Local Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/SEOptimize-LLC/bulk-image-downloader-from-an-excel-file.git
cd bulk-image-downloader-from-an-excel-file
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## Usage

1. **Prepare Your Excel File**
   - Create an Excel file with at least one column containing image URLs
   - Example format:
     ```
     | Product Name | Image URL                          | Price |
     |--------------|-----------------------------------|-------|
     | Product 1    | https://example.com/image1.jpg    | $10   |
     | Product 2    | https://example.com/image2.png    | $20   |
     ```

2. **Upload and Configure**
   - Upload your Excel file using the file uploader
   - Preview your data to verify it loaded correctly
   - Select the column that contains image URLs
   - (Optional) Set row range and timeout settings

3. **Download Images**
   - Click the "Download All Images" button
   - Wait for the download process to complete
   - Review the download summary and any errors
   - Download the ZIP file containing all successfully downloaded images

## Excel File Format

Your Excel file should contain:
- At least one column with valid image URLs
- URLs should be complete (including `http://` or `https://`)
- Supported URL formats:
  - Direct image links (e.g., `https://example.com/image.jpg`)
  - CDN links
  - Any publicly accessible image URL

## Configuration Options

- **Start/End Row**: Select specific rows to download (useful for testing or partial downloads)
- **Request Timeout**: Set maximum wait time for each image download (5-60 seconds)

## Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- WebP
- BMP
- TIFF
- SVG

## Error Handling

The application includes comprehensive error handling:
- Invalid URLs are skipped with error messages
- Network timeouts are caught and reported
- Invalid image data is detected and logged
- Detailed error report shows which downloads failed and why

## Deployment to Streamlit Cloud

### Prerequisites
- A GitHub account
- A Streamlit Cloud account (free at [streamlit.io/cloud](https://streamlit.io/cloud))

### Steps

1. **Push to GitHub**
   - Ensure all files are committed to your repository

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select this repository
   - Set the main file path to `streamlit_app.py`
   - Click "Deploy"

3. **Share Your App**
   - Once deployed, you'll get a public URL
   - Share this URL with anyone who needs to use the app

## Technical Details

### Dependencies

- `streamlit`: Web application framework
- `pandas`: Excel file reading and data manipulation
- `openpyxl`: Excel file support
- `requests`: HTTP library for downloading images
- `Pillow`: Image processing and validation

### File Naming Convention

Downloaded images are named with the format:
```
image_NNNN.ext
```
Where:
- `NNNN` is the row number (zero-padded)
- `.ext` is the detected file extension

### Rate Limiting

The application downloads images sequentially to avoid overwhelming servers. For very large batches, consider:
- Breaking into smaller chunks
- Adjusting timeout settings
- Being mindful of the source server's rate limits

## Troubleshooting

### Common Issues

**"No URLs found in the selected column"**
- Verify the correct column is selected
- Check that the column contains valid URLs
- Ensure row range includes rows with data

**"Timeout" errors**
- Increase the timeout setting
- Check your internet connection
- Verify the URLs are accessible

**"Invalid image data" errors**
- The URL might not point to a valid image file
- The server might be blocking automated downloads
- The image file might be corrupted

**Images won't download**
- Ensure URLs are publicly accessible (not behind authentication)
- Check if the server requires specific headers
- Verify URLs are complete and valid

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review error messages in the download report
3. Create an issue on GitHub with details about your problem

## Future Enhancements

Potential features for future versions:
- Custom file naming patterns
- Image resizing/optimization options
- Support for CSV files
- Batch processing with rate limiting
- Resume failed downloads
- Download history tracking
- Multiple URL columns support

---

Made with Streamlit
