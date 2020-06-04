from conans import ConanFile, CMake, tools


class {project_name}Conan(ConanFile):
    name = "{project_name}"
    version = "0.0.1"
    settings = "os", "compiler", "build_type", "arch"
    requires = ()
    generators = "cmake"
    scm = {
        "type": "git",
        "subfolder": name,
        "url": "auto",
        "revision": "auto"
    }
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": {is_shared}
    }

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TEST"] = False
        cmake.definitions["BUILD_SHARED"] = self.options.shared
        cmake.configure(source_folder=self.name)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dll", dst="bin", src="lib")
        self.copy("*.dylib", dst="bin", src="lib")
        self.copy("*.pdb", dst="bin", src="bin")

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        self.copy("*.h", dst="include", src=f"{self.name}/src")
        self.copy("*.hpp", dst="include", src=f"{self.name}/src")
    
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
