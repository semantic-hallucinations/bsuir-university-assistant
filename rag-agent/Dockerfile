FROM langchain/langchain:latest

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt ./requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/SERVICE_PATH
COPY . .