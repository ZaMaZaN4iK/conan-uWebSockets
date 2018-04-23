from conans import ConanFile, CMake, tools


class uWebSocketsConan(ConanFile):
    name = "uWebSockets"
    version = "0.13.0"
    license = "BSD 3-clause \"New\" or \"Revised\" License"
    license_url = "https://raw.githubusercontent.com/uNetworking/uWebSockets/master/LICENSE"
    url = "https://github.com/kwallner/uWebSockets.git"
    description = "lightweight, efficient & scalable WebSocket & HTTP server implementations"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    repository = "https://github.com/kwallner/uWebSockets.git"
    branch = "develop-v0.13"
    no_copy_source = True

    def requirements(self):
        self.requires("boost/1.67.0@%s/%s" % ("kwallner", "testing"))
        self.requires("libuv/1.15.0@%s/%s" % ("kwallner", "testing"))
        self.requires("zlib/1.2.11@%s/%s" % ("kwallner", "testing"))
        self.requires("OpenSSL/1.0.2o@%s/%s" % ("kwallner", "testing"))

    def config(self):
        if self.settings.compiler != "Visual Studio":
            self.settings.compiler.libcxx = 'libstdc++11'

    def source(self):
        self.run("git clone %s" % self.repository)
        self.run("cd uWebSockets && git checkout %s" % (self.branch))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_DEBUG_POSTFIX"]= "" # No postfix as distinct directories are used
        cmake.definitions["BUILD_SHARED_LIBS"] = "OFF" # Does not yet compile as shared
        cmake.configure(source_dir="%s/uWebSockets" % (self.source_folder))
        cmake.build()
        cmake.install()
        cmake.test()

    def package(self):
        self.copy("LICENSE", "LICENSE.txt", "")
        self.copy("README.md", "README.md", "")

    def package_info(self):
        self.cpp_info.libs = ["uWS"]
