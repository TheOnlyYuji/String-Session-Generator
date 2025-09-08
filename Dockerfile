# Use an official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies file first for better cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port if needed (e.g., webhooks); optional
# EXPOSE 8443

# Define default environment variables (can be overridden)
ENV API_ID=""
ENV API_HASH=""
ENV BOT_TOKEN=""
ENV OWNER_ID=""

# Start the bot
CMD ["python", "bot.py"]
