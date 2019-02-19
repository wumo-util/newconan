from conans import ConanFile, CMake, tools

class {project_name}Conan(ConanFile):
  name = "{project_name}"
  settings = "os", "compiler", "build_type", "arch"
  requires = ()
  generators = "cmake"
  scm = {
    "type": "git",
    "subfolder": name,
    "url": "auto",
    "revision": "auto"
  }
  default_options = {}

  def build(self):
    cmake = CMake(self)
    cmake.configure(source_folder=self.name)
    cmake.build()

  def imports(self):
    self.copy("*.dll", dst="bin", src="bin", )
    self.copy("*.pdb", dst="bin", src="bin", )

  def package(self):
    self.copy("*.h", dst="include", src=f"{self.name}/src")
    self.copy("*.dll", dst="bin", keep_path=False)
    self.copy("*.so", dst="lib", keep_path=False)
    self.copy("*.dylib", dst="lib", keep_path=False)
    self.copy("*.a", dst="lib", keep_path=False)
    self.copy("*.lib", dst="lib", keep_path=False)

  def package_info(self):
    self.cpp_info.libs = tools.collect_libs(self)
