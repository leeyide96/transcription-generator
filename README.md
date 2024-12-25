# Project: ASR API and Elasticsearch Integration

## Access the Services
- **ASR API**: Accessible at `http://35.198.242.84:8001`
  - Health check: `http://35.198.242.84:8001/ping`
  - Process audio: `http://35.198.242.84:8001/asr`
- **Search UI**: Accessible at `http://35.198.242.84:3000`
- **Elasticsearch**: Accessible at `http://35.198.242.84:9200`


## Features
- **ASR API**: Transcribes audio files using a pre-trained Wav2Vec2 model.
- **Transcription Processing**: Processes audio files and updates CSV files with transcriptions and durations.
- **Elasticsearch Integration**: Indexes transcription data in Elasticsearch.
- **Search UI**: Frontend for searching and interacting with indexed data.

## Project Structure
- **`asr_api.py`**: Defines the ASR API with endpoints for health checks and audio transcription.
- **`cv-decode.py`**: Processes a folder of audio files, generates transcriptions using the ASR API, and updates a CSV file.
- **`cv-index.py`**: Indexes transcription data from a CSV file into Elasticsearch.
- **`docker-compose.yaml`**: Defines the services and dependencies for containerized deployment.

## Files and Components

### asr
- `asr_api.py`
  - **Endpoints**:
    - `GET /ping`: Health check endpoint.
    - `POST /asr`: Upload an MP3 file to receive its transcription and duration.
  - **Dependencies**: Utilizes `torchaudio` and Wav2Vec2 for transcription.

 - `cv-decode.py`
   - Processes audio files in a specified folder.
   - Calls the ASR API to generate transcriptions and durations.
   - Updates a CSV file with the results.

### elastic-backend
 - `cv-index.py`
   - Creates an Elasticsearch index if it does not exist.
   - Reads transcription data from a CSV file and indexes it into Elasticsearch.

### search-ui
 - Javascript files are used examples from https://github.com/elastic/app-search-reference-ui-react
 - Edited to fit in the fields required
 - Added sort by option to sort filename or generated text in ascending order

### docker-compose.yaml
- **Services**:
  - `asr-api`: The ASR API service.
  - `elastic-backend-1`: Primary Elasticsearch node.
  - `elastic-backend-2`: Secondary Elasticsearch node.
  - `transcription_runner`: Processes audio files and generates transcriptions.
  - `ingest_runner`: Ingests transcription data into Elasticsearch.
  - `search-ui`: Provides a frontend for searching indexed data.
- **Volumes**:
  - `shared-data`: Shared storage for transcription results.

## Usage Workflow
1. Upload an audio file to the ASR API using the `/asr` endpoint.
2. Process a batch of audio files using `cv-decode.py`.
3. Index transcription data into Elasticsearch using `cv-index.py`.
4. Interact with the data through the search UI.



