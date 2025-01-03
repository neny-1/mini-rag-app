import os

class TemplateParser:
    def __init__(self,language:str=None,default_language='en'):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = language

    def set_language(self,language:str):
        # if language is not provided, use default language
        if language is None:
            self.language = self.default_language
        
        language_path = os.path.join(self.current_path,"locales",language)
        if os.path.exists(language_path):
            self.language = language
        else:
            self.language = self.default_language

    
    def get_template(self,group:str,key:str,vars:dict=None):
        if not group or not key:
            return None
        
        # get group file path => src/stores/llm/templates/locales/en/rag.py
        group_path = os.path.join(self.current_path,"locales",self.language,f"{group}.py")
        targeted_language = self.language
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path,"locales",self.default_language,f"{group}.py")
            targeted_language = self.default_language
        
        if not os.path.exists(group_path):
            return None
        
        # import group file
        # runtime import when language is set 
        module = __import__(f"stores.llm.templates.locales.{targeted_language}.{group}",fromlist=[group])

        if not module:
            return None

        # get key from group
        ket_attribute = getattr(module,key)
        return ket_attribute.substitute(vars) # substitute vars in the template string 
