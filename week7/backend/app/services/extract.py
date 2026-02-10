import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ExtractedActionItem:
    """Represents an extracted action item with metadata."""
    text: str
    priority: str  # "high", "medium", "low"
    category: str  # "task", "reminder", "decision", "general"
    assignee: Optional[str] = None
    due_date: Optional[str] = None
    context: Optional[str] = None


def extract_action_items(text: str) -> list[str]:
    """
    Extract action items from text with basic pattern recognition.
    Returns a list of action item strings.
    """
    extracted_items = extract_action_items_advanced(text)
    return [item.text for item in extracted_items]


def extract_action_items_advanced(text: str) -> list[ExtractedActionItem]:
    """
    Enhanced action item extraction with sophisticated pattern recognition.
    
    Supports:
    - Multiple action indicators (TODO, ACTION, TASK, etc.)
    - Priority detection (high, medium, low, urgent)
    - Assignee extraction (@username or assigned to [name])
    - Due date detection
    - Contextual categorization
    - Checkbox patterns ([ ], [x])
    - Imperative verbs
    - Separator support: ||| or ;; to split multiple items in one line
    """
    # 先处理分隔符，将一行分成多行
    # 支持 ||| 或 ;; 作为分隔符
    text = text.replace('|||', '\n').replace(';;', '\n')
    
    lines = text.splitlines()
    results: list[ExtractedActionItem] = []
    
    # Action indicators with priority mapping
    action_patterns = {
        r'\b(urgent|asap|critical|important)[\s:]*': 'high',
        r'\b(todo|action|task|must|should|need to|have to)[\s:]*': 'medium',
        r'\b(maybe|consider|could|might want to|nice to have)[\s:]*': 'low',
    }
    
    # Checkbox patterns
    checkbox_pattern = r'^\s*[-*]?\s*\[[ xX]\]\s*(.+)$'
    
    # Assignee patterns
    assignee_patterns = [
        r'@(\w+)',  # @username
        r'assigned to:?\s*(\w+)',  # assigned to: John
        r'\((\w+)\)$',  # (John) at end of line
    ]
    
    # Due date patterns
    due_date_patterns = [
        r'(?:by|due|deadline)[\s:]+(\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)',
        r'(?:by|due|deadline)[\s:]+(\w+\s+\d{1,2}(?:,?\s+\d{4})?)',
    ]
    
    # Imperative verbs that suggest action
    imperative_verbs = [
        'implement', 'create', 'fix', 'update', 'add', 'remove', 'delete',
        'refactor', 'test', 'deploy', 'review', 'merge', 'document', 'write',
        'install', 'configure', 'setup', 'check', 'verify', 'validate',
        'optimize', 'improve', 'enhance', 'investigate', 'research', 'analyze',
        'prepare', 'schedule', 'contact', 'send', 'respond', 'follow up',
        'build', 'compile', 'run', 'execute', 'process', 'handle', 'resolve'
    ]
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
            
        # Remove bullet points and list markers
        cleaned = re.sub(r'^\s*[-*•]\s*', '', stripped)
        normalized = cleaned.lower()
        
        # Track if this line is an action item
        is_action = False
        priority = "medium"
        category = "general"
        assignee = None
        due_date = None
        
        # Check checkbox pattern
        checkbox_match = re.match(checkbox_pattern, stripped)
        if checkbox_match:
            is_action = True
            cleaned = checkbox_match.group(1)
            normalized = cleaned.lower()
            category = "task"
        
        # Check for exclamation mark (emphasis) - check before stripping
        if stripped.endswith("!"):
            is_action = True
            if priority == "medium":  # Don't override if already high
                priority = "high"
            if category == "general":
                category = "reminder"
        
        # Check for explicit action indicators
        for pattern, detected_priority in action_patterns.items():
            if re.search(pattern, normalized):
                is_action = True
                priority = detected_priority
                if 'todo' in normalized or 'task' in normalized:
                    category = "task"
                elif 'action' in normalized:
                    category = "decision"
                break
        
        # Check for imperative verbs at start
        if not is_action:
            first_word = normalized.split()[0] if normalized.split() else ""
            if first_word in imperative_verbs:
                is_action = True
                category = "task"
        
        # Check for question marks that imply decisions
        if "?" in cleaned and any(word in normalized for word in ["should", "need", "must", "can we", "could we", "would we"]):
            is_action = True
            category = "decision"
        
        # Extract assignee
        for pattern in assignee_patterns:
            match = re.search(pattern, cleaned, re.IGNORECASE)
            if match:
                assignee = match.group(1)
                # Clean assignee from the text
                cleaned = re.sub(pattern, '', cleaned, count=1, flags=re.IGNORECASE).strip()
                break
        
        # Extract due date
        for pattern in due_date_patterns:
            match = re.search(pattern, cleaned, re.IGNORECASE)
            if match:
                due_date = match.group(1)
                break
        
        # Add to results if it's an action item
        if is_action:
            # Get context from surrounding lines
            context_lines = []
            if i > 0 and lines[i-1].strip():
                context_lines.append(lines[i-1].strip())
            if i < len(lines) - 1 and lines[i+1].strip():
                context_lines.append(lines[i+1].strip())
            context = " | ".join(context_lines) if context_lines else None
            
            # Clean up the final text - remove any remaining separators
            final_text = cleaned.strip()
            # Remove any remaining ||| or ;; that might be in the middle or end
            final_text = final_text.split('|||')[0].strip()
            final_text = final_text.split(';;')[0].strip()
            
            if final_text:
                results.append(ExtractedActionItem(
                    text=final_text,
                    priority=priority,
                    category=category,
                    assignee=assignee,
                    due_date=due_date,
                    context=context
                ))
    
    return results


def categorize_action_items(items: list[ExtractedActionItem]) -> dict[str, list[ExtractedActionItem]]:
    """Categorize action items by priority or category."""
    categorized = {
        "high_priority": [],
        "medium_priority": [],
        "low_priority": [],
        "by_category": {
            "task": [],
            "reminder": [],
            "decision": [],
            "general": []
        }
    }
    
    for item in items:
        # Categorize by priority
        if item.priority == "high":
            categorized["high_priority"].append(item)
        elif item.priority == "medium":
            categorized["medium_priority"].append(item)
        else:
            categorized["low_priority"].append(item)
        
        # Categorize by type
        categorized["by_category"][item.category].append(item)
    
    return categorized


def filter_action_items_by_assignee(items: list[ExtractedActionItem], assignee: str) -> list[ExtractedActionItem]:
    """Filter action items assigned to a specific person."""
    return [item for item in items if item.assignee and item.assignee.lower() == assignee.lower()]


def get_high_priority_items(items: list[ExtractedActionItem]) -> list[ExtractedActionItem]:
    """Get only high priority action items."""
    return [item for item in items if item.priority == "high"]


