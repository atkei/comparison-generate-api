import json
from typing import List

import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ComparisonRequest(BaseModel):
    model: str | None = "gpt-3.5-turbo-0613"
    target1: str
    target2: str
    min_items: int | None = 3
    items: List[str] | None = []


result_schema = {
    "type": "object",
    "properties": {
        "comparisonResults": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string"
                    },
                    "target1": {
                        "type": "object",
                        "description": "Comparison target1",
                        "properties": {
                            "better": {
                                "type": "boolean",
                                "description": "Is it better than target2?",
                            },
                            "description": {
                                "type": "string",
                                "description": "Explanation of the basis for the score"
                            }
                        },
                        "required": ["score", "description"]
                    },
                    "target2": {
                        "type": "object",
                        "description": "Comparison target2",
                        "properties": {
                            "better": {
                                "type": "boolean",
                                "description": "Is it better than target1?",
                            },
                            "description": {
                                "type": "string",
                                "description": "Explanation of the basis for the score"
                            }
                        },
                        "required": ["score", "description"]
                    }
                },
                "required": ["item", "target1", "target2"]
            }
        }
    },
    "required": ["comparisonResults"]
}


def to_content(req: ComparisonRequest):
    content = "Please compare target1: {} with target2: {}. Items should include at least {}.".format(req.target1, req.target2, req.min_items)

    if len(req.items) > 0:
        content += "\nItems must include {}".format(','.join(req.items))

    print(content)
    return content


@app.post("/comparison")
async def create_comparison(req: ComparisonRequest):
    try:
        res = openai.ChatCompletion.create(
            model=req.model,
            messages=[
                {"role": "user", "content": to_content(req)}
            ],
            functions=[
                {"name": "set_definition", "parameters": result_schema}
            ],
            function_call={"name": "set_definition"}
        )

        return json.loads(res.choices[0].message.function_call.arguments)
    except openai.error.InvalidRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
