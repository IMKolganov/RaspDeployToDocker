# ���������� ������� ����� Python
FROM python:3.12-slim

# ������������� ������� ���������� � ����������
WORKDIR /app

# �������� ���� ������������ � ������� ����������
COPY requirements.txt .

# ������������� �����������
RUN pip install --no-cache-dir -r requirements.txt

# �������� �� ���������� ������� � ������� ����������
COPY . .

# ��������� ���� 5000 ��� Flask
EXPOSE 5000

# ������� ��� ������� ����������
CMD ["python", "app.py"]