from fastapi import APIRouter, Depends, HTTPException


from app.api.depencies.guard import require_role
from app.services.role_service import ADMIN_ROLE

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

from fastapi.responses import HTMLResponse
import psutil
import GPUtil
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import time


def get_system_metrics():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()

    # Memory
    memory = psutil.virtual_memory()
    memory_total = round(memory.total / (1024 ** 3), 2)
    memory_used = round(memory.used / (1024 ** 3), 2)
    memory_percent = memory.percent

    # Disk
    disk = psutil.disk_usage('/')
    disk_total = round(disk.total / (1024 ** 3), 2)
    disk_used = round(disk.used / (1024 ** 3), 2)
    disk_percent = disk.percent

    # GPU (если есть)
    gpu_metrics = []
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_metrics.append({
                "name": gpu.name,
                "load": gpu.load * 100,
                "memory_used": gpu.memoryUsed,
                "memory_total": gpu.memoryTotal,
                "temperature": gpu.temperature
            })
    except:
        pass

    # Processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append({
            "pid": proc.info['pid'],
            "name": proc.info['name'],
            "cpu": proc.info['cpu_percent'],
            "memory": proc.info['memory_percent']
        })

    # Сортируем процессы по потреблению CPU
    processes = sorted(processes, key=lambda x: x['cpu'], reverse=True)[:20]

    return {
        "cpu": {"percent": cpu_percent, "count": cpu_count},
        "memory": {"total": memory_total, "used": memory_used, "percent": memory_percent},
        "disk": {"total": disk_total, "used": disk_used, "percent": disk_percent},
        "gpu": gpu_metrics,
        "processes": processes,
        "timestamp": time.time()
    }


def create_plot(data, title, ylabel):
    plt.figure(figsize=(10, 4))
    plt.plot(data)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(True)

    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')


@router.get("/metrics", response_class=HTMLResponse)
async def get_metrics_dashboard():
    metrics = get_system_metrics()

    # Генерация графиков
    cpu_plot = create_plot([metrics["cpu"]["percent"]], "CPU Usage", "Percent")
    mem_plot = create_plot([metrics["memory"]["percent"]], "Memory Usage", "Percent")
    disk_plot = create_plot([metrics["disk"]["percent"]], "Disk Usage", "Percent")

    # Таблица процессов
    processes_df = pd.DataFrame(metrics["processes"])
    processes_html = processes_df.to_html(index=False, classes="table table-striped")

    # HTML шаблон
    html_content = f"""
    <html>
        <head>
            <title>System Monitoring Dashboard</title>
            <style>
                .dashboard {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                .metrics-container {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                }}
                .metric-card {{
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    width: 30%;
                    min-width: 300px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .plot {{
                    margin: 20px 0;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <h1>System Monitoring Dashboard</h1>

                <h2>Resource Usage</h2>
                <div class="metrics-container">
                    <div class="metric-card">
                        <h3>CPU: {metrics["cpu"]["percent"]}%</h3>
                        <div class="plot">
                            <img src="data:image/png;base64,{cpu_plot}" alt="CPU Usage">
                        </div>
                        <p>Cores: {metrics["cpu"]["count"]}</p>
                    </div>

                    <div class="metric-card">
                        <h3>Memory: {metrics["memory"]["percent"]}%</h3>
                        <div class="plot">
                            <img src="data:image/png;base64,{mem_plot}" alt="Memory Usage">
                        </div>
                        <p>Used: {metrics["memory"]["used"]} GB / {metrics["memory"]["total"]} GB</p>
                    </div>

                    <div class="metric-card">
                        <h3>Disk: {metrics["disk"]["percent"]}%</h3>
                        <div class="plot">
                            <img src="data:image/png;base64,{disk_plot}" alt="Disk Usage">
                        </div>
                        <p>Used: {metrics["disk"]["used"]} GB / {metrics["disk"]["total"]} GB</p>
                    </div>
                </div>

                <h2>GPU Metrics</h2>
                <div class="metrics-container">
                    {''.join([f'''
                    <div class="metric-card">
                        <h3>{gpu['name']}</h3>
                        <p>Load: {gpu['load']:.1f}%</p>
                        <p>Memory: {gpu['memory_used']} MB / {gpu['memory_total']} MB</p>
                        <p>Temperature: {gpu['temperature']}°C</p>
                    </div>
                    ''' for gpu in metrics["gpu"]]) if metrics["gpu"] else '<p>No GPU detected</p>'}
                </div>

                <h2>Top Processes</h2>
                {processes_html}
            </div>
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)


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