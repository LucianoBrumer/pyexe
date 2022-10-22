import tkinter as tk
from tkinter import filedialog
from os import system, path, remove, rename
from shutil import rmtree
from python_minifier import minify

if __name__ == "__main__":

    system('pip3 install pyinstaller')
    
    root = tk.Tk()
    root.withdraw()

    target_path = filedialog.askopenfilename(filetypes=[('Python file', '.py .pyw')],title='Select python file')
    icon_path = filedialog.askopenfilename(filetypes=[('Ico file', '.ico')],title='Select icon')
        
    if(path.isfile(target_path)):

        file_path = path.dirname(__file__)
        upx_path = path.join(file_path, 'upx-3.96-win64')

        target_name = path.basename(target_path)
        target_name_without_extension = path.splitext(target_name)[0]

        if(path.isdir('build')): rmtree('build')
        else: system('mkdir build')
    
        target_name_list = target_name.split('.')
        target_name_minify = f'{target_name_without_extension}.min.{target_name_list[len(target_name_list)-1]}'

        target_path_minify = path.join(path.dirname(__file__), f'build/{target_name_minify}')

        with open(target_path) as f:
            minify_code = minify(f.read())

            with open(target_path_minify, 'w+') as f:
                f.write(minify_code)

        while not(path.isfile(target_path_minify)):
            print(path.isfile(target_path_minify), target_path_minify)
        
        if(path.isfile(icon_path)):
            system(f'cd build && pyinstaller -w -F --onefile --upx-dir="{upx_path}" --icon="{icon_path}" "{target_path_minify}"')
        else:
            system(f'cd build && pyinstaller -w -F --onefile --upx-dir="{upx_path}" "{target_path_minify}"')
            
        while not(path.isfile(f'build/dist/{target_name_without_extension}.min.exe')):
            print(path.isfile(f'build/dist/{target_name_without_extension}.min.exe'), f'build/dist/{target_name_without_extension}.min.exe')
            
        rmtree('build/build')
        rename(f'build/dist/{target_name_without_extension}.min.exe', f'build/{target_name_without_extension}.exe')
        remove(f'build/{target_name_without_extension}.min.spec')
        rmtree('build/dist')

        print(upx_path)