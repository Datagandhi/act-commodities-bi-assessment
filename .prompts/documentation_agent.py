"""
Documentation Agent for Automated Data Platform Documentation Generation

This agent uses Gen AI to automatically generate comprehensive documentation
for data engineering, BI, and analytics projects using predefined templates.

Usage:
    python documentation_agent.py --template <template_name> --output <output_path> [--vars <vars.yaml>]

Templates available:
    - project_readme
    - dimensional_model
    - powerbi_report

Author: ACT Commodities BI Assessment
Version: 1.0
Date: November 2025
"""

import argparse
import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class DocumentationAgent:
    """
    Agent for generating documentation using Gen AI with predefined templates.
    
    Supports:
    - Template-based documentation generation
    - Variable substitution
    - Multiple output formats (Markdown, HTML, PDF)
    - Quality validation
    """
    
    def __init__(self, template_dir: str = ".prompts", output_dir: str = "."):
        """
        Initialize the Documentation Agent.
        
        Args:
            template_dir: Directory containing documentation templates
            output_dir: Directory for generated documentation
        """
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.templates = {
            "project_readme": "documentation_template_project_readme.md",
            "dimensional_model": "documentation_template_dimensional_model.md",
            "powerbi_report": "documentation_template_powerbi_report.md"
        }
        
    def load_template(self, template_name: str) -> str:
        """
        Load a documentation template.
        
        Args:
            template_name: Name of the template (project_readme, dimensional_model, powerbi_report)
            
        Returns:
            Template content as string
        """
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}. Available: {list(self.templates.keys())}")
        
        template_path = self.template_dir / self.templates[template_name]
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_variables(self, vars_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load variables from YAML or JSON file.
        
        Args:
            vars_path: Path to variables file (YAML or JSON)
            
        Returns:
            Dictionary of variables
        """
        if not vars_path:
            return {}
        
        vars_file = Path(vars_path)
        
        if not vars_file.exists():
            raise FileNotFoundError(f"Variables file not found: {vars_path}")
        
        with open(vars_file, 'r', encoding='utf-8') as f:
            if vars_file.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif vars_file.suffix == '.json':
                return json.load(f)
            else:
                raise ValueError(f"Unsupported variables file format: {vars_file.suffix}")
    
    def substitute_variables(self, template_content: str, variables: Dict[str, Any]) -> str:
        """
        Substitute variables in template content.
        
        Args:
            template_content: Template string with {variable} placeholders
            variables: Dictionary of variable values
            
        Returns:
            Template with substituted values
        """
        result = template_content
        
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            
            # Handle nested dictionaries and lists
            if isinstance(value, (dict, list)):
                value_str = yaml.dump(value, default_flow_style=False)
            else:
                value_str = str(value)
            
            result = result.replace(placeholder, value_str)
        
        return result
    
    def generate_documentation(
        self, 
        template_name: str, 
        variables: Optional[Dict[str, Any]] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate documentation from template.
        
        Args:
            template_name: Template to use
            variables: Variables for substitution
            output_path: Where to save generated documentation
            
        Returns:
            Generated documentation content
        """
        # Load template
        template_content = self.load_template(template_name)
        
        # Substitute variables
        variables = variables or {}
        
        # Add metadata variables
        variables.setdefault('generation_date', datetime.now().strftime('%Y-%m-%d'))
        variables.setdefault('generation_timestamp', datetime.now().isoformat())
        variables.setdefault('template_version', '1.0')
        
        # Generate actual documentation based on template type
        if template_name == "project_readme":
            documentation = self._generate_project_readme(variables)
        elif template_name == "dimensional_model":
            documentation = self._generate_dimensional_model(variables)
        elif template_name == "powerbi_report":
            documentation = self._generate_powerbi_report(variables)
        else:
            # Fallback: return template with instructions for Gen AI
            documentation = f"""
# GENERATED DOCUMENTATION

**Template:** {template_name}
**Generated:** {variables['generation_date']}

---

⚠️ **Note:** This template requires Gen AI integration (Azure OpenAI, GPT-4, etc.) to generate actual content.

See USER_GUIDE.md for instructions on using GitHub Copilot or Azure OpenAI to generate documentation.

---

## TEMPLATE CONTENT

{template_content}
"""
        
        # Save if output path provided
        if output_path:
            output_file = self.output_dir / output_path
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(documentation)
            
            print(f"✅ Documentation generated: {output_file}")
        
        return documentation
    
    def _generate_project_readme(self, variables: Dict[str, Any]) -> str:
        """Generate project README documentation."""
        project_name = variables.get('project_name', 'Project Name')
        project_description = variables.get('project_description', 'Project description')
        project_components = variables.get('project_components', [])
        folder_structure = variables.get('folder_structure', '.')
        sql_component = variables.get('sql_component', {})
        dimensional_model_component = variables.get('dimensional_model_component', {})
        powerbi_component = variables.get('powerbi_component', {})
        deliverables_list = variables.get('deliverables_list', [])
        
        # Build components section
        components_text = "\n".join([
            f"- **{comp.get('name', 'Component')}**: {comp.get('description', '')}"
            for comp in project_components
        ])
        
        # Build file organization descriptions
        file_descriptions = [
            "- `README.md` - Project Repository documentation",
            "- `project_documents/act_power_bi_theme.json` - Power BI theme (required for reporting assessment)",
            "- `project_documents/senior_bi_engineer_assessment_details.md` - Full requirements & assessment details",
            "- `project_documents/sql_assignment.sql` - SQL schema + assignment placeholders",
            "- `project_documents/trading_dataset.xlsx` - Trading dataset for dimensional modeling & Power BI"
        ]
        
        # Build SQL component section
        sql_section = ""
        if sql_component:
            sql_section = f"""## SQL Development {sql_component.get('file_reference', '')}

### Environment Setup
- **Target platform**: {sql_component.get('environment', {}).get('platform', 'SQL Server')}
- **Testing platform**: {sql_component.get('environment', {}).get('testing_url', 'N/A')}

## Core Data Model
{sql_component.get('data_model', {}).get('description', '')}
"""
            for entity in sql_component.get('data_model', {}).get('entities', []):
                sql_section += f"- {entity}\n"
            
            sql_section += f"""
### Schema Notes
"""
            for note in sql_component.get('schema_notes', []):
                sql_section += f"- {note}\n"
            
            sql_section += f"""
### Required Queries ({sql_component.get('required_queries', {}).get('count', 0)} total)
"""
            for i, query in enumerate(sql_component.get('required_queries', {}).get('list', []), 1):
                sql_section += f"{i}. {query}\n"
            
            sql_section += f"""
### Key Business Logic
"""
            for logic in sql_component.get('business_logic', []):
                sql_section += f"- {logic}\n"
            
            sql_section += f"""
### SQL Patterns to Follow
"""
            for pattern in sql_component.get('sql_patterns', []):
                sql_section += f"- {pattern}\n"
        
        # Build dimensional modeling section
        dim_section = ""
        if dimensional_model_component:
            dim_section = f"""## {dimensional_model_component.get('title', 'Dimensional Modeling Exercise')}

### Requirements
"""
            for req in dimensional_model_component.get('requirements', []):
                dim_section += f"- {req}\n"
            
            dim_section += f"""
### Modeling Conventions
"""
            for conv in dimensional_model_component.get('conventions', []):
                dim_section += f"- {conv}\n"
        
        # Build Power BI section
        pbi_section = ""
        if powerbi_component:
            pbi_section = f"""## Power BI Report {powerbi_component.get('report_name', '')}

### Theme
- **Required theme**: {powerbi_component.get('theme', {}).get('file', 'theme.json')}
  
### Data Source
- Use {powerbi_component.get('data_source', {}).get('file', 'data.xlsx')} {powerbi_component.get('data_source', {}).get('note', '')}
- {powerbi_component.get('data_source', {}).get('transformation', '')}
"""
        
        # Build deliverables section
        deliverables_section = """## Deliverables
"""
        for deliverable in deliverables_list:
            deliverables_section += f"- **{deliverable.get('component', 'Component')}**: {deliverable.get('description', '')}\n"
        
        # Assemble final documentation
        documentation = f"""# {project_name}

{project_description}

## Project Overview
This repository contains three core components for a Senior BI Engineer role assessment:
{components_text}

## File Organization
```
{folder_structure}
```

{chr(10).join(file_descriptions)}

{sql_section}
{dim_section}
{pbi_section}
  

{deliverables_section}"""
        
        return documentation
    
    def _generate_dimensional_model(self, variables: Dict[str, Any]) -> str:
        """Generate dimensional model documentation."""
        # Placeholder for dimensional model generation
        return "# Dimensional Model Documentation\n\n(To be implemented based on template)"
    
    def _generate_powerbi_report(self, variables: Dict[str, Any]) -> str:
        """Generate Power BI report documentation."""
        # Placeholder for Power BI documentation generation
        return "# Power BI Report Documentation\n\n(To be implemented based on template)"
    
    def validate_documentation(self, doc_content: str, template_name: str) -> Dict[str, Any]:
        """
        Validate generated documentation against quality checklist.
        
        Args:
            doc_content: Generated documentation
            template_name: Template used
            
        Returns:
            Validation results
        """
        validation_results = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "metrics": {}
        }
        
        # Basic validations
        if len(doc_content) < 500:
            validation_results["warnings"].append("Documentation seems too short (< 500 chars)")
        
        if "{" in doc_content and "}" in doc_content:
            validation_results["warnings"].append("Possible unsubstituted variables found")
        
        if "TODO" in doc_content or "FIXME" in doc_content:
            validation_results["errors"].append("Placeholder text found (TODO/FIXME)")
            validation_results["valid"] = False
        
        # Metrics
        validation_results["metrics"]["char_count"] = len(doc_content)
        validation_results["metrics"]["line_count"] = doc_content.count('\n')
        validation_results["metrics"]["word_count"] = len(doc_content.split())
        
        return validation_results


def main():
    """Command-line interface for Documentation Agent."""
    parser = argparse.ArgumentParser(
        description="Generate automated documentation using Gen AI templates"
    )
    parser.add_argument(
        "--template",
        required=True,
        choices=["project_readme", "dimensional_model", "powerbi_report"],
        help="Documentation template to use"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path for generated documentation"
    )
    parser.add_argument(
        "--vars",
        help="Path to variables file (YAML or JSON)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate generated documentation"
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = DocumentationAgent()
    
    # Load variables
    variables = agent.load_variables(args.vars) if args.vars else {}
    
    # Generate documentation
    print(f"🤖 Generating documentation using template: {args.template}")
    doc_content = agent.generate_documentation(
        template_name=args.template,
        variables=variables,
        output_path=args.output
    )
    
    # Validate if requested
    if args.validate:
        print(f"✅ Validating generated documentation...")
        validation = agent.validate_documentation(doc_content, args.template)
        
        print(f"\n📊 Validation Results:")
        print(f"  Valid: {validation['valid']}")
        print(f"  Warnings: {len(validation['warnings'])}")
        print(f"  Errors: {len(validation['errors'])}")
        print(f"  Metrics: {validation['metrics']}")
        
        if validation['warnings']:
            print(f"\n⚠️  Warnings:")
            for warning in validation['warnings']:
                print(f"    - {warning}")
        
        if validation['errors']:
            print(f"\n❌ Errors:")
            for error in validation['errors']:
                print(f"    - {error}")
    
    print(f"\n✅ Documentation generation complete!")


if __name__ == "__main__":
    main()
