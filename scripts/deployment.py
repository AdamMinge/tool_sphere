import os
import zipfile
import subprocess


def __deploy_app(deployspec: str):
    subprocess.run(["pyside6-deploy", "-c", deployspec])

def __deploy_plugins(plugins_dir: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for plugin in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin)
        if os.path.isdir(plugin_path):
            zip_path = os.path.join(output_dir, f"{plugin}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(plugin_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, plugin_path)
                        zipf.write(full_path, arcname)

def main():
    deployspec = "pysidedeploy.spec"
    dist_dir = "./.dist"
    plugins_dir = "plugins"
    output_dir = os.path.join(dist_dir, "plugins")

    __deploy_app(deployspec)
    __deploy_plugins(plugins_dir, output_dir)
    

if __name__ == "__main__":
    main()