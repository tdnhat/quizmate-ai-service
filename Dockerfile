FROM continuumio/miniconda3:latest

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/conda/bin:${PATH}"

# Copy environment file
COPY environment.yml .

# Create conda environment and install packages
# Force conda to install as many packages as possible from conda-forge
RUN conda env create -f environment.yml && \
    conda clean -afy

# Install curl for healthcheck
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Add conda environment to path and run application
SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "quizmate"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 