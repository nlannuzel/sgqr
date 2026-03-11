from yaml import load, Loader
from enum import Enum, auto
from nlannuzel.sgqr.tokenizer import Tokenizer

class Template(Enum):
    ROOT = auto(),
    MERCHANT_ACCOUNT_INFORMATION_PAYNOW = auto(),
    ADDITIONAL_DATA_FIELDS = auto(),
    MERCHANT_INFORMATION_LANGUAGE = auto(),
    RESERVED_FOR_FUTURE_USE = auto(),
    UNRESERVED = auto(),

class SpecTable():
    def __init__(self, template: Template, specs_dir: str='specs'):
        spec_files = {
            Template.ROOT: 'root-data.yaml',
            Template.ADDITIONAL_DATA_FIELDS: '62-additional-data-fields-template.yaml',
            Template.MERCHANT_INFORMATION_LANGUAGE: '64-merchant-information-language-template.yaml',
            Template.UNRESERVED: '80-99-unreserved-templates.yaml',
            Template.MERCHANT_ACCOUNT_INFORMATION_PAYNOW: '26-sg-paynow.yaml',
        }
        self._template = template
        self._spec_file = specs_dir + '/' + spec_files[template] if template in spec_files else None
        self._table = None

    @property
    def spec_file(self) -> str:
        return self._spec_file

    @property
    def template(self) -> Template:
        return self._template

    @property
    def table(self) -> list[list]:
        if self.spec_file is None:
            raise NoSpecfileError(self.template)
        if self._table is None:
            with open(self.spec_file) as f:
                self._table = load(f, Loader=Loader)
        return self._table

    def match_range(self, id_range: str, value: str) -> bool:
        a = id_range.split('-')
        return a[0] == value if len(a) == 1 else a[0] <= value <= a[1]

    def lookup_field_name(self, field_id: str) -> str:
        for row in self.table:
            if self.match_range(row[1], field_id):
                return row[0]
        raise UnknownFieldError(self.template, field_id)

def get_mai_template(uid: str) -> Template:
    match uid:
        case 'SG.PAYNOW':
            return Template.MERCHANT_ACCOUNT_INFORMATION_PAYNOW
        case '_':
            raise UnknownMAIUIDError(uid)

def get_uid(s: str) -> str:
    entry_id, entry_value = next(iter(Tokenizer(s)))
    if entry_id != '00':
        raise MissingUIDError(s)
    return entry_value

def get_template(parent: Template, entry_id: str, entry_value: str) -> Template:
    if parent is not Template.ROOT:
        return None
    if '02' <= entry_id <= '51':
        return get_mai_template(get_uid(entry_value))
    if entry_id == '62':
        return Template.ADDITIONAL_DATA_FIELDS
    if entry_id == '64':
        return Template.MERCHANT_INFORMATION_LANGUAGE
    if '65' <= entry_id <= '79':
        return Template.RESERVED_FOR_FUTURE_USE
    if '80' <= entry_id <= '99':
        uid = get_uid(entry_value)
        return Template.UNRESERVED
    return None

def make_entry(ent_i: str, ent_v: str, parent: Template, spec: SpecTable) -> dict:
    tmpl = get_template(parent, ent_i, ent_v)
    return {
        'id': ent_i,
        'value': ent_v if tmpl is None else parse_str(tmpl, ent_v),
        'name': spec.lookup_field_name(ent_i),
    }

def parse_str(parent: Template, s: str) -> list[dict]:
    spec = SpecTable(parent)
    return [ make_entry(i, v, parent, spec) for i, v in Tokenizer(s) ]

class TemplateError(RuntimeError):
    pass

class NoSpecfileError(TemplateError):
    def __init__(self, template):
        super().__init__(template + ': no specfile')

class UnknownFieldError(TemplateError):
    def __init__(self, template, field_id):
        super().__init__(template + f"unknown field {field_id}")

class UnknownMAIUIDError(TemplateError):
    def __init__(self, uid):
        super().__init__(f"unknown merchant account information UID: {uid}")

class MissingUIDError(TemplateError):
    def __init__(self, s):
        super().__init__(f"no UID in {s}")
