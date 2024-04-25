import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.logger import Logger
from src.models import NanozymesBotRequest, NanozymesBotResponse
from src.rag import call_llm_service

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Установите "*" для разрешения доступа со всех источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP методы
    allow_headers=["*"],  # Разрешить все заголовки
)


@app.post("/nanozymes_bot", response_model=NanozymesBotResponse)
async def handler_nanozymes_bot(request: NanozymesBotRequest):
    Logger.info(f"/nanozymes_bot::request : {request}")
    try:
        link = request.article.get("link", None)
        if link is None:
            return {"answer": "No link", "context": request.context}
        llm_response = call_llm_service(
            request.query_text, request.instruction, request.context, link
        )
        return {
            "answer": llm_response,
            "context": "\n".join(
                [
                    f"Question: {request.query_text}",
                    f"Context: {request.context}",
                    f"Response: {llm_response=}",
                ]
            ),
        }
    except BaseException as error:
        Logger.error(f"Error: {error=}, {type(error)=} {request=}")
        return {
            "answer": f"Error: {error}",
            "context": request.context,
        }


@app.get("/health", status_code=200)
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    Logger.info("RUN SERVER")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
