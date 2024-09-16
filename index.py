import os
from supabase import create_client, Client
from controllers import admin_controller
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_controller.router)


# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("custom_logger")

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Middleware to log request details including query parameters
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        query_params = dict(request.query_params)
        logger.info(f"Request: {request.method} {request.url} | Query: {query_params}")
        response = await call_next(request)
        return response

# Nice to have custom logging
# app.add_middleware(LoggingMiddleware)

@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    ) 


@app.get("/")
async def root():
    return {"message": "Bonjour, Bienvenue dans totory"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)

