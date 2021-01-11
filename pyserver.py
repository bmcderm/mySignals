import os
import glob
import json
import hashlib
import requests
import argparse

from config import Config
from colorama import Fore, init

USERNAME = ''
DOMAIN_NAME = ''
BASE_FILEPATH = f'home/{USERNAME}/'
API_URL = 'https://www.pythonanywhere.com'
HEADERS = {
    'Authorization': f'Token {Config.PYTHON_ANYWHERE_API_TOKEN}',
}

# NOTE: .png, .tff, .woff, .woff2 FILES CANNOT BE UPLOADED! MUST BE DONE MANUALLY
EXTENSIONS = ['.py', '.html', '.css', '.js']
IGNORE_FOLDERS = ['env', 'icons', 'logs',
                  '__pycache__', '.vscode', 'migrations']


init(autoreset=True)
parser = argparse.ArgumentParser(
    description='Controls the PythonAnywhere server for Waffler.')

parser.add_argument('-f', '--f', help='This command will force upload every file, '
                    'even if it hasn\'t been modified.', action='store_true')
parser.add_argument('-r', '--r', help='This command will restart the server.',
                    action='store_true')


def getProjectFiles() -> list:
    """
        Gets all the project files in this directory
    """
    allFiles = []
    for path, folders, files in os.walk('.'):
        if not any([i in path for i in IGNORE_FOLDERS]):
            allFiles.extend([
                os.path.join(path, i).lstrip('./').lstrip('.\\') for i in files if
                # Makes sure it's a valid file
                any([i.endswith(ext) for ext in EXTENSIONS])
            ])
    return allFiles


def uploadFile(fileName: str) -> bool:
    """
        Uploads a file to the pythonanywhere server
    """
    try:
        with open(fileName, 'r') as f:
            pythonAnywhereFilename = fileName.replace('\\', '/')
            url = f'{API_URL}/api/v0/user/{USERNAME}/files/path/{BASE_FILEPATH + pythonAnywhereFilename}'
            r = requests.post(url,
                              files={'content': f.read()},
                              headers=HEADERS)

            if r.status_code != 200 and r.status_code != 201:
                print(f'{Fore.RED}{fileName} COULD NOT BE UPLOADED!')
                return False
            else:
                print(f'{Fore.GREEN}{fileName} SUCCESSFULLY UPLOADED')
                return True
    except Exception:
        print(f'{Fore.RED}{fileName} COULD NOT BE UPLOADED!')
        return False


def pushFilesToServer(force: bool = False) -> bool:
    """
        Find all files that haven't been modified
        and then upload those files onto the server

        params\n
        force: bool = Whether to upload modified files or not
    """
    try:
        with open('fileHashs.json', 'r') as f:
            fileHashs = json.load(f)
    except FileNotFoundError:
        fileHashs = {}

    successCount = 0
    failCount = 0

    allFiles = getProjectFiles()
    for fileName in allFiles:
        curFileHash = getFileHash(fileName)

        # If the hash we have saved is not the same
        # as the newly calcualted hash, then save the
        # file to upload
        if force or fileHashs.get(fileName) != curFileHash:
            success = uploadFile(fileName)

            if success:
                successCount += 1
                fileHashs[fileName] = curFileHash
            else:
                failCount += 1

    # Save the json
    with open('fileHashs.json', 'w') as f:
        json.dump(fileHashs, f, indent=4)

    if successCount > 0:
        print(f'\n{Fore.GREEN}Uploaded {successCount} file(s).')
        return True
    if failCount > 0:
        print(f'\n{Fore.RED}Upload failed for {failCount} file(s).')
        return False

    print(f'{Fore.CYAN}No files were uploaded!')
    return False


def getFileHash(path: str) -> str:
    """
        Returns the MD5 hash of a file
    """
    h = hashlib.new('md5')
    with open(path, 'rb') as file:
        block = file.read(512)
        while block:
            h.update(block)
            block = file.read(512)

    return h.hexdigest()


def restartServer() -> bool:
    """
        Restarts the pythonanywhere server so that
        modified files can take effect
    """
    print(f'\n{Fore.CYAN}RESTARTING SERVER...')

    url = f'{API_URL}/api/v0/user/{USERNAME}/webapps/{DOMAIN_NAME}/reload/'
    r = requests.post(url, headers=HEADERS)

    if r.status_code == 200:
        print(f'{Fore.GREEN}SUCCESSFULLY RESTARTED SERVER!')
        return True
    else:
        print(r)
        print(r.text)
        print(f'{Fore.RED}SERVER RESTART FAILED!')
        return False


if __name__ == '__main__':
    args = parser.parse_args()

    pushFilesToServer(args.f)
    if args.r:
        restartServer()
