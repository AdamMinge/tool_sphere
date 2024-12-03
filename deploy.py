import os
import zipfile
import argparse
import subprocess
import configparser


def __get_exec_directory(spec_file: str):
    config = configparser.ConfigParser()
    config.read(spec_file)
    return config["app"].get("exec_directory")

def __deploy_app(spec_file: str):
    subprocess.run(["pyside6-deploy", "-c", spec_file])

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

def deploy(spec_file: str, plugins_dir: str):
    dist_dir = __get_exec_directory(spec_file)
    output_dir = os.path.join(dist_dir, os.path.basename(plugins_dir))

    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)

    __deploy_app(spec_file)
    __deploy_plugins(plugins_dir, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Deploy application.")
    parser.add_argument(
        "--spec-file", 
        type=str, 
        default="./pysidedeploy.spec",
        help="Path to the PySide6 deployment spec file (default: ./pysidedeploy.spec)"
    )
    parser.add_argument(
        "--plugins-path", 
        type=str, 
        default="./plugins",
        help="Path to the plugins directory (default: ./plugins)"
    )

    args = parser.parse_args()
    deploy(args.spec_file, args.plugins_path)
    

if __name__ == "__main__":
    main()