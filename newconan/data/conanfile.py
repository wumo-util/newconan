from conans import ConanFile, CMake

class {project_name}Conan(ConanFile):
  settings = "os", "compiler", "build_type", "arch"
  requires = ()
  generators = "cmake"

  default_options = {}

  def imports(self):
    self.copy("*.dll", dst="bin", src="bin", )
    self.copy("*.pdb", dst="bin", src="bin", )
