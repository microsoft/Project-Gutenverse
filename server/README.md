# Flask Stories API

A simple Flask application that provides an API to manage stories. Stories are saved in individual directories identified by GUIDs under the `server/stories` folder.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [Testing](#testing)

---

## Installation

1. Clone the repository:
    ```
    git clone <repository_url>
    ```
  
2. Navigate to the repository directory:
    ```
    cd <repository_directory>
    ```

3. Create a virtual environment (optional but recommended):
    ```
    python3 -m venv venv
    ```
  
4. Activate the virtual environment:
    - On macOS and Linux:
        ```
        source venv/bin/activate
        ```
    - On Windows:
        ```
        .\venv\Scripts\activate
        ```

5. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```
    python app.py
    or 
    flask --app server/run run --debug
    ```

2. Open a web browser or use a tool like Postman to interact with the API. The server will be running at `http://localhost:5000/`.

## API Endpoints

### GET `/stories`

Returns a list of GUIDs corresponding to the available stories.

Example:

```
GET http://localhost:5000/stories
```

### POST `/stories`

Creates a new story. The story should be sent as a JSON object in the request body. A new GUID will be generated for the story, and the story will be saved in a new directory under `server/stories`.

Example:

```
POST http://localhost:5000/stories
{
    "title": "New Story",
    "content": "This is the content of the new story.",
    "author": "Author Name"
}
```

## Testing

### Using `curl`

You can use `curl` to test the API from the command line.

#### To get a list of stories:

```bash
curl -X GET http://localhost:5000/stories
```

#### To create a new story:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"title":"New Story","content":"This is a new story","author":"John Doe"}' http://localhost:5000/stories
```