# vim:ts=4:sts=4:sw=4:expandtab


from kolejka.judge import config
from kolejka.judge.tasks.build.base import *
from kolejka.judge.paths import *
from kolejka.judge.typing import *
from kolejka.judge.validators import *
from kolejka.judge.commands import *
from kolejka.judge.tasks.base import TaskBase


__all__ = [
        'BuildCompilerTask', 'SolutionBuildCompilerTask', 'ToolBuildCompilerTask',
        'BuildGCCTask', 'SolutionBuildGCCTask', 'ToolBuildGCCTask',
        'BuildGXXTask', 'SolutionBuildGXXTask', 'ToolBuildGXXTask',
        'BuildNVCCTask', 'SolutionBuildNVCCTask', 'ToolBuildNVCCTask', 'SolutionBuildRustTask'
        ]
def __dir__():
    return __all__


class BuildCompilerTask(BuildTask):
    @default_kwargs
    def __init__(self, compiler=None, build_arguments=None, source_globs=None, libraries=None, **kwargs):
        super().__init__(**kwargs)
        self.compiler = compiler or CompileCommand
        self.build_arguments = build_arguments
        self.source_globs = source_globs or []
        self.libraries = libraries

    def get_source_files(self):
        result = []
        for f in self.find_files(self.source_directory):
            for source_glob in self.source_globs:
                if f.match(source_glob):
                    result += [f]
                    break
        return result

    def ok(self):
        return len(self.get_source_files()) > 0

    @property
    def compiler_kwargs(self):
        return self.get_compiler_kwargs()
    def get_compiler_kwargs(self):
        kwargs = dict()
        if self.build_directory is not None:
            kwargs['build_directory'] = self.build_directory
        if self.build_arguments is not None:
            kwargs['build_arguments'] = self.build_arguments
        if self.build_options is not None:
            kwargs['build_options'] = self.build_options
        if self.build_target is not None:
            kwargs['build_target'] = self.build_target
        if self.libraries is not None:
            kwargs['libraries'] = self.libraries
        return kwargs

    def execute_build(self):
        status = self.run_command('compile', self.compiler,
                source_files=self.get_source_files(),
                **self.compiler_kwargs
                )
        return status

    def get_execution_command(self):
        return self.commands['compile'].execution_command


class SolutionBuildCompilerTask(SolutionBuildMixin, BuildCompilerTask):
    pass
class ToolBuildCompilerTask(ToolBuildMixin, BuildCompilerTask):
    pass

class BuildGCCTask(BuildCompilerTask):
    DEFAULT_COMPILER = GCCCommand
    DEFAULT_SOURCE_GLOBS = [
        '*.[Cc]',
        ]
    @default_kwargs
    def __init__(self, static=None, version=None, standard=None, **kwargs):
        super().__init__(**kwargs)
        self.version = version
        self.standard = standard
        self.static = static
    def get_compiler_kwargs(self):
        kwargs = super().get_compiler_kwargs()
        if self.version is not None:
            kwargs['version'] = self.version
        if self.standard is not None:
            kwargs['standard'] = self.standard
        if self.static is not None:
            kwargs['static'] = self.static
        return kwargs

class BuildRustTask(BuildCompilerTask):
    DEFAULT_COMPILER = RustcCommand
    DEFAULT_SOURCE_GLOBS = [
        '*.[Rr][Ss]',
    ]
    
    @default_kwargs
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute_build(self):
        self.run_command("create_dir", CreateDirectoryCommand, path="libs")
        self.run_command("move_libraries", MoveLibraryCommand, source="solution/src/rand/", target="libs/")
        
        self.run_command("cargo_new", CargoNewCommand, path="rust_project")
        
        # FIXME: This works only unders assumption that source directory is /src/
        self.run_command("copy_source", CopySourceCommand, source=self.source_directory, target="rust_project")
        self.run_command("add_offline_dependency", AddOfflineDependency, project_path="rust_project/Cargo.toml", dep_path="libs/rand")
        
        self.run_command("cargo_build", CargoBuildCommand, target="rust_project/Cargo.toml")
        
        self.run_command("copy_executable", CopyExecutableCommand, source="rust_project/target/debug/rust_project", target=self.build_directory)
        
        self.run_command("rename_executable", RenameExecutableCommand, source="solution/build/rust_project", target="solution/build/a.out")
        
        return super().execute_build()

class SolutionBuildGCCTask(SolutionBuildMixin, BuildGCCTask):
    pass
class ToolBuildGCCTask(ToolBuildMixin, BuildGCCTask):
    pass

class BuildGXXTask(BuildGCCTask):
    DEFAULT_COMPILER = GXXCommand
    DEFAULT_SOURCE_GLOBS = [
        '*.[Cc][Pp][Pp]',
        '*.[Cc][Cc]',
        ]
    @default_kwargs
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class SolutionBuildGXXTask(SolutionBuildMixin, BuildGXXTask):
    pass
class SolutionBuildRustTask(SolutionBuildMixin, BuildRustTask):
    pass 
class ToolBuildGXXTask(ToolBuildMixin, BuildGXXTask):
    pass

class BuildNVCCTask(BuildGCCTask):
    DEFAULT_COMPILER = NVCCCommand
    DEFAULT_SOURCE_GLOBS = [
        '*.[Cc][Uu]',
        ]
    @default_kwargs
    def __init__(self, architecture=None, **kwargs):
        super().__init__(**kwargs)
        self.architecture = architecture
    def get_compiler_kwargs(self):
        kwargs = super().get_compiler_kwargs()
        if self.architecture is not None:
            kwargs['architecture'] = self.architecture
        return kwargs

class SolutionBuildNVCCTask(SolutionBuildMixin, BuildNVCCTask):
    pass
class ToolBuildNVCCTask(ToolBuildMixin, BuildNVCCTask):
    pass
