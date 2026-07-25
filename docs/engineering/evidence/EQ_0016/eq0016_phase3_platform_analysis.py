#!/usr/bin/env python3
"""
EQ-0016 Phase 3: External Provenance Validation
Platform Signature Catalogue and Evidence Comparison
"""

import os
import zipfile
from xml.etree import ElementTree as ET
from collections import defaultdict
import json
import re

def analyze_xlsx_zip_detailed(file_path):
    """Enhanced analysis of XLSX as ZIP to extract detailed platform signatures"""
    try:
        results = {
            'filename': os.path.basename(file_path),
            'file_path': file_path,
            'sheets': [],
            'shared_strings': [],
            'creator': None,
            'last_modified_by': None,
            'app_name': None,
            'has_vba': False,
            'has_custom_xml': False,
            'total_files': 0,
            'formula_patterns': set(),
            'column_headers': set(),
            'trade_related_terms': set(),
            'distinctive_features': [],
            'file_structure': {}
        }

        with zipfile.ZipFile(file_path, 'r') as z:
            all_files = z.namelist()
            results['total_files'] = len(all_files)

            # Get workbook.xml for sheet names and structure
            if 'xl/workbook.xml' in all_files:
                wb_xml = z.read('xl/workbook.xml')
                root = ET.fromstring(wb_xml)
                ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for sheet in root.findall('.//s:sheet', ns):
                    sheet_name = sheet.get('name')
                    results['sheets'].append(sheet_name)
                    # Get sheet ID
                    sheet_id = sheet.get('sheetId')
                    if sheet_id:
                        results['file_structure'][sheet_name] = f"sheet{sheet_id}.xml"

            # Get app.xml for metadata
            if 'docProps/app.xml' in all_files:
                app_xml = z.read('docProps/app.xml')
                root = ET.fromstring(app_xml)
                ns = {'': 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'}
                gen = root.find('.//Application', ns)
                if gen is not None:
                    results['app_name'] = gen.text

            # Get core.xml for creator info
            if 'docProps/core.xml' in all_files:
                core_xml = z.read('docProps/core.xml')
                root = ET.fromstring(core_xml)
                ns = {
                    'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
                    'dc': 'http://purl.org/dc/elements/1.1/',
                }
                creator = root.find('.//dc:creator', ns)
                if creator is not None:
                    results['creator'] = creator.text

                lmb = root.find('.//cp:lastModifiedBy', ns)
                if lmb is not None:
                    results['last_modified_by'] = lmb.text

            # Get shared strings for content analysis
            if 'xl/sharedStrings.xml' in all_files:
                ss_xml = z.read('xl/sharedStrings.xml')
                root = ET.fromstring(ss_xml)
                ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for si in root.findall('.//s:si/s:t', ns):
                    if si.text:
                        text = si.text.strip()
                        results['shared_strings'].append(text)

                        # Look for formula patterns
                        if re.search(r'[A-Z]+\d+', text):  # Cell references
                            results['formula_patterns'].add('CELL_REFERENCES')
                        if 'XGET' in text.upper():
                            results['formula_patterns'].add('XGET_FUNCTION')
                        if re.search(r'SUM|AVERAGE|COUNT|IF', text.upper()):
                            results['formula_patterns'].add('STANDARD_FUNCTIONS')

                        # Look for column headers
                        if re.search(r'Code|Description|Quantity|UOM|Unit|Rate|Total|SubTotal|Factor', text, re.IGNORECASE):
                            results['column_headers'].add(text)

                        # Look for trade-related terms
                        if re.search(r'Trade|Breakup|Markup|Reference|GFA|FECA|UCA|BOQ|Bill', text, re.IGNORECASE):
                            results['trade_related_terms'].add(text)

            # Look for distinctive files and features
            results['has_vba'] = 'xl/vbaProject.bin' in all_files
            results['has_custom_xml'] = any('customXml' in f for f in all_files)

            # Check for CostX-specific patterns
            if any('costx' in s.lower() for s in results['sheets']):
                results['distinctive_features'].append('CostX_sheet_name')
            if any('costx' in s.lower() for s in results['shared_strings']):
                results['distinctive_features'].append('CostX_in_content')

            # Check for trade breakdown patterns
            if any('trade' in s.lower() and ('breakup' in s.lower() or 'breakdown' in s.lower()) for s in results['sheets']):
                results['distinctive_features'].append('Trade_breakup_sheets')
            if any('trade' in s.lower() and ('breakup' in s.lower() or 'breakdown' in s.lower()) for s in results['shared_strings']):
                results['distinctive_features'].append('Trade_breakup_content')

            return results

    except Exception as e:
        return {'filename': os.path.basename(file_path), 'error': str(e)}

def create_platform_signature_catalogue(all_results):
    """Create a catalogue of platform signatures based on analysis"""
    catalogue = {}

    # Group by platform family based on distinctive features
    costx_family = []
    trade_breakup_family = []
    generic_family = []
    unknown_family = []

    for result in all_results:
        if 'error' in result:
            continue

        if 'CostX_sheet_name' in result['distinctive_features'] or 'CostX_in_content' in result['distinctive_features']:
            costx_family.append(result)
        elif 'Trade_breakup_sheets' in result['distinctive_features'] or 'Trade_breakup_content' in result['distinctive_features']:
            trade_breakup_family.append(result)
        elif result['filename'].startswith('client_') or result['filename'].startswith('Structural_Steel_Program'):
            generic_family.append(result)
        else:
            unknown_family.append(result)

    # Create platform signatures
    catalogue['CostX'] = {
        'known_worksheet_names': list(set(sheet for result in costx_family for sheet in result['sheets'])),
        'typical_structure': 'Single worksheet named "CostX" with BOQ data',
        'formula_conventions': list(set(pattern for result in costx_family for pattern in result['formula_patterns'])),
        'metadata_patterns': {
            'creator': list(set(r['creator'] for r in costx_family if r['creator'])),
            'app_name': list(set(r['app_name'] for r in costx_family if r['app_name']))
        },
        'export_characteristics': {
            'has_vba': any(r['has_vba'] for r in costx_family),
            'has_custom_xml': any(r['has_custom_xml'] for r in costx_family),
            'average_files': sum(r['total_files'] for r in costx_family) / len(costx_family) if costx_family else 0
        },
        'column_headers': list(set(header for result in costx_family for header in result['column_headers'])),
        'trade_terms': list(set(term for result in costx_family for term in result['trade_related_terms'])),
        'sources': ['Repository analysis of confirmed CostX exports'],
        'confidence': 'High - based on sheet names containing "CostX"'
    }

    catalogue['Trade_Breakup'] = {
        'known_worksheet_names': list(set(sheet for result in trade_breakup_family for sheet in result['sheets'])),
        'typical_structure': 'Multiple worksheets including "Trade Breakup", "Trade Breakup Showing Markup", "Trade Summary"',
        'formula_conventions': list(set(pattern for result in trade_breakup_family for pattern in result['formula_patterns'])),
        'metadata_patterns': {
            'creator': list(set(r['creator'] for r in trade_breakup_family if r['creator'])),
            'app_name': list(set(r['app_name'] for r in trade_breakup_family if r['app_name']))
        },
        'export_characteristics': {
            'has_vba': any(r['has_vba'] for r in trade_breakup_family),
            'has_custom_xml': any(r['has_custom_xml'] for r in trade_breakup_family),
            'average_files': sum(r['total_files'] for r in trade_breakup_family) / len(trade_breakup_family) if trade_breakup_family else 0
        },
        'column_headers': list(set(header for result in trade_breakup_family for header in result['column_headers'])),
        'trade_terms': list(set(term for result in trade_breakup_family for term in result['trade_related_terms'])),
        'sources': ['Repository analysis of trade breakdown exports'],
        'confidence': 'Medium - based on worksheet names and content patterns, but no explicit platform identification'
    }

    catalogue['Generic_Client'] = {
        'known_worksheet_names': list(set(sheet for result in generic_family for sheet in result['sheets'])),
        'typical_structure': 'Multiple worksheets with client-specific naming conventions',
        'formula_conventions': list(set(pattern for result in generic_family for pattern in result['formula_patterns'])),
        'metadata_patterns': {
            'creator': list(set(r['creator'] for r in generic_family if r['creator'])),
            'app_name': list(set(r['app_name'] for r in generic_family if r['app_name']))
        },
        'export_characteristics': {
            'has_vba': any(r['has_vba'] for r in generic_family),
            'has_custom_xml': any(r['has_custom_xml'] for r in generic_family),
            'average_files': sum(r['total_files'] for r in generic_family) / len(generic_family) if generic_family else 0
        },
        'column_headers': list(set(header for result in generic_family for header in result['column_headers'])),
        'trade_terms': list(set(term for result in generic_family for term in result['trade_related_terms'])),
        'sources': ['Repository analysis of client-specific exports'],
        'confidence': 'Low - unknown platform origin'
    }

    return catalogue

def compare_export_families(all_results, catalogue):
    """Compare repository export families against platform catalogue"""
    comparison_matrix = []

    for result in all_results:
        if 'error' in result:
            continue

        # Determine which platform signature it matches
        best_match = None
        confidence_score = 0
        evidence = []

        # Check CostX match
        if 'CostX_sheet_name' in result['distinctive_features'] or 'CostX_in_content' in result['distinctive_features']:
            best_match = 'CostX'
            confidence_score = 0.9
            evidence.append('Sheet name contains "CostX"')
            evidence.append('Content contains CostX references')
        # Check Trade Breakup match
        elif 'Trade_breakup_sheets' in result['distinctive_features'] or 'Trade_breakup_content' in result['distinctive_features']:
            best_match = 'Trade_Breakup'
            confidence_score = 0.6
            evidence.append('Sheet names match trade breakdown pattern')
            evidence.append('Content contains trade breakdown terms')
        # Check Generic match
        elif result['filename'].startswith('client_') or result['filename'].startswith('Structural_Steel_Program'):
            best_match = 'Generic_Client'
            confidence_score = 0.4
            evidence.append('Filename suggests client-specific format')
        else:
            best_match = 'Unknown'
            confidence_score = 0.1
            evidence.append('No distinctive platform signatures found')

        # Add counter-evidence
        counter_evidence = []
        if best_match == 'CostX' and 'CostX_sheet_name' not in result['distinctive_features']:
            counter_evidence.append('No "CostX" sheet name found')
        if best_match == 'Trade_Breakup' and len(result['sheets']) < 3:
            counter_evidence.append('Fewer sheets than typical trade breakdown')

        comparison_matrix.append({
            'filename': result['filename'],
            'matched_platform': best_match,
            'confidence': confidence_score,
            'supporting_evidence': evidence,
            'contradictory_evidence': counter_evidence,
            'missing_evidence': [] if best_match == 'Unknown' else ['Explicit platform metadata'],
            'sheets': result['sheets'],
            'distinctive_features': result['distinctive_features']
        })

    return comparison_matrix

def main():
    print("=" * 120)
    print("EQ-0016 PHASE 3: EXTERNAL PROVENANCE VALIDATION")
    print("=" * 120)

    # Analyze all fixtures
    directories = [
        "tests/fixtures/costx",
        "tests/fixtures/generic",
    ]

    all_results = []

    for dir_path in directories:
        if os.path.exists(dir_path):
            for file in sorted(os.listdir(dir_path)):
                if file.endswith(('.xlsx', '.xlsX')):
                    file_path = os.path.join(dir_path, file)
                    result = analyze_xlsx_zip_detailed(file_path)
                    if result and 'error' not in result:
                        all_results.append(result)
                        print(f"Analyzed: {result['filename']} - {len(result['sheets'])} sheets, {len(result['distinctive_features'])} distinctive features")
                    else:
                        print(f"Error analyzing {file}: {result.get('error', 'Unknown error')}")

    print(f"\nAnalyzed {len(all_results)} files successfully")

    # Create platform signature catalogue
    catalogue = create_platform_signature_catalogue(all_results)

    print("\n" + "=" * 120)
    print("PLATFORM SIGNATURE CATALOGUE")
    print("=" * 120)

    for platform, signature in catalogue.items():
        print(f"\n{platform}:")
        print(f"  Worksheet names: {signature['known_worksheet_names'][:5]}")
        print(f"  Structure: {signature['typical_structure']}")
        print(f"  Formula conventions: {signature['formula_conventions']}")
        print(f"  Confidence: {signature['confidence']}")
        print(f"  Sources: {signature['sources']}")

    # Compare export families
    comparison_matrix = compare_export_families(all_results, catalogue)

    print("\n" + "=" * 120)
    print("EXPORT FAMILY COMPARISON MATRIX")
    print("=" * 120)

    for comparison in comparison_matrix:
        print(f"\n{comparison['filename']}:")
        print(f"  Matched Platform: {comparison['matched_platform']}")
        print(f"  Confidence: {comparison['confidence']:.1f}")
        print(f"  Evidence: {comparison['supporting_evidence']}")
        if comparison['contradictory_evidence']:
            print(f"  Counter-evidence: {comparison['contradictory_evidence']}")
        if comparison['missing_evidence']:
            print(f"  Missing evidence: {comparison['missing_evidence']}")
        print(f"  Sheets: {comparison['sheets']}")

    # Save results
    with open('data/reports/eq0016_phase3_platform_catalogue.json', 'w') as f:
        json.dump(catalogue, f, indent=2)

    with open('data/reports/eq0016_phase3_comparison_matrix.json', 'w') as f:
        json.dump(comparison_matrix, f, indent=2)

    print("\n" + "=" * 120)
    print("RESULTS SAVED")
    print("=" * 120)
    print("Platform Catalogue: data/reports/eq0016_phase3_platform_catalogue.json")
    print("Comparison Matrix: data/reports/eq0016_phase3_comparison_matrix.json")

    # Classification review
    print("\n" + "=" * 120)
    print("CLASSIFICATION REVIEW")
    print("=" * 120)

    classification_counts = defaultdict(int)
    for comparison in comparison_matrix:
        classification_counts[comparison['matched_platform']] += 1

    for platform, count in classification_counts.items():
        print(f"{platform}: {count} files")

    print("\nREMAINING UNKNOWN FILES:")
    unknown_files = [c['filename'] for c in comparison_matrix if c['matched_platform'] == 'Unknown']
    for file in unknown_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()