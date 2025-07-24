import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import fitz
import re
import logging
from typing import Optional
from app.schemas.aadhaar import AadhaarDataCreate

logger = logging.getLogger(__name__)

def extract_text_from_image(image: Image.Image) -> str:
    """Extract text from PIL Image using OCR"""
    try:
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config, lang='eng+tam')
        logger.info("Successfully extracted text from image")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from image: {str(e)}")
        raise

def extract_text_from_pdf(pdf_bytes: bytes, password: Optional[str] = None) -> str:
    """Extract text from PDF bytes using PyMuPDF"""
    try:
        text = ""
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Handle password-protected PDFs
        if doc.needs_pass:
            if password:
                if not doc.authenticate(password):
                    raise ValueError("Invalid password for PDF")
            else:
                raise ValueError("PDF is password protected but no password provided")
        
        # Extract text from all pages
        for page in doc:
            text += page.get_text("text")
        
        doc.close()
        logger.info("Successfully extracted text from PDF")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def extract_name_from_text(lines):
    """Extract name from text lines with filtering"""
    unwanted_phrases = [
        "Digitally signed by DS Unique",
        "Identification Authority of India",
        "Government of India",
        "Signature Not Verified",
        "Date of Issue",
        "Download Date"
    ]

    for line in lines:
        clean_line = line.strip()
        # Allow common characters in names (alphabets, spaces, apostrophes, hyphens)
        if (
            re.match(r'^[A-Za-z\s\'-]+$', clean_line)
            and len(clean_line.split()) > 1
            and all(phrase.lower() not in clean_line.lower() for phrase in unwanted_phrases)
        ):
            # Split on guardian prefixes (S/O, C/O, etc.) and take the first part
            name_part = re.split(r'\s*(?:S/O|C/O|W/O|D/O)\s*', clean_line, flags=re.IGNORECASE)[0]
            # Remove trailing single letters (C, W, S, D) followed by whitespace
            name_part = re.sub(r'\s+[CWSD]\s*$', '', name_part).strip()
            # Clean any extra spaces
            name_part = re.sub(r'\s+', ' ', name_part)
            if len(name_part) > 2:  # Ensure name is meaningful
                return name_part
    return ""

def parse_aadhaar_details(text: str) -> AadhaarDataCreate:
    """Parse Aadhaar details from extracted text"""
    try:
        data = AadhaarDataCreate(
            aadhaar_number="",
            name=""
        )
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Extract Aadhaar Number
        aadhaar_match = re.search(r'\b(\d{4}\s\d{4}\s\d{4})\b', text)
        if aadhaar_match:
            data.aadhaar_number = aadhaar_match.group(1)
        
        # Extract VID (Virtual ID)
        vid_match = re.search(r'VID[:\s]*(\d{4}\s\d{4}\s\d{4}\s\d{4})', text)
        if vid_match:
            data.vid = vid_match.group(1)

        # Extract Name (Tamil and English)
        tamil_name_match = re.search(r'([\u0B80-\u0BFF\s]+)\n([A-Za-z\s\'-]+)', text)
        if tamil_name_match:
            data.name_tamil = tamil_name_match.group(1).strip()
            data.name = tamil_name_match.group(2).strip().replace("\n", " ")
            # Process to remove guardian prefixes and trailing letters
            data.name = re.split(r'\s*(?:S/O|C/O|W/O|D/O)\s*', data.name, flags=re.IGNORECASE)[0].strip()
            data.name = re.sub(r'\s+[CWSD]\s*$', '', data.name).strip()
            data.name = re.sub(r'\s+', ' ', data.name)
        
        # **Backup:** If English name is still missing, find the first proper English name
        if not data.name:
            data.name = extract_name_from_text(lines)

        # Extract Guardian Name (S/O, W/O, C/O, D/O)
        guardian_match = re.search(r'(S/o|C/o|D/o|W/o)[.:]?\s*([A-Za-z\s\'-]+)', text, re.IGNORECASE)
        if guardian_match:
            data.guardian_name = guardian_match.group(2).strip()

        # Extract DOB
        dob_match = re.search(r'(DOB|Date of Birth|D\.O\.B)[:\s]*?(\d{1,2}[-/]\d{1,2}[-/]\d{4})', text, re.IGNORECASE)
        if dob_match:
            data.dob = dob_match.group(2).replace('-', '/')

        # Extract Gender
        gender_match = re.search(r'\b(Male|Female|Transgender|M|F|T)\b', text, re.IGNORECASE)
        if gender_match:
            gender = gender_match.group(1).capitalize()
            if gender in ['M']:
                data.gender = 'Male'
            elif gender in ['F']:
                data.gender = 'Female'
            elif gender in ['T']:
                data.gender = 'Transgender'
            else:
                data.gender = gender

        # Extract Address
        address_match = re.search(r'(?i)address[:\s]*(.*?)(?=\nDistrict|\nState|\n\d{6}|\nVID|\nDigitally|$)', text, re.DOTALL)
        if address_match:
            address_text = re.sub(r'(S/o|C/o|D/o|W/o)[.:]?\s*[A-Za-z\s\'-]+', '', address_match.group(1).strip(), flags=re.IGNORECASE)
            address_text = re.sub(r'\b\d{4}\s\d{4}\s\d{4}\b', '', address_text)
            address_text = re.sub(r'PO:.*?,', '', address_text)
            address_text = re.sub(r'(?i)\b(dist|state)\b.*', '', address_text)
            address_text = re.sub(r'\n+', ' ', address_text).strip()
            address_text = re.sub(r'\s+', ' ', address_text).strip()
            data.address = address_text.lstrip(',').strip()

        # Extract VTC (Village/Town/City)
        vtc_match = re.search(r'VTC[:\s]*(.*)', text, re.IGNORECASE)
        if vtc_match:
            data.vtc = vtc_match.group(1).strip()
        
        # Extract PO (Post Office)
        po_match = re.search(r'PO[:\s]*(.*)', text, re.IGNORECASE)
        if po_match:
            data.po = po_match.group(1).strip()
        
        # Extract Sub District
        sub_district_match = re.search(r'Sub District[:\s]*(.*)', text, re.IGNORECASE)
        if sub_district_match:
            data.sub_district = sub_district_match.group(1).strip()

        # Extract District
        district_match = re.search(r'District[:\s]*(.*)', text, re.IGNORECASE)
        if district_match:
            data.district = district_match.group(1).strip().replace(',', '')
        
        # Extract State
        state_match = re.search(r'State[:\s]*(.*)', text, re.IGNORECASE)
        if state_match:
            data.state = state_match.group(1).strip()

        # Extract Pincode
        pincode_match = re.search(r'\b(\d{6})\b', text)
        if pincode_match:
            data.pincode = pincode_match.group(1)

        # Extract Phone Number
        phone_match = re.search(r'\b(\d{10})\b', text)
        if phone_match:
            data.phone = phone_match.group(1)

        logger.info(f"Successfully parsed Aadhaar details for: {data.aadhaar_number}")
        return data
    
    except Exception as e:
        logger.error(f"Error parsing Aadhaar details: {str(e)}")
        raise

async def process_aadhaar_file(file_content: bytes, filename: str, password: Optional[str] = None) -> AadhaarDataCreate:
    """Process uploaded file and extract Aadhaar details"""
    try:
        # Determine file type and extract text
        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_content, password)
        else:
            # Assume it's an image
            image = Image.open(io.BytesIO(file_content))
            text = extract_text_from_image(image)
        
        # Parse the extracted text
        aadhaar_data = parse_aadhaar_details(text)
        
        # Validate that we have minimum required data
        if not aadhaar_data.aadhaar_number:
            raise ValueError("Could not extract Aadhaar number from the document")
        
        if not aadhaar_data.name:
            raise ValueError("Could not extract name from the document")
        
        return aadhaar_data
    
    except Exception as e:
        logger.error(f"Error processing Aadhaar file: {str(e)}")
        raise
