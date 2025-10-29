# Simple PDF Editor Webapp

A simple, deployable web application for basic PDF operations: **merge, split, delete, and rotate pages**. Built with Python (Flask) and PyPDF2, and ready for Docker deployment.

## Features

- **Merge PDFs:** Combine multiple PDFs into one.
- **Split PDF:** Split a PDF into separate pages (demo returns first page; can be extended).
- **Delete Pages:** Remove selected pages from a PDF.
- **Rotate Pages:** Rotate selected pages by 90°, 180°, or 270°.

## Quick Start (Locally)

1. **Clone the repository:**
    ```sh
    git clone <repo-url>
    cd pdf-editor-webapp
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the app:**
    ```sh
    python app.py
    ```
    The app will be available at [http://localhost:5000](http://localhost:5000)

## Docker Deployment

1. **Build the Docker image:**
    ```sh
    docker build -t pdf-editor .
    ```

2. **Run the Docker container:**
    ```sh
    docker run -d -p 5000:5000 pdf-editor
    ```
    Access the webapp at [http://localhost:5000](http://localhost:5000)

## Project Structure

```
pdf_editor_webapp/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css        # (optional)
├── requirements.txt
├── Dockerfile
└── README.md
```

## Notes

- **File Handling:** All processing is done in-memory; no files are stored on the server.
- **Split Feature:** For demo, only the first page is returned (can be modified to return all pages as a ZIP).
- **Security:** No authentication; open to all users by default.
- **Customization:** UI can be easily extended or themed via `templates/index.html` and `static/style.css`.

## Dependencies

- [Flask](https://flask.palletsprojects.com/)
- [PyPDF2](https://pypdf2.readthedocs.io/)

## License

This project is licensed under the MIT License.
