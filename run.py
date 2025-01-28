import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

path_to_dir = Path.cwd()

run = os.environ.get('RUN')
marker = os.environ.get('MARKER')
maxfail = os.environ.get('MAXFAIL', '10')
tests = ""

if run == "*":
    for i in run:
        if '.py' in i and i not in [
                'http_methods.py', 'checking.py'
        ]:
            tests += f'tests/{i} '
else:
    run = run.split(',')
    for i in run:
        if '::' in i:
            # Если указан конкретный тест внутри файла
            tests += f'tests/{i} '
        else:
            # Если указан только файл
            tests += f'tests/{i}.py '
        # tests += f'tests{test_version}/{i}.py '

command = f'pytest -v -s {tests} --clean-alluredir --maxfail {maxfail} --alluredir=./allure_results --junit-xml=xml_report/report'

if marker:
    command += f' -m {marker}'

os.system(command)
os.system('allure generate -c ./allure_results -o ./allure_report')
os.system('allure open ./allure_report')
