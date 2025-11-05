# services/placeholder_service.py
from docxtpl import DocxTemplate
import re

class PlaceholderExtractor:
    @staticmethod
    def extract(docx_path):
        """
        Extrai placeholders de um arquivo .docx usando docxtpl.
        Retorna uma lista ordenada de placeholders encontrados.
        """
        try:
            # Carrega o template
            doc = DocxTemplate(docx_path)

            # Usa o método interno para obter todos os placeholders do Jinja2
            placeholders = doc.get_undeclared_template_variables()

            # Retorna como lista ordenada
            return sorted(list(placeholders))

        except Exception as e:
            raise Exception(f"Erro ao extrair placeholders do DOCX: {str(e)}")

    @staticmethod
    def extract_from_text(file_path):
        """
        Extrai placeholders de arquivos de texto simples (.txt, .html, etc)
        usando regex compatível com {{variavel}} ou [variavel].
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = re.compile(r'\{\{(\w+)\}\}|\[(\w+)\]')
        matches = pattern.finditer(content)
        return sorted({
            match.group(1) or match.group(2)
            for match in matches
            if match.group(1) or match.group(2)
        })
