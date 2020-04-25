from jinja2 import Environment, FileSystemLoader, select_autoescape
import os


class TemplateManager:
    def __init__(self):
        self.env = Environment(
                loader=FileSystemLoader(os.getcwd() + "/client/TemplateManager/templates"),
                autoescape=select_autoescape(['html'])
            )

    def get_template(self, template_name, render_args=None):
        if render_args is None:
            render_args = {}

        template = self.env.get_template(template_name)
        return template.render(render_args)


template_manager = TemplateManager()
