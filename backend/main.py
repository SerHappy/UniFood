from asyncpg import Connection, Record, connect
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
