from fastapi import APIRouter, Depends, HTTPException

import psutil
import GPUtil

from app.api.depencies.guard import require_role
from app.services.role_service import ADMIN_ROLE

router = APIRouter(prefix="/monitoring", tags=["monitoring"])




@router.get("/resources", dependencies=[Depends(require_role(ADMIN_ROLE))])
def get_resource_usage():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
        "gpu": [gpu.__dict__ for gpu in GPUtil.getGPUs()]
    }

@router.get("/processes", dependencies=[Depends(require_role(ADMIN_ROLE))])
def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'cmdline']):
        try:
            cmdline = proc.info.get("cmdline", [])
            # Убедимся, что cmdline всегда список
            if isinstance(cmdline, list) and ("python" in proc.info["name"].lower() or "uvicorn" in " ".join(cmdline)):
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)