from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from app.core.database import get_database
from app.crud.aadhaar import get_aadhaar_crud
from app.schemas.aadhaar import (
    AadhaarSubmissionResponse, 
    AadhaarRetrievalResponse, 
    ErrorResponse,
    AadhaarData
)
from app.ocr_parser import process_aadhaar_file

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/form", tags=["Aadhaar Forms"])

@router.post("/submit", response_model=AadhaarSubmissionResponse)
async def submit_aadhaar_form(
    file: UploadFile = File(..., description="Aadhaar PDF or image file"),
    password: Optional[str] = Form(None, description="Password for protected PDF files"),
    database = Depends(get_database)
):
    """
    Upload and process Aadhaar document
    
    - **file**: PDF or image file containing Aadhaar details
    - **password**: Optional password for password-protected PDF files
    
    Returns extracted and stored Aadhaar data
    """
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        file_extension = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Process the file and extract Aadhaar details
        logger.info(f"Processing file: {file.filename}")
        aadhaar_data = await process_aadhaar_file(file_content, file.filename, password)
        
        # Get CRUD instance
        crud = get_aadhaar_crud(database)
        
        # Check if Aadhaar number already exists
        existing_record = await crud.get_aadhaar_by_number(aadhaar_data.aadhaar_number)
        
        if existing_record:
            # Update existing record
            updated_record = await crud.update_aadhaar_record(aadhaar_data.aadhaar_number, aadhaar_data)
            if updated_record:
                return AadhaarSubmissionResponse(
                    success=True,
                    message="Aadhaar data updated successfully",
                    data=AadhaarData(**updated_record),
                    aadhaar_number=aadhaar_data.aadhaar_number
                )
        else:
            # Create new record
            created_record = await crud.create_aadhaar_record(aadhaar_data)
            if created_record:
                return AadhaarSubmissionResponse(
                    success=True,
                    message="Aadhaar data submitted successfully",
                    data=AadhaarData(**created_record),
                    aadhaar_number=aadhaar_data.aadhaar_number
                )
        
        # If we reach here, something went wrong
        raise HTTPException(status_code=500, detail="Failed to save Aadhaar data")
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in submit_aadhaar_form: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred while processing the file")

@router.get("/{aadhaar_number}", response_model=AadhaarRetrievalResponse)
async def get_aadhaar_data(
    aadhaar_number: str,
    database = Depends(get_database)
):
    """
    Retrieve Aadhaar data by Aadhaar number
    
    - **aadhaar_number**: The Aadhaar number to search for (format: XXXX XXXX XXXX or XXXXXXXXXXXX)
    
    Returns stored Aadhaar data if found
    """
    try:
        # Normalize Aadhaar number format
        clean_aadhaar = aadhaar_number.replace(" ", "").replace("-", "")
        
        # Validate Aadhaar number format
        if len(clean_aadhaar) != 12 or not clean_aadhaar.isdigit():
            raise HTTPException(
                status_code=400, 
                detail="Invalid Aadhaar number format. Must be 12 digits."
            )
        
        # Format Aadhaar number with spaces
        formatted_aadhaar = f"{clean_aadhaar[:4]} {clean_aadhaar[4:8]} {clean_aadhaar[8:]}"
        
        # Get CRUD instance
        crud = get_aadhaar_crud(database)
        
        # Retrieve data from database
        logger.info(f"Retrieving Aadhaar data for: {formatted_aadhaar}")
        aadhaar_record = await crud.get_aadhaar_by_number(formatted_aadhaar)
        
        if aadhaar_record:
            return AadhaarRetrievalResponse(
                success=True,
                message="Aadhaar data retrieved successfully",
                data=AadhaarData(**aadhaar_record)
            )
        else:
            return AadhaarRetrievalResponse(
                success=False,
                message=f"No Aadhaar data found for number: {formatted_aadhaar}",
                data=None
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_aadhaar_data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred while retrieving data")

@router.get("/", response_model=dict)
async def list_all_aadhaar_records(
    limit: int = 10,
    offset: int = 0,
    database = Depends(get_database)
):
    """
    List all Aadhaar records (for testing purposes)

    - **limit**: Maximum number of records to return (default: 10)
    - **offset**: Number of records to skip (default: 0)
    """
    try:
        crud = get_aadhaar_crud(database)
        result = await crud.list_all_records(limit, offset)

        return {
            "success": True,
            "message": f"Retrieved {len(result['data'])} records",
            "data": result['data'],
            "total_count": result['total_count']
        }

    except Exception as e:
        logger.error(f"Error listing Aadhaar records: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred while listing records")
