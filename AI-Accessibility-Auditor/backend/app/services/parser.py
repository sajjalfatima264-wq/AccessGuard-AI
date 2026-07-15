from bs4 import BeautifulSoup

def parse_html_to_accessibility_data(html_content: str) -> dict:
    """
    Parses raw HTML using BeautifulSoup and extracts structured data
    tailored for accessibility analysis.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Extract Images
    images = []
    for img in soup.find_all('img'):
        # Calculate a rough line location based on string position
        location = str(img).split('\n')[0]
        images.append({
            "src": img.get('src'),
            "alt": img.get('alt'), # Will be None if missing
            "element_snippet": str(img)[:100]
        })

    # 2. Extract Buttons & Interactive Elements
    buttons = []
    for btn in soup.find_all(['button', 'input'], attrs={'type': ['button', 'submit', 'reset']}):
        buttons.append({
            "tag": btn.name,
            "text": btn.get_text(strip=True) or None,
            "aria_label": btn.get('aria-label'),
            "role": btn.get('role'),
            "element_snippet": str(btn)[:100]
        })

    # 3. Extract Forms with Label Connection Logic
    forms = []
    for form in soup.find_all('form'):
        inputs = []
        for inp in form.find_all(['input', 'textarea', 'select']):
            # Check for connection: id -> for, or nested inside <label>
            has_label = False
            label_text = None
            
            if inp.get('id'):
                label_tag = soup.find('label', {'for': inp.get('id')})
                if label_tag:
                    has_label = True
                    label_text = label_tag.get_text(strip=True)
                    
            if not has_label:
                parent_label = inp.find_parent('label')
                if parent_label:
                    has_label = True
                    label_text = parent_label.get_text(strip=True)

            inputs.append({
                "type": inp.get('type', inp.name),
                "name": inp.get('name'),
                "aria_label": inp.get('aria-label'),
                "placeholder": inp.get('placeholder'),
                "has_label": has_label,
                "label_text": label_text,
                "element_snippet": str(inp)[:100]
            })
            
        forms.append({"inputs": inputs})

    # 4. Extract Headings and Check Order
    headings = []
    prev_level = 0
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        level = int(h.name[1])
        # Heading order is incorrect if it skips levels (e.g., h1 straight to h3)
        order_correct = (prev_level == 0) or (level <= prev_level + 1)
        
        headings.append({
            "tag": h.name,
            "text": h.get_text(strip=True)[:50], # Limit text length
            "level": level,
            "order_correct": order_correct,
            "element_snippet": str(h)[:100]
        })
        prev_level = level

    # 5. Extract Links
    links = []
    for a in soup.find_all('a', href=True):
        links.append({
            "href": a.get('href'),
            "text": a.get_text(strip=True) or None,
            "aria_label": a.get('aria-label'),
            "element_snippet": str(a)[:100]
        })

    return {
        "images": images,
        "buttons": buttons,
        "forms": forms,
        "headings": headings,
        "links": links
    }
