from bs4 import BeautifulSoup

# HTML report parsing functions

# Example function to parse HTML test report
# Returns: {'status': 'pass'/'fail', 'faults': [...], 'replace': [...]} 
def parse_html_report(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # Dummy logic: look for keywords in HTML
    status = 'pass' if 'Test Pass' in soup.text else 'fail'
    faults = []
    replace = []
    # Example: find all <li class="fault">...</li>
    for li in soup.find_all('li', class_='fault'):
        faults.append(li.text.strip())
    for li in soup.find_all('li', class_='replace'):
        replace.append(li.text.strip())
    return {'status': status, 'faults': faults, 'replace': replace}
