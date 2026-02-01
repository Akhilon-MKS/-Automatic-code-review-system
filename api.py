"""
backend/api.py

Flask API for The Living Memory Vault backend.
Provides REST endpoints for file processing and chat interactions.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path
import sys
import tempfile
import base64
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# Load environment variables
try:
    load_dotenv()
except UnicodeDecodeError:
    # If .env file has encoding issues, skip loading
    pass

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ingestion import ingest_files
from backend.embeddings import MemoryEmbeddings
from backend.rag import RAGSystem

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=["http://localhost:8000", "http://127.0.0.1:8000"])

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded files (images)."""
    return send_from_directory('uploads', filename)

# Initialize components
embeddings = MemoryEmbeddings()
rag = RAGSystem(embeddings)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

@app.route('/upload', methods=['POST'])
def upload_files():
    """Upload and process files."""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    descriptions = request.form.getlist('descriptions')  # Get descriptions for each file
    uploaded_files = []

    for i, file in enumerate(files):
        if file.filename == '':
            continue

        # Determine file type
        filename = file.filename.lower()
        if filename.endswith(('.txt', '.md')):
            source_type = 'text'
        elif filename.endswith(('.docx', '.doc')):
            source_type = 'word'
        elif filename.endswith(('.mp3', '.wav')):
            source_type = 'audio'
        elif filename.endswith(('.jpg', '.jpeg', '.png')):
            source_type = 'image'
        else:
            continue  # Skip unsupported types

        # Read file data
        file_data = file.read()
        # Get description for this file (if provided)
        description = descriptions[i] if i < len(descriptions) and descriptions[i].strip() else None
        uploaded_files.append((file.filename, file_data, source_type, description))

    if not uploaded_files:
        return jsonify({'error': 'No supported files uploaded'}), 400

    try:
        # Process files
        memories = ingest_files(uploaded_files)

        # Add to embeddings
        embeddings.add_memories(memories)

        return jsonify({
            'message': f'Successfully processed {len(memories)} memories',
            'memories_count': len(memories)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat interactions."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    user_message = data['message']

    try:
        # Retrieve relevant memories
        retrieved = rag.retrieve_memories(user_message)

        # Generate response
        result = rag.generate_response(user_message, retrieved)

        return jsonify({
            'response': result['response'],
            'images': result.get('images', []),
            'audio': result.get('audio', []),
            'sources': retrieved
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/memories', methods=['GET'])
def get_memories():
    """Get stored memories (for debugging/testing)."""
    try:
        # This is a simple way to get some memories - in production, you'd want pagination
        results = embeddings.collection.get(limit=10)
        memories = []
        for i in range(len(results['documents'])):
            memories.append({
                'content': results['documents'][i],
                'metadata': results['metadatas'][i]
            })
        return jsonify({'memories': memories})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_memories', methods=['POST'])
def clear_memories():
    """Clear all stored memories and uploaded files."""
    try:
        # Clear the ChromaDB collection
        # Get all IDs first, then delete them
        all_docs = embeddings.collection.get()
        if all_docs['ids']:
            embeddings.collection.delete(ids=all_docs['ids'])

        # Clear uploaded files directory
        uploads_dir = Path('uploads')
        if uploads_dir.exists():
            for file_path in uploads_dir.glob('*'):
                if file_path.is_file():
                    file_path.unlink()

        return jsonify({'message': 'All memories and uploaded files have been cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
