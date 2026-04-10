FROM python:3.11-slim

# Install LibreOffice (perfect Word→PDF conversion) + weasyprint system libs
RUN apt-get update && apt-get install -y \
    libreoffice \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libglib2.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
