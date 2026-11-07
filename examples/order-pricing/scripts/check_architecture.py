"""Example-only C4-to-code allocation checks, not a generic skill validator."""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re

DEMO = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def assess(demo, skill_root):
    path = skill_root / 'skills/mkl-uml-c4-architecture/scripts/validate_c4.py'
    spec = importlib.util.spec_from_file_location('c4_profile', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = json.loads((demo / 'architecture/component-code-map.json').read_text(encoding='utf-8'))
    parsed = module.inspect((demo / 'architecture/component.puml').read_text(encoding='utf-8'), 'component', 'component.puml')
    require(not parsed['errors'] and not parsed['warnings'], 'Component source is outside the checked profile')
    elements = parsed['elements']
    ids = [item['id'] for item in data['components']]
    require(len(ids) == len(set(ids)), 'Duplicate component allocation')
    actual = {key for key, value in elements.items() if value['kind'] == 'component'}
    require(set(ids) == actual, 'Every modeled component needs a code allocation')
    require(data['container'] in elements, 'Parent container is missing')
    model = (demo / '07-class-model/classes.puml').read_text(encoding='utf-8')
    classifiers = set(re.findall(r'^\s*(?:class|interface)\s+(\w+)', model, re.M))
    allocated, symbols = [], set()
    for component in data['components']:
        declared = set()
        for member in component['members']:
            path = (demo / member['path']).resolve()
            require(path.is_relative_to(demo.resolve()), 'Source path escapes example root')
            tree = ast.parse(path.read_text(encoding='utf-8'))
            names = {node.name for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef))}
            for name in member['symbols']:
                require(name in names, 'Missing source declaration: ' + member['path'] + ':' + name)
                identity = (member['path'], name)
                require(identity not in symbols, 'Declaration allocated more than once: ' + str(identity))
                symbols.add(identity); declared.add(name)
        require(set(component['model_classes']) <= declared, 'A mapped classifier has no source declaration')
        allocated.extend(component['model_classes'])
    for helper in data.get('shared_helpers', []):
        path = (demo / helper['path']).resolve()
        require(path.is_relative_to(demo.resolve()), 'Shared helper source escapes example root')
        tree = ast.parse(path.read_text(encoding='utf-8'))
        declarations = {node.name: node for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef))}
        for name in helper['symbols']:
            require(name in declarations, 'Missing shared helper declaration: ' + name)
            identity = (helper['path'], name)
            require(identity not in symbols, 'Shared helper also has an exclusive allocation')
            symbols.add(identity)
            actual_consumers = set()
            for component in data['components']:
                for member in component['members']:
                    if member['path'] == helper['path']:
                        for owner in member['symbols']:
                            if any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                                   and node.func.id == name for node in ast.walk(declarations[owner])):
                                actual_consumers.add(component['id'])
            require(set(helper['used_by']) == actual_consumers,
                    'Shared helper consumers differ from actual calls: ' + name)
    require(len(allocated) == len(set(allocated)), 'Classifier allocated to multiple components')
    require(set(allocated) == classifiers, 'Class model and architecture allocation differ')
    zoom = data['code_view']
    require(zoom['parent_component'] in ids, 'Code view has no parent component')
    parent = next(item for item in data['components'] if item['id'] == zoom['parent_component'])
    code = (demo / zoom['artifact']).read_text(encoding='utf-8')
    code_names = set(re.findall(r'^\s*(?:class|interface)\s+(\w+)', code, re.M))
    require(code_names == set(zoom['classifiers']), 'Code view classifier list differs from its actual source')
    require(code_names <= set(parent['model_classes']), 'Code view leaks across its selected component')
    service = ast.parse((demo / '09-reference-implementation/pricing/service.py').read_text(encoding='utf-8'))
    require(not any(isinstance(node, ast.ImportFrom) and node.module == 'adapters' for node in ast.walk(service)),
            'Application workflow imports concrete adapters')
    return {'passed': True, 'components': len(ids), 'classifiers': len(classifiers),
            'source_declarations': len(symbols), 'code_view_classifiers': len(code_names),
            'limits': 'Declared allocation and one dependency constraint checked; behavior, architecture adequacy and SOLID need separate evidence.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--example-root', type=Path, default=DEMO)
    parser.add_argument('--skill-root', type=Path, default=DEMO.parents[1])
    args = parser.parse_args()
    try:
        result = assess(args.example_root.resolve(), args.skill_root.resolve())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'passed': False, 'error': str(error)})); return 1
    print(json.dumps(result, indent=2)); return 0


if __name__ == '__main__':
    raise SystemExit(main())
