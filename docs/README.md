# Web UI

This folder contains the **browser-based interface** for ResumeUnmark.

## What's Inside

- **index.html** - Main web interface
- **app.js** - Client-side PDF processing logic
- **style.css** - Styling and animations
- **.nojekyll** - GitHub Pages configuration

## Live Demo

🌐 **https://patrickzs.github.io/ResumeUnmark/**

## Why "docs/"?

This folder is named `docs/` (instead of `web-ui/` or `public/`) because GitHub Pages automatically serves static sites from a folder named `docs/`. This is a GitHub-specific convention that allows zero-configuration deployment.

## Technology Stack

- **PDF Processing**: pdf-lib + pdf.js (browser-based)
- **Styling**: Vanilla CSS with modern animations
- **Deployment**: GitHub Pages (static hosting)

## Local Development

To test the web UI locally:

```bash
# Option 1: Python
python -m http.server 8000
# Then visit: http://localhost:8000/docs/

# Option 2: Node.js
npx serve docs/
```

## Note

This is **separate** from the desktop application (`src/`). The web UI uses JavaScript libraries (pdf-lib, pdf.js) while the desktop app uses Python (PyMuPDF).
