#!/usr/bin/env python3
"""
EQ-0016 Phase 2: Deeper analysis using subprocess to compare workbook families
with confirmed CostX exports.
"""

import os
import sys
import zipfile
from xml.etree import ElementTree as ET
from collections import defaultdict

def analyze_xlsx_zip(file_path):
    """Analyze XLSX as ZIP to extract metadata without openpyxl compatibility issues"""
    try:
        results = {
            'filename': os.path.basename(file_path),
            'sheets': [],
            'shared_strings_samples': [],
            'creator': None,
            'last_modified_by': None,
            'created': None,
            'modified': None,
            'app_name': None,
        }
        
        with zipfile.ZipFile(file_path, 'r') as z:
            # List all files in the archive
            all_files = z.namelist()
            results['all_files'] = all_files
            
            # Get workbook.xml for sheet names
            if 'xl/workbook.xml' in all_files:
                wb_xml = z.read('xl/workbook.xml')
                root = ET.fromstring(wb_xml)
                ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
                      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
                for sheet in root.findall('.//s:sheet', ns):
                    results['sheets'].append(sheet.get('name'))
            
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
                
                # Try lastModifiedBy
                lmb = root.find('.//cp:lastModifiedBy', ns)
                if lmb is not None:
                    results['last_modified_by'] = lmb.text
            
            # Get shared strings for sample of text content
            if 'xl/sharedStrings.xml' in all_files:
                ss_xml = z.read('xl/sharedStrings.xml')
                root = ET.fromstring(ss_xml)
                ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for i, si in enumerate(root.findall('.//s:si/s:t', ns)):
                    if i < 20:  # First 20 strings
                        results['shared_strings_samples'].append(si.text[:100] if si.text else '')
                        if len(results['shared_strings_samples']) >= 10:
                            break
            
            # Look for custom XML or VBA
            results['has_vba'] = 'xl/vbaProject.bin' in all_files
            results['has_custom_xml'] = any('customXml' in f for f in all_files)
            
            return results
            
    except Exception as e:
        return {'filename': os.path.basename(file_path), 'error': str(e)}

def main():
    print("=" * 100)
    print("EQ-0016 PHASE 2: PLATFORM PROVENANCE INVESTIGATION (ZIP-level analysis)")
    print("=" * 100)
    
    directories = [
        ("costx", "tests/fixtures/costx"),
        ("generic", "tests/fixtures/generic"),
    ]
    
    all_results = []
    
    for dir_name, dir_path in directories:
        for file in sorted(os.listdir(dir_path)):
            if file.endswith(('.xlsx', '.xlsX')):
                file_path = os.path.join(dir_path, file)
                result = analyze_xlsx_zip(file_path)
                if result and 'error' not in result:
                    all_results.append(result)
                    print(f"\n{'='*60}")
                    print(f"File: {result['filename']}")
                    print(f"{'='*60}")
                    print(f"  Application: {result['app_name']}")
                    print(f"  Creator: {result['creator']}")
                    print(f"  Last Modified By: {result.get('last_modified_by')}")
                    print(f"  Sheets ({len(result['sheets'])}): {result['sheets'][:8]}")
                    print(f"  Has VBA: {result['has_vba']}")
                    print(f"  Has Custom XML: {result['has_custom_xml']}")
                    
                    # Look for XGET formulas in shared strings
                    xget_found = [s for s in result['shared_strings_samples'] if 'xget' in (s or '').lower()]
                    if xget_found:
                        print(f"  XGET formulas found: {len(xget_found)}")
                    
                    # Show trade-related samples
                    trade_samples = [s for s in result['shared_strings_samples'] if any(
                        term in (s or '').lower() for term in ['trade', 'breakup', 'markup', 'reference']
                    )]
                    if trade_samples:
                        print(f"  Trade-related samples: {trade_samples[:5]}")
                    
                    # Show first 10 shared strings
                    print(f"  Sample strings: {result['shared_strings_samples'][:10]}")
                    
                    # Check for distinctive files
                    files_set = set(result['all_files'])
                    print(f"  Total files in archive: {len(result['all_files'])}")
                    if result['has_vba']:
                        print(f"  ⚠️ Contains VBA macros!")
                    if result['has_custom_xml']:
                        print(f"  ⚠️ Contains custom XML!")
                else:
                    print(f"\n{file}: Error - {result.get('error', 'Unknown error')}")
    
    # Group by application name
    print("\n" + "=" * 100)
    print("APPLICATION-BASED GROUPING")
    print("=" * 100)
    
    app_groups = defaultdict(list)
    for r in all_results:
        app = r.get('app_name') or r.get('creator') or 'Unknown'
        app_groups[app].append(r['filename'])
    
    for app, members in sorted(app_groups.items()):
        print(f"\n{app}:")
        for m in members:
            print(f"  - {m}")
    
    # Group Confirmed CostX exports
    print("\n" + "=" * 100)
    print("CONFIRMED COSTX EXPORTS (Sheet name contains 'CostX')")
    print("=" * 100)
    
    for r in all_results:
        for sheet in r['sheets']:
            if 'costx' in sheet.lower():
                print(f"\n  Confirmed CostX: {r['filename']}")
                print(f"    Application: {r.get('app_name')}")
                print(f"    Creator: {r.get('creator')}")
                print(f"    Sheets: {r['sheets']}")
                break
    
    # Compare Family 2 (Trade Breakup) against confirmed
    print("\n" + "=" * 100)
    print("FAMILY 2 (Trade Breakup) vs CONFIRMED COSTX")
    print("=" * 100)
    
    family2_files = ['full_boq_2.xlsx', 'full_boq_5.xlsx', 'full_boq_6.xlsx']
    confirmed_costx = ['full_boq.xlsx', 'full_boq_corrected.xlsx']
    
    print("\nConfidence Assessment:")
    for r in all_results:
        if r['filename'] in family2_files:
            print(f"\n{r['filename']}:")
            print(f"  Application: {r.get('app_name', 'Unknown')}")
            print(f"  Creator: {r.get('creator', 'Unknown')}")
            print(f"  Sheets: {r['sheets']}")
            print(f"  Status: Unknown - no platform signatures found")
        
        if r['filename'] in confirmed_costx:
            print(f"\n{r['filename']}:")
            print(f"  Application: {r.get('app_name', 'Unknown')}")
            print(f"  Creator: {r.get('creator', 'Unknown')}")
            print(f"  Sheets: {r['sheets']}")
            
            # Check if CostX is in any metadata
            has_costx = False
            for val in [r.get('app_name', ''), r.get('creator', '')]:
                if val and 'costx' in val.lower():
                    has_costx = True
                    print(f"  ✅ CostX confirmed via metadata: {val}")
            for sheet in r['sheets']:
                if 'costx' in sheet.lower():
                    has_costx = True
                    print(f"  ✅ CostX confirmed via sheet name: {sheet}")
            if not has_costx:
                print(f"  Status: No explicit CostX metadata found in ZIP analysis")

if __name__ == "__main__":
    main()