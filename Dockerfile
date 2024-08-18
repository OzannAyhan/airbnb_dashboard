FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8050 available to the world outside in the container
EXPOSE 8050

# Define environment variable for Dash to run in production mode
ENV DASH_DEBUG_MODE=False

# Run app.py when the container launches
CMD ["python", "app.py"]