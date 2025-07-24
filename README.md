# Aadhaar OCR API

A complete full-stack web application that allows users to upload Aadhaar PDF or image files, extract details using OCR, and store them in a Supabase PostgreSQL database.

## Features

- 📄 **File Upload**: Support for PDF and image files (JPG, PNG, etc.)
- 🔍 **OCR Processing**: Extract Aadhaar details using advanced OCR technology
- 🗄️ **Database Storage**: Store extracted data in Supabase PostgreSQL
- 🔍 **Data Retrieval**: Fetch Aadhaar data by Aadhaar number
- 📚 **API Documentation**: Interactive Swagger/OpenAPI docs
- 🌐 **Web Interface**: Simple frontend for testing uploads
- 🐳 **Docker Support**: Containerized deployment

## Technologies Used

- **Backend**: Python (FastAPI)
- **Database**: Supabase (PostgreSQL)
- **OCR**: pytesseract, pdf2image, PyMuPDF
- **ORM**: SQLAlchemy + Supabase client
- **Frontend**: HTML/CSS/JavaScript
- **Documentation**: Swagger/OpenAPI

## Quick Start

### Prerequisites

- Python 3.8+
- Tesseract OCR installed
- Supabase account and project

### Automated Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "API Project"
```

2. Run the setup script:
```bash
python setup.py
```

3. Update `.env` with your Supabase credentials:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-role-key
```

4. Set up the database:
```bash
python run.py db-setup
```
Copy and run the SQL commands in your Supabase SQL editor.

5. Start the application:
```bash
python run.py dev
```

### Manual Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

### Access Points

- **Web Interface**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

## API Endpoints

### POST /form/submit
Upload and process Aadhaar document
- **Input**: File (PDF/Image) + optional password
- **Output**: Extracted Aadhaar data

### GET /form/{aadhaar_number}
Retrieve stored Aadhaar data
- **Input**: Aadhaar number (path parameter)
- **Output**: Stored Aadhaar details

## Project Structure

```
API Project/
├── app/
│   ├── core/           # Core configuration
│   ├── crud/           # Database operations
│   ├── models/         # SQLAlchemy models
│   ├── routers/        # API routes
│   ├── schemas/        # Pydantic schemas
│   ├── main.py         # FastAPI application
│   └── ocr_parser.py   # OCR processing logic
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── Dockerfile          # Docker configuration
└── README.md          # This file
```

## Environment Variables

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-role-key
APP_NAME=Aadhaar OCR API
APP_VERSION=1.0.0
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://127.0.0.1:8000
```

## Running Options

### Development Mode
```bash
python run.py dev
```

### Production Mode
```bash
python run.py prod
```

### Docker Deployment
```bash
# Using the run script
python run.py docker

# Or manually
docker-compose up --build

# Or build manually
docker build -t aadhaar-ocr-api .
docker run -p 8000:8000 aadhaar-ocr-api
```

## Testing

### Using the Web Interface
1. Visit http://127.0.0.1:8000
2. Upload an Aadhaar PDF or image file
3. View extracted data in the results section
4. Search for existing records using Aadhaar number

### Using Postman
1. Import `Aadhaar_OCR_API.postman_collection.json`
2. Set the `base_url` variable to `http://127.0.0.1:8000`
3. Test the endpoints:
   - Health check
   - File upload (PDF/Image)
   - Data retrieval by Aadhaar number
   - List all records

### Using cURL
```bash
# Health check
curl http://127.0.0.1:8000/health

# Upload file
curl -X POST "http://127.0.0.1:8000/api/form/submit" \
  -F "file=@path/to/aadhaar.pdf" \
  -F "password=optional_password"

# Get data by Aadhaar number
curl "http://127.0.0.1:8000/api/form/1234%205678%209012"
```

## Troubleshooting

### Common Issues

1. **Tesseract not found**
   - Install Tesseract OCR for your OS
   - Ensure it's in your system PATH

2. **Supabase connection failed**
   - Check your SUPABASE_URL and SUPABASE_KEY in .env
   - Ensure your Supabase project is active

3. **Database table not found**
   - Run the SQL commands from `python run.py db-setup`
   - Check your Supabase database

4. **OCR extraction failed**
   - Ensure the uploaded file is a valid Aadhaar document
   - Check file format (PDF, JPG, PNG supported)
   - For PDFs, ensure they're not heavily encrypted

### Health Check
```bash
python run.py health
```

## License

MIT License
# API-Project
