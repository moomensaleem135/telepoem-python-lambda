import subprocess
import json

def lambda_handler(event, context):
    command = event.get('command')
    if command == 'run_process':
        process = subprocess.Popen(['python', 'manage.py', 'run_process'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif command == 'add_links':
        process = subprocess.Popen(['python', 'manage.py', 'add_links'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        return {
            'statusCode': 400,
            'body': 'Invalid command'
        }

    stdout, stderr = process.communicate()
    return {
        'statusCode': 200,
        'body': json.dumps({
            'stdout': stdout.decode(),
            'stderr': stderr.decode()
        })
    }
