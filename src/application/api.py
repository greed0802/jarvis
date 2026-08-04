from src.application.runtime import RuntimeEngine

def handle_request(path: str, method: str = "GET") -> dict:
    if path == "/health":
        return {"status": 200, "data": {"health": "OK"}}
        
    engine = RuntimeEngine()
    
    if path == "/version":
        try:
            context = engine.initialize_runtime()
            return {"status": 200, "data": {"version": context.repository_version}}
        except Exception:
            return {"status": 500, "error": "Internal Server Error"}
            
    if path == "/status":
        try:
            context = engine.initialize_runtime()
            return {"status": 200, "data": {"runtime_status": context.status}}
        except Exception:
            return {"status": 500, "error": "Internal Server Error"}
            
    return {"status": 404, "error": "Not Found"}