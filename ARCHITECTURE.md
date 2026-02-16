# ResumeUnmark Architecture

## System Overview

```mermaid
graph TB
    User[User] --> CLI[CLI Interface]
    User --> WebUI[Web UI]
    User --> API[Python API]

    CLI --> Cleaner[PDF Cleaner]
    API --> Cleaner
    WebUI --> Browser[Browser Processing]

    Cleaner --> Detector[Edge Text Detector]
    Cleaner --> Config[Configuration]
    Cleaner --> Utils[File Utils]

    Detector --> PyMuPDF[PyMuPDF Library]
    Cleaner --> PyMuPDF

    PyMuPDF --> Output[Clean PDF Files]
```

## Module Dependencies

```mermaid
graph LR
    CLI[cli.main] --> Core[core.cleaner]
    CLI --> Utils[utils.file_utils]

    Core --> Detector[core.detector]
    Core --> Config[core.config]

    Detector --> Config

    Tests[tests/*] --> Core
    Tests --> Detector
    Tests --> Utils
```

## Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant CLI as CLI Main
    participant Utils as File Utils
    participant Cleaner as PDF Cleaner
    participant Detector as Edge Detector
    participant PDF as PDF Output

    U->>CLI: Run with file path
    CLI->>Utils: Find PDF files
    Utils-->>CLI: List of PDF paths

    loop For each PDF
        CLI->>Cleaner: clean_file(path)
        Cleaner->>Cleaner: Open PDF
        Cleaner->>Detector: find_watermark_rects(page)
        Detector-->>Cleaner: Rectangle coordinates
        Cleaner->>Cleaner: Add redaction annotations
        Cleaner->>Cleaner: Apply redactions
        Cleaner->>PDF: Save cleaned PDF
        PDF-->>Cleaner: Success
        Cleaner-->>CLI: Output path
    end

    CLI->>U: Display summary
```

## Class Diagram

```mermaid
classDiagram
    class PDFCleaner {
        -remove_width: int
        -remove_height: int
        -enable_edge_detection: bool
        -detector: EdgeTextDetector
        +clean_file(path: str) str
        +clean_files(paths: list) list
    }

    class EdgeTextDetector {
        -max_chars: int
        -padding: float
        +find_watermark_rects(page) list
        -_clamp_rect_to_page(rect, page_rect) Rect
    }

    class FileUtils {
        +find_pdf_files(path: str) list
        +get_file_size_mb(path: str) float
        +normalize_path(path: str) str
    }

    PDFCleaner --> EdgeTextDetector : uses
    PDFCleaner --> FileUtils : uses
```

## Package Structure

```
src/
├── __init__.py                 # Package entry point
│   └── Exports: PDFCleaner, EdgeTextDetector, main
│
├── core/                       # Core watermark removal
│   ├── __init__.py
│   ├── cleaner.py             # PDFCleaner class
│   ├── detector.py            # EdgeTextDetector class
│   └── config.py              # Configuration constants
│
├── cli/                        # Command-line interface
│   ├── __init__.py
│   └── main.py                # CLI entry point
│
└── utils/                      # Utilities
    ├── __init__.py
    └── file_utils.py           # File operations
```

## Configuration Flow

```mermaid
graph TD
    Config[core.config] --> Defaults[Default Values]

    User1[CLI User] --> Override1[CLI Arguments]
    User2[API User] --> Override2[Constructor Args]

    Override1 --> Cleaner[PDFCleaner Instance]
    Override2 --> Cleaner
    Defaults --> Cleaner

    Cleaner --> Processing[PDF Processing]
```

## Build & Release Pipeline

```mermaid
graph LR
    Dev[Developer] --> Commit[Git Commit]
    Commit --> Push[Push to GitHub]

    Push --> Tests[Run Tests]
    Tests --> |Pass| Tag[Create Tag]
    Tests --> |Fail| Fix[Fix & Retry]

    Tag --> Build[Build Executable]
    Build --> Release[GitHub Release]
    Release --> Download[User Downloads]
```

## Testing Strategy

```mermaid
graph TB
    Code[Source Code] --> Unit[Unit Tests]
    Code --> Integration[Integration Tests]

    Unit --> Coverage[Coverage Report]
    Integration --> Coverage

    Coverage --> CI[CI Pipeline]
    CI --> |Pass| Deploy[Deploy/Release]
    CI --> |Fail| Notify[Notify Developer]
```

## User Interaction Models

### Desktop App

```
User → Drag & Drop → .exe → PDFCleaner → Output PDF
```

### Web UI

```
User → Upload → Browser Processing → Download Clean PDF
```

### Python API

```python
from src.core import PDFCleaner

cleaner = PDFCleaner()
cleaner.clean_file("document.pdf")
```

### CLI

```bash
python -m src.cli.main "document.pdf"
```

## Architecture Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Open/Closed Principle**: Open for extension, closed for modification
3. **Dependency Injection**: Configuration passed via constructor
4. **DRY (Don't Repeat Yourself)**: Shared logic in utils
5. **Testability**: All components can be tested independently

## Extension Points

- **New Detection Algorithms**: Add to `core.detector`
- **New Output Formats**: Extend `core.cleaner`
- **New Interfaces**: Add to `src/` (e.g., GUI)
- **Custom Configurations**: Modify `core.config`
