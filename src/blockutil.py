from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "u_list"
    ORDERED_LIST = "o_list"
  
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    res = []
    for block in blocks:
        block = block.strip()
        if block:
            res.append(block)
    return res

def block_to_block_type(block):
    # Check for heading
    if block[0] == "#":
        space = block.find(" ")
        if space > 0 and space <= 6:
            if block.startswith("#" * space):
                return BlockType.HEADING
            
    # Check for code
    elif block.startswith("```"):
        if block.endswith("```"):
            return BlockType.CODE
        
    # Check for quote
    elif block[0] == ">":
        lines = block.split("\n")
        all_ok = True
        for line in lines:
            if line[0] != ">":
                all_ok = False
                break
        if all_ok:
            return BlockType.QUOTE
        
    # Check for unordered list
    elif block.startswith("* ") or block.startswith("- "):
        lines = block.split("\n")
        all_ok = True
        for line in lines:
            if line.startswith("* ") or line.startswith("- "):
                continue
            else:
                all_ok = False
                break
        if all_ok:
            return BlockType.UNORDERED_LIST
        
    # Check for ordered list
    elif block.startswith("1. "):
        lines = block.split("\n")
        all_ok = True
        for index in range(len(lines)):
            if not lines[index].startswith(f"{index + 1}. "):
                all_ok = False
                break
        if all_ok:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH