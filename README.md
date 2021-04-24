# VuMoS - USP's Vulnerability Monitoring System

## Vulnerability scanning and assessment tool

Developed by USP's [HDB](https://hackersdobem.sti.usp.br), VuMoS automates recon and OpSec testing in order to facilitate 
vulnerability assessment and bug reporting within the [University of São Paulo](https://www5.usp.br/)'s  IT infrastructure.

## Usage

During first-time usage, start the Alembic docker module to update and version databases:
```
docker-compose up alembic
```

And to run the subsequent recon/attack VuMoS modules: 
```
docker-compose up 
```

Alternatively, 
```
docker-compose up -d
```
to hide docker logs during the VuMoS usage.



<br>
2021 © Hackers Do Bem USP
