#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. Licensed under Apache-2.0.
"""Check a literal C4-PlantUML profile or a declared architecture handoff.

Read-only standard-library checker. Never evaluates PlantUML, includes or commands.
Exit 0: no structural findings (drafts may be unready); 1: findings or strict gate
failure; 2: unreadable input, invalid JSON or invalid CLI usage.
"""
import argparse
import json
from pathlib import Path
import re
import sys

LEVELS = ('context', 'container', 'component', 'deployment')
INCLUDES = {name: 'C4_' + name.title() for name in LEVELS}
ELEMENTS = {'Person': 'person', 'System': 'system', 'Container': 'container',
            'ContainerDb': 'container', 'ContainerQueue': 'container', 'Component': 'component',
            'ComponentDb': 'component', 'ComponentQueue': 'component', 'Deployment_Node': 'node',
            'Node': 'node', 'System_Boundary': 'system', 'Container_Boundary': 'container',
            'Boundary': 'boundary', 'Enterprise_Boundary': 'boundary'}
ALLOWED = {'context': {'person', 'system', 'boundary'},
           'container': {'person', 'system', 'container', 'boundary'},
           'component': {'person', 'system', 'container', 'component', 'boundary'},
           'deployment': {'person', 'system', 'container', 'node', 'boundary'}}
DISPLAY = {'LAYOUT_TOP_DOWN', 'LAYOUT_LEFT_RIGHT', 'LAYOUT_LANDSCAPE', 'LAYOUT_AS_SKETCH',
           'LAYOUT_WITH_LEGEND', 'SHOW_LEGEND', 'SHOW_PERSON_OUTLINE', 'SHOW_PERSON_PORTRAIT',
           'HIDE_PERSON_SPRITE', 'HIDE_STEREOTYPE'}
LITERAL = re.compile(r'"(?:\\.|[^"\\])*"')
EXTERNAL = {'Person', 'System', 'Container', 'ContainerDb', 'ContainerQueue',
            'Component', 'ComponentDb', 'ComponentQueue'}
ALIAS = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def finding(items, code, location, message):
    items.append({'code': code, 'location': location, 'message': message})


def arguments(text):
    """Split comma-separated literal arguments, preserving quoted commas."""
    parts, start, quoted, escaped, depth = [], 0, False, False, 0
    for index, char in enumerate(text):
        if escaped:
            escaped = False
        elif char == '\\' and quoted:
            escaped = True
        elif char == '"':
            quoted = not quoted
        elif not quoted:
            if char == '(': depth += 1
            elif char == ')': depth -= 1
            elif char == ',' and depth == 0:
                parts.append(text[start:index].strip()); start = index + 1
    if quoted or depth:
        raise ValueError('Unbalanced literal argument list')
    return parts + [text[start:].strip()]


def visible_lines(source):
    """Comments, notes and legends cannot stand in for modeled declarations."""
    block, annotation = False, None
    for number, line in enumerate(source.splitlines(), 1):
        out, quoted, escaped, index = '', False, False, 0
        while index < len(line):
            if block:
                end = line.find("'/", index)
                if end < 0: break
                block, index = False, end + 2
                continue
            char = line[index]
            if not quoted and line[index:index+2] == "/'":
                block, index = True, index + 2; continue
            if char == "'" and not quoted: break
            out += char
            if escaped: escaped = False
            elif char == '\\' and quoted: escaped = True
            elif char == '"': quoted = not quoted
            index += 1
        text = out.strip()
        if annotation:
            if re.match(r'^end\s*' + annotation + r'\b', text, re.I): annotation = None
            continue
        if re.match(r'^(?:note|legend)\b', text, re.I):
            if text.lower().startswith('legend'): annotation = 'legend'
            elif '"' not in text and ':' not in text: annotation = 'note'
            continue
        if text: yield number, text
    if block or annotation:
        yield 0, '!UNTERMINATED_ANNOTATION'


def inspect(source, level, location):
    errors, warnings, elements, relations = [], [], {}, []
    included, started, ended, stack, pending = False, 0, 0, [], None
    for line_no, line in visible_lines(source):
        loc = str(location) + ':' + str(line_no)
        if pending:
            line = pending[1] + ' ' + line
            loc = pending[0]
        if re.match(r'^@startuml(?:\s|$)', line):
            started += 1; continue
        if line == '@enduml': ended += 1; continue
        if started != 1 or ended:
            finding(errors, 'OUTSIDE_DIAGRAM', loc, 'Profile content must be inside the diagram.'); continue
        if line.startswith('!include'):
            if line == '!include <C4/' + INCLUDES[level] + '>': included = True
            else: finding(errors, 'UNSUPPORTED_INCLUDE', loc, 'Use the matching bundled C4 standard library include.')
            continue
        if line == '}':
            if stack: stack.pop()
            else: finding(errors, 'UNBALANCED_BOUNDARY', loc, 'Closing boundary has no opener.')
            continue
        call = re.match(r'^(\w+)\s*\((.*)\)\s*(\{)?$', line)
        if not call:
            if re.match(r'^\w+\s*\(', line) and not line.rstrip().endswith(')'):
                pending = (loc, line); continue
            pending = None
            if re.match(r'^(title\b|caption\b|left to right direction$|top to bottom direction$|skinparam\s+\w+\s+[^{}]+$)', line): continue
            finding(warnings, 'UNSUPPORTED_SYNTAX', loc, 'Not checked by the literal C4 profile.'); continue
        pending = None
        macro, raw, opens = call.groups()
        try: args = arguments(raw)
        except ValueError as exc:
            finding(errors, 'INVALID_CALL', loc, str(exc)); continue
        base = macro[:-4] if macro.endswith('_Ext') else macro
        if base in ELEMENTS and (not macro.endswith('_Ext') or base in EXTERNAL):
            kind = ELEMENTS[base]
            if len(args) < 2 or not ALIAS.fullmatch(args[0]):
                finding(errors, 'INVALID_ELEMENT', loc, 'Expected a literal alias and quoted name.'); continue
            identifier, label = args[0], args[1]
            if not LITERAL.fullmatch(label) or not label[1:-1].strip():
                finding(warnings, 'NONLITERAL_LABEL', loc, 'Name must be a nonempty quoted literal for this profile.')
            if any(not LITERAL.fullmatch(value) for value in args[2:]):
                finding(warnings, 'NONLITERAL_ARGUMENT', loc, 'Computed/named arguments are outside this literal profile.')
            boundary = base.endswith('_Boundary') or base in ('Boundary', 'Deployment_Node', 'Node')
            technology = args[2] if len(args) > 2 and kind in ('container', 'component', 'node') and not base.endswith('_Boundary') else None
            if kind in ('container', 'component') and not base.endswith('_Boundary') and not technology:
                finding(errors, 'TECHNOLOGY_REQUIRED', loc, 'Record the technology or an explicit undecided value.')
            elif technology is not None and not technology.strip('"').strip():
                finding(errors, 'TECHNOLOGY_REQUIRED', loc, 'Technology must not be empty.')
            if identifier in elements: finding(errors, 'DUPLICATE_ALIAS', loc, 'Alias already declared in this view: ' + identifier)
            if kind not in ALLOWED[level]: finding(errors, 'MIXED_LEVEL', loc, 'Element does not belong to this selected C4 level: ' + macro)
            elements[identifier] = {'kind': kind, 'label': label, 'technology': technology,
                                    'parent': stack[-1] if stack else None, 'boundary': boundary,
                                    'external': macro.endswith('_Ext'), 'location': loc}
            if opens:
                if not boundary: finding(errors, 'INVALID_BOUNDARY', loc, 'Only a boundary/node may open a scope.')
                stack.append(identifier)
        elif re.fullmatch(r'(?:Rel|BiRel|Rel_Back)(?:_[UDLR])?', macro):
            if len(args) < 3 or not args[2].strip('"').strip(): finding(errors, 'RELATION_LABEL_REQUIRED', loc, 'A relationship needs two endpoints and intent.')
            else:
                relations.append((args[0], args[1], loc))
                if any(not LITERAL.fullmatch(value) for value in args[2:]):
                    finding(warnings, 'NONLITERAL_ARGUMENT', loc, 'Relationship arguments must be literal for this profile.')
        elif macro not in DISPLAY:
            finding(warnings, 'UNSUPPORTED_MACRO', loc, 'Macro not checked: ' + macro)
    if pending or stack or started != 1 or ended != 1:
        finding(errors, 'INCOMPLETE_DIAGRAM', str(location), 'Expected one complete diagram with balanced calls/scopes.')
    if not included: finding(errors, 'C4_INCLUDE_REQUIRED', str(location), 'Matching C4 standard library include is required.')
    if not elements: finding(errors, 'EMPTY_VIEW', str(location), 'No modeled C4 elements were found.')
    for left, right, loc in relations:
        for endpoint in (left, right):
            if endpoint not in elements: finding(errors, 'UNKNOWN_ENDPOINT', loc, 'Undeclared endpoint: ' + endpoint)
    return {'errors': errors, 'warnings': warnings, 'elements': elements}


def load_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result: raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def assess(record, root):
    errors, blockers, warnings = [], [], []
    def error(code, loc, message): finding(errors, code, loc, message)
    def block(code, loc, message): finding(blockers, code, loc, message)
    def fields(obj, required, loc, optional=()):
        if not isinstance(obj, dict): error('OBJECT_REQUIRED', loc, 'Expected an object.'); return False
        if set(required) - obj.keys(): error('MISSING_FIELD', loc, 'Required fields: ' + ', '.join(sorted(set(required)-obj.keys())))
        if obj.keys() - set(required) - set(optional): error('UNKNOWN_FIELD', loc, 'Unknown fields are not accepted.')
        return True
    def text(obj, keys, loc):
        for key in keys:
            if not isinstance(obj.get(key), str) or not obj[key].strip(): error('TEXT_REQUIRED', loc+'.'+key, 'Expected nonempty text.')
    def choice(obj, key, values, loc):
        if not isinstance(obj.get(key), str) or obj[key] not in values: error('INVALID_VALUE',loc+'.'+key,'Expected '+', '.join(values))
    ids = set()
    def items(name, required, optional=()):
        values = record.get(name)
        if not isinstance(values, list): error('ARRAY_REQUIRED',name,'Expected an array.'); return {}
        result = {}
        for i, obj in enumerate(values):
            loc = name+'['+str(i)+']'
            if not fields(obj, ('id', *required), loc, optional): continue
            text(obj, ('id',), loc); key = obj.get('id')
            if not isinstance(key, str) or not key.strip(): continue
            if key in ids: error('DUPLICATE_ID',loc,'ID must be globally unique.'); continue
            ids.add(key); result[key] = obj
        return result
    def refs(obj, key, targets, loc):
        values = obj.get(key)
        if not isinstance(values, list) or any(not isinstance(v,str) or not v.strip() for v in values):
            error('REFERENCES_REQUIRED',loc+'.'+key,'Expected an array of IDs.'); return []
        if len(values) != len(set(values)): error('DUPLICATE_REFERENCE',loc,'Reference is repeated.')
        for value in values:
            if value not in targets: error('UNKNOWN_REFERENCE',loc,'Unknown ID: '+value)
        return [v for v in values if v in targets]
    required = ('schema_version','scope','required_levels','sources','requirements','quality_scenarios','decisions','views','handoff')
    if not fields(record, required, '$'): return outcome(errors,blockers,warnings)
    if type(record.get('schema_version')) is not int or record['schema_version'] != 1: error('SCHEMA_VERSION','$','Expected schema version 1.')
    text(record,('scope',),'$')
    levels = record.get('required_levels')
    if not isinstance(levels,list) or not levels or any(not isinstance(v,str) or v not in LEVELS for v in levels):
        error('LEVELS_REQUIRED','required_levels','Select nonempty supported view levels.'); levels=[]
    elif len(set(levels)) != len(levels): error('DUPLICATE_LEVEL','required_levels','Level repeated.')
    sources = items('sources',('reference',))
    requirements = items('requirements',('kind','text','source_ids','status'),('priority',))
    scenarios = items('quality_scenarios',('requirement_ids','context','stimulus','response','measure','verification'),('source_ids','priority','status'))
    decisions = items('decisions',('requirement_ids','view_ids','decision','rationale','tradeoffs','status'))
    views = items('views',('level','status','scope','reason'),('artifact',))
    for key,obj in sources.items(): text(obj,('reference',),key)
    if not sources or not requirements: block('INPUTS_REQUIRED','requirements','Record current requirement inputs and their sources.')
    for key,obj in requirements.items():
        text(obj,('text',),key); choice(obj,'kind',('functional','quality','constraint'),key); choice(obj,'status',('confirmed','open','proposed'),key)
        if not refs(obj,'source_ids',sources,key): block('SOURCE_REQUIRED',key,'Requirement needs a source.')
        if 'priority' in obj: text(obj,('priority',),key)
        if obj.get('status') != 'confirmed': block('REQUIREMENT_UNSETTLED',key,'Current design input is not confirmed.')
    quality_covered, decision_covered = set(), set()
    for key,obj in scenarios.items():
        text(obj,('context','stimulus','response','measure','verification'),key)
        if 'priority' in obj: text(obj,('priority',),key)
        if 'source_ids' in obj and not refs(obj,'source_ids',sources,key): block('SOURCE_REQUIRED',key,'Scenario source IDs must resolve.')
        if 'status' in obj:
            choice(obj,'status',('confirmed','open','proposed'),key)
            if obj.get('status') != 'confirmed': block('SCENARIO_UNSETTLED',key,'Quality scenario agreement is unresolved.')
        linked=refs(obj,'requirement_ids',requirements,key)
        if not linked: block('SCENARIO_INPUT_REQUIRED',key,'Link the quality requirements this scenario refines.')
        if any(requirements[r].get('kind')!='quality' for r in linked): error('QUALITY_REFERENCE_REQUIRED',key,'Scenarios reference quality requirements.')
        quality_covered.update(linked)
    for key,obj in decisions.items():
        text(obj,('decision','rationale','tradeoffs'),key); choice(obj,'status',('settled','proposed'),key)
        linked=refs(obj,'requirement_ids',requirements,key)
        if not linked: block('DECISION_INPUT_REQUIRED',key,'Link the inputs driving this decision.')
        decision_covered.update(linked)
        linked_views=refs(obj,'view_ids',views,key)
        if not linked_views: block('DECISION_VIEW_REQUIRED',key,'Link the architecture views affected by this decision.')
        if any(views[v].get('status')=='not_applicable' for v in linked_views): error('DECISION_VIEW_NOT_APPLICABLE',key,'A decision cannot claim an excluded view.')
        if obj.get('status')!='settled': block('DECISION_UNSETTLED',key,'Resolve or exclude the affected design scope.')
    for key,obj in requirements.items():
        if obj.get('kind')=='quality' and key not in quality_covered: block('QUALITY_SCENARIO_MISSING',key,'Quality input has no verification scenario.')
        if key not in decision_covered: block('DECISION_COVERAGE_MISSING',key,'No architectural response or retain decision linked.')
    usable, canonical = set(), {}
    for key,obj in views.items():
        choice(obj,'level',LEVELS,key);choice(obj,'status',('ready','draft','not_applicable'),key);text(obj,('scope','reason'),key)
        if obj.get('status')=='not_applicable':
            if 'artifact' in obj: error('NA_HAS_ARTIFACT',key,'Non-applicable view cannot claim an artifact.')
            continue
        if obj.get('status')!='ready': block('VIEW_UNREADY',key,'View is draft or needs revalidation.')
        if 'artifact' not in obj:
            block('VIEW_ARTIFACT_REQUIRED',key,'Current source is required.');continue
        value=obj['artifact']
        if not isinstance(value,str) or not value.strip(): error('ARTIFACT_PATH',key,'Expected a relative file path.');continue
        try:
            path=Path(value);resolved=(root/path).resolve()
            if path.is_absolute() or not resolved.is_relative_to(root): error('ARTIFACT_OUTSIDE_ROOT',key,'View must stay within project root.');continue
            if not resolved.is_file(): error('ARTIFACT_MISSING',key,'View source does not exist.');continue
            if obj.get('level') not in LEVELS: continue
            parsed=inspect(resolved.read_text(encoding='utf-8'),obj['level'],value)
        except (OSError,ValueError,RuntimeError) as exc:
            error('ARTIFACT_INPUT',key,str(exc));continue
        errors.extend(parsed['errors']);warnings.extend(parsed['warnings'])
        scope=obj.get('scope')
        if not isinstance(scope,str) or scope not in parsed['elements']: error('VIEW_SCOPE_MISSING',key,'Declared scope alias is absent from this view.')
        elif obj['level'] in ('container','component'):
            expected='system' if obj['level']=='container' else 'container'
            if parsed['elements'][scope]['kind']!=expected or not parsed['elements'][scope]['boundary']: error('VIEW_SCOPE_TYPE',key,'Expected the corresponding system/container boundary.')
            child='container' if obj['level']=='container' else 'component'
            for alias,entry in parsed['elements'].items():
                if entry['kind']==child and not entry['boundary'] and not entry['external']:
                    parent, visited = entry['parent'], set()
                    while parent and parent != scope and parent not in visited:
                        visited.add(parent)
                        owner = parsed['elements'].get(parent, {})
                        if owner.get('boundary') and owner.get('kind') == expected:
                            break  # A different nearest typed owner cannot be crossed.
                        parent = owner.get('parent')
                    if parent != scope:
                        error('OWNERSHIP_MISMATCH',key,'Internal element is not inside the declared scope: '+alias)
        for alias,entry in parsed['elements'].items():
            prior=canonical.get(alias)
            if prior and (prior['kind']!=entry['kind'] or prior['label']!=entry['label'] or (prior['technology'] and entry['technology'] and prior['technology']!=entry['technology'])):
                error('CROSS_VIEW_DRIFT',key,'Conflicting identity/name/technology for alias: '+alias)
            if not prior or not entry['boundary']: canonical[alias]=entry
        if obj.get('status')=='ready' and not parsed['errors'] and not parsed['warnings']: usable.add(obj['level'])
    for level in levels:
        if level not in usable: block('REQUIRED_VIEW_MISSING',level,'Required view has no ready checked source.')
    handoff=record.get('handoff')
    if fields(handoff,('status','consumer','notes'),'handoff'):
        choice(handoff,'status',('ready','draft'),'handoff');text(handoff,('consumer','notes'),'handoff')
        if handoff.get('status')!='ready': block('HANDOFF_UNREADY','handoff','Downstream input is not declared ready.')
    return outcome(errors,blockers,warnings)


def outcome(errors, blockers=None, warnings=None):
    blockers, warnings = blockers or [], warnings or []
    return {'structure_valid':not errors,'ready':not errors and not blockers and not warnings,
            'errors':errors,'blockers':blockers,'warnings':warnings,
            'coverage':{'profile':'partial' if warnings else 'checked',
                        'rendering':'not_run','architecture_semantics':'not_verified'}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('diagram',nargs='?',type=Path)
    parser.add_argument('--level',choices=LEVELS)
    parser.add_argument('--record',type=Path)
    parser.add_argument('--project-root',type=Path)
    parser.add_argument('--require-ready',action='store_true')
    args=parser.parse_args()
    if bool(args.diagram)==bool(args.record) or (args.diagram and not args.level) or (args.record and args.level):
        parser.error('Choose diagram --level LEVEL, or --record RECORD.')
    try:
        if args.record:
            root=(args.project_root or args.record.parent).resolve()
            if not root.is_dir(): raise ValueError('Project root is not a directory')
            result=assess(load_json(args.record),root)
        else:
            result=inspect(args.diagram.read_text(encoding='utf-8'),args.level,args.diagram)
            result=outcome(result['errors'],warnings=result['warnings'])
    except (OSError,ValueError,RuntimeError) as exc:
        print(json.dumps({'input_error':str(exc)},ensure_ascii=True),file=sys.stderr);return 2
    print(json.dumps(result,indent=2,ensure_ascii=True))
    return 0 if result['structure_valid'] and (not args.require_ready or result['ready']) else 1


if __name__=='__main__':
    raise SystemExit(main())
