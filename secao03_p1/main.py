from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Query
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Header
from fastapi import Path
from fastapi import status
from fastapi import Depends

from time import sleep
from models import Curso
from models import cursos

def fake_db():
    try:
        print('Abrindo conexão com o banco de dados')
        sleep(1)
    finally:
        print('Fechando conexão com banco de dados')
        sleep(1)

app = FastAPI(
    title='API de Cursos da Geek University',
    version='0.0.1',
    description='Uma API para estudo do FASTAPI'
)


@app.get('/cursos', 
         description='Retorna todos os cursos ou uma lista vazia', 
         summary='Retorna todos os cursos', 
         response_model=List[Curso],
         response_description='Cursos encontrados com sucesso'
        )
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
    
@app.post('/cursos', response_model=Curso)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    del curso.id
    return curso

@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        curso.id = curso_id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com id {curso_id}')
    
@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        #return JSONResponse(status_code=status.HTTP_204_NO_CONTENT) 
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'ID {curso_id} não existe')
    
@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default=None),c: Optional[int] = None):
    soma: int = a + b
    if c:
        soma = soma + c
    resultado = a + b + c
    print(f'X_GEEK: {x_geek}')
    return {'resultado': resultado}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
