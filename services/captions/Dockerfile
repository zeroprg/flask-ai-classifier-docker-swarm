# Use the official Python base image with version 3.7
FROM python:3.7

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining project files to the container
COPY . .

# Set the entrypoint command to run your script
CMD ["python", "your_script.py"]
