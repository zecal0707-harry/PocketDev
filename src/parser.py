import re
from typing import Optional, Dict, Any

def parse_comment(comment_body: str) -> Optional[Dict[str, Any]]:
    if not comment_body:
        return None
        
    match = re.search(r'(?m)^/oc\s*(.*)', comment_body, re.DOTALL)
    if not match:
        return None
        
    raw_instruction = match.group(1).strip()
    
    model = "gemini"
    instruction = raw_instruction
    
    flag_match = re.search(r'--model\s+(\w+)', raw_instruction)
    if flag_match:
        model = flag_match.group(1)
        instruction = re.sub(r'--model\s+\w+', '', raw_instruction).strip()
        
    if not instruction:
        return None
        
    return {
        "instruction": instruction,
        "model": model
    }
