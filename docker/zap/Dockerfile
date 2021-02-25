# Dockerfile para scan usando OWASP ZAP

FROM owasp/zap2docker-stable as builder

COPY commons amass/commons
COPY recon/amass amass

ENTRYPOINT ["python3", "zap-full-scan.py"]



