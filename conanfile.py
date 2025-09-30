import json
from pathlib import Path

required_conan_version = ">=2.0"

from conan import ConanFile
from conan.tools.files import copy, collect_libs

class ConanConfiguration(ConanFile):
    settings = "arch", "os", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": True}

    def set_name(self):
        try:
            self.name = json.loads(Path(__file__).parent.joinpath('name-version.json').read_bytes().decode())['name'].lower()
        except Exception as e:
            self.output.error(e)
            raise e

    def set_version(self):
        try:
            self.version = json.loads(Path(__file__).parent.joinpath('name-version.json').read_bytes().decode())['version'].lower()
        except Exception as e:
            self.output.error(e)
            raise e

    def package(self):
        try:
            build_folder_path: Path = Path(self.build_folder)
            package_folder_path: Path = Path(self.package_folder)

            src: str = build_folder_path.joinpath("include").as_posix()
            dst: str = package_folder_path.joinpath("include").as_posix()
            copy(self, pattern="*.*", src=src, dst=dst)

            src: str = build_folder_path.joinpath("cmake").as_posix()
            dst: str = package_folder_path.joinpath("cmake").as_posix()
            copy(self, pattern="*.*", src=src, dst=dst)

            src: str = build_folder_path.joinpath("lib").as_posix()
            dst: str = package_folder_path.joinpath("lib").as_posix()
            copy(self, pattern="*.*", src=src, dst=dst)

            src: str = build_folder_path.joinpath("bin").as_posix()
            dst: str = package_folder_path.joinpath("bin").as_posix()
            copy(self, pattern="*.*", src=src, dst=dst)
        except Exception as e:
            self.output.error(e)
            raise e

    def package_info(self):
        try:
            self.cpp_info.set_property("cmake_file_name", 'CycloneDDS')
            self.cpp_info.libs = collect_libs(self)
        except Exception as e:
            self.output.error(e)
            raise e
