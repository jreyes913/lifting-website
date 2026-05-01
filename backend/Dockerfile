FROM python:3.12-slim

# /workspace is the project root; backend is mounted/copied as a sub-package
WORKDIR /workspace

COPY requirements.txt ./backend/requirements.txt

# requirements.txt is UTF-16 encoded on Windows; convert before pip install
RUN python3 -c "
content = open('backend/requirements.txt', 'rb').read()
if content[:2] in (b'\xff\xfe', b'\xfe\xff'):
    content = content.decode('utf-16').encode('utf-8')
open('backend/requirements.txt', 'wb').write(content)
" && pip install --no-cache-dir -r backend/requirements.txt

COPY . ./backend/

EXPOSE 8000

# Run as backend.app so relative imports inside app.py resolve correctly
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
