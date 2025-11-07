from docxtpl import DocxTemplate
import re
from io import BytesIO

class PlaceholderExtractor:
    @staticmethod
    def extract(source):
        """
        Extrai placeholders de um arquivo .docx.
        Aceita tanto um caminho de arquivo (str) quanto um BytesIO.
        Retorna uma lista ordenada de placeholders encontrados.
        """
        try:
            # Se for um caminho de arquivo, abre normalmente
            if isinstance(source, str):
                doc = DocxTemplate(source)
            # Se for um binário (em memória)
            elif isinstance(source, BytesIO):
                doc = DocxTemplate(source)
            else:
                raise TypeError("O parâmetro 'source' deve ser um caminho ou BytesIO.")

            placeholders = doc.get_undeclared_template_variables()
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
