
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="Auto DDl API", description="LLM기반의 컬럼 논리명, 물리명 생성 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 도메인을 명시. "*"는 모든 도메인 허용.
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드. "*"는 모든 메서드 허용.
    allow_headers=["*"],  # 허용할 HTTP 헤더.
)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

class InferenceRequest(BaseModel):
    physical_col_nm: str
    logical_col_nm: str
    col_type: str


# Example endpoint
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Function to recommend physical column name
@app.post("/inference_physical_col_nm")
def inference_physical_col_nm(request: InferenceRequest):
    recommended_name = f"{request.physical_col_nm[:10]}_{request.col_type[:3]}".lower()
    return {"recommend_physical_col_nm": recommended_name}


@app.post("/inference_logical_col_nm")
def inference_physical_col_nm(request: InferenceRequest):
    recommended_name = f"{request.logical_col_nm[:10]}_{request.col_type[:3]}".lower()
    return {"recommend_logical_col_nm": recommended_name}




class InferenceRequestDDL(BaseModel):
    dw: str
    schema: str
    table: str
    columns: List


@app.post("/create_ddl")
def create_ddl(request: InferenceRequestDDL):
    print(request)


    ddl = """
    CREATE TABLE dw.ast.test
    (id varhar comments '아이디')
    """
    return {"ddl": ddl}


class InferenceAnalysisDDL(BaseModel):
    ddl: str


@app.post("/analysis_ddl")
def create_ddl(request: InferenceAnalysisDDL):
    print(request)

    data = {"database":"Test",
            "schema":"Test",
            "table":"Test",
            "columns":[{'id': 1,
                        'physicalName': 'qw',
                        'logicalName': 'qwe',
                        'dataType': 'varchar',
                        'isNull': False,
                        'applyPhysicalSuggestion': True,
                        'applyLogicalSuggestion': False,
                        'suggestedPhysicalName': 'qw_var'},
                       {'id': 2,
                        'physicalName': 'qew',
                        'logicalName': 'qwe',
                        'dataType': 'varchar',
                        'isNull': False,
                        'applyPhysicalSuggestion': False,
                        'applyLogicalSuggestion': True,
                        'suggestedLogicalName': 'qwe_var'},
                       {'id': 3,
                        'physicalName': 'e',
                        'logicalName': 'e',
                        'dataType': 'varchar',
                        'isNull': False,
                        'applyPhysicalSuggestion': False,
                        'applyLogicalSuggestion': False,
                        'suggestedPhysicalName': 'e_var'}]}
    return data
