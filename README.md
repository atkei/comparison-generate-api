# Comparison Table Generation API

Implementation of an API server that automatically generates JSON that is 
easily converted into a comparison table by [ChatGPT](https://chat.openai.com/) prompt engineering.

## Usage

Set your API key to the environment variable `OPENAI_API_KEY` and install dependencies.

```sh
pip install -r requirements.txt
```

Run server.

```sh
uvicorn main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Sample Payload and Response

Sample payload.

```sh
 curl -X 'POST' \
  'http://localhost:8000/comparison' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": "gpt-3.5-turbo-0613",
  "target1": "Java",
  "target2": "Python",
  "min_items": 5,
  "items": ["Ease of Learning"]
}' | jq .
```

Sample response.

```json
{
  "comparisonResults": [
    {
      "item": "Ease of Learning",
      "target1": {
        "better": true,
        "description": "Java is easier to learn than Python"
      },
      "target2": {
        "better": false,
        "description": "Python is harder to learn than Java"
      }
    },
    {
      "item": "Performance",
      "target1": {
        "better": false,
        "description": "Python has slower performance compared to Java"
      },
      "target2": {
        "better": true,
        "description": "Java has better performance compared to Python"
      }
    },
    {
      "item": "Syntax",
      "target1": {
        "better": false,
        "description": "Java has more complex syntax compared to Python"
      },
      "target2": {
        "better": true,
        "description": "Python has simpler syntax compared to Java"
      }
    },
    {
      "item": "Versatility",
      "target1": {
        "better": true,
        "description": "Java is more versatile than Python"
      },
      "target2": {
        "better": false,
        "description": "Python is less versatile than Java"
      }
    },
    {
      "item": "Community Support",
      "target1": {
        "better": true,
        "description": "Java has a larger and more active community compared to Python"
      },
      "target2": {
        "better": false,
        "description": "Python has a smaller community compared to Java"
      }
    }
  ]
}
```