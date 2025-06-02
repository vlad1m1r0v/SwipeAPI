import dishka as di

from jinja2 import Environment, FileSystemLoader, ChoiceLoader

from src.core.constants import BASE_DIR


class JinjaProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    def provide_jinja2_env(self) -> Environment:
        template_dirs = [
            str(path) for path in BASE_DIR.glob("**/templates") if path.is_dir()
        ]

        loader = ChoiceLoader(
            [FileSystemLoader(dir_path) for dir_path in template_dirs]
        )
        return Environment(loader=loader, autoescape=True)
