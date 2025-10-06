from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Any, Union
import re

app = FastAPI()

class DataRequest(BaseModel):
    data: List[Any]

class DataResponse(BaseModel):
    is_success: bool
    user_id: str
    email: EmailStr
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str

def process_array(data):
    even = []
    odd = []
    alphabets = []
    specials = []
    nums = []
    
    # Regex for alphabet check (allowing letter strings)
    alpha_re = re.compile(r"^[a-zA-Z]+$")

    for item in data:
        item_str = str(item)
        if item_str.isdigit():
            val = int(item_str)
            if val % 2 == 0:
                even.append(item_str)
            else:
                odd.append(item_str)
            nums.append(val)
        elif alpha_re.match(item_str):
            alphabets.append(item_str.upper())
        elif not item_str.isalnum():
            specials.append(item_str)

    sum_nums = str(sum(nums))
    concat_alpha = [ch for elem in data if alpha_re.match(str(elem)) for ch in str(elem)]
    rev_concat = ''.join(concat_alpha)[::-1]
    alt_caps = ''.join(ch.upper() if i % 2 == 0 else ch.lower() for i, ch in enumerate(rev_concat))

    return even, odd, alphabets, specials, sum_nums, alt_caps


@app.post("/bfhl", response_model=DataResponse)
async def bfhl_api(request: DataRequest):
    try:
        user_fullname = "RAJ"  
        user_dob = "06102006"            
        email = "abc@email.com"         
        roll_number = "12345678"          
        
        even, odd, alphabets, specials, sum_nums, alt_caps = process_array(request.data)
        return {
            "is_success": True,
            "user_id": f"{user_fullname}{user_dob}",
            "email": email,
            "roll_number": roll_number,
            "odd_numbers": odd,
            "even_numbers": even,
            "alphabets": alphabets,
            "special_characters": specials,
            "sum": sum_nums,
            "concat_string": alt_caps
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Error: {exc}")

# To run locally:
# uvicorn main:app --reload

# When deploying, follow the platform's FastAPI deployment guidance.
