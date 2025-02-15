import uvicorn
from dotenv import load_dotenv
load_dotenv()
import os
from stockzrs_metrics_service.server import app

metrics_service_host = os.environ.get('METRICS_SERVICE_HOST') or "0.0.0.0"
def main():
    uvicorn.run(app, host=metrics_service_host, port=80)

if __name__ == "__main__":
    main()