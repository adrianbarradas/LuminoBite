with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

p = text.find("Comienza tu investigación nutricional")
if p == -1:
    p = text.find("Comienza tu investigaci")
print('Onboarding text found at:', p)
if p != -1:
    print(repr(text[p-100:p+800]))

