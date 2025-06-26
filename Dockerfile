FROM python:3.11

WORKDIR /scrape_house_listings

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scrape_house_listings.py"]