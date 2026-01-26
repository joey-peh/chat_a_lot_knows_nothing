#!/bin/bash

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to be ready..."
for i in {1..30}; do
    if curl -s http://ollama:11434/api/tags > /dev/null; then
        echo "✓ Ollama is ready!"
        break
    fi
    echo "Attempt $i/30: Waiting for Ollama..."
    sleep 2
done

# Pull the default model
echo "Pulling llama2 model..."
ollama pull llama2

echo "✓ Ollama initialization complete!"
