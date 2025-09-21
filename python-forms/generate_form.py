#!/usr/bin/env python3
"""
🏥 LocumTele Form Generator - User-Friendly JSON to HTML Converter

Convert any JSON form to a complete HTML medical form with one command.

Usage:
    python3 generate_form.py --form surveys/weightloss/GLP1-screener.json
    python3 generate_form.py --category weightloss --form-name GLP1
    python3 generate_form.py --interactive
    python3 generate_form.py --list-forms
    python3 generate_form.py --batch-all
"""

import argparse
import json
import os
import sys
from pathlib import Path
from enhanced_form_generator import EnhancedFormGenerator
from form_data_loader import FormDataLoader

def print_banner():
    """Print welcome banner"""
    print("🏥" + "="*60)
    print("   LocumTele Medical Form Generator")
    print("   Convert JSON forms to production-ready HTML")
    print("="*62)

def list_available_forms():
    """List all available JSON forms"""
    print("\n📋 Available Forms:")
    surveys_dir = Path("../surveys")

    # List category-specific forms
    for category_dir in surveys_dir.iterdir():
        if category_dir.is_dir() and category_dir.name != "all-forms":
            print(f"\n📁 {category_dir.name.title()}:")
            for json_file in category_dir.glob("*.json"):
                form_name = json_file.stem.replace("-screener", "")
                print(f"   • {form_name} ({json_file.name})")

    # List shared sections
    all_forms_dir = surveys_dir / "all-forms"
    if all_forms_dir.exists():
        print(f"\n📁 Shared Sections:")
        for json_file in all_forms_dir.glob("*.json"):
            print(f"   • {json_file.stem}")

def validate_json_structure(json_data, file_path):
    """Validate JSON structure for form generation"""
    print(f"🔍 Validating {file_path}...")

    required_fields = ["property_category"]
    optional_fields = ["name", "property_form_type", "property_consult_type", "questions"]

    issues = []

    # Check required fields
    for field in required_fields:
        if field not in json_data:
            issues.append(f"Missing required field: {field}")

    # Check if it has questions (either directly or sub_items)
    if "questions" not in json_data and "property_sub_item" not in json_data:
        issues.append("No questions found - need either 'questions' array or 'property_sub_item' references")

    # Check category validity
    if "property_category" in json_data:
        category = json_data["property_category"]
        if not isinstance(category, str) or not category:
            issues.append("property_category must be a non-empty string")

    if issues:
        print("❌ Validation failed:")
        for issue in issues:
            print(f"   • {issue}")
        return False

    print("✅ JSON structure valid")
    return True

def extract_form_info(json_file_path):
    """Extract form info from JSON file"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract basic info
        form_name = data.get("name", Path(json_file_path).stem.replace("-screener", ""))
        category = data.get("property_category", "")
        consult_type = data.get("property_consult_type", "async")

        return {
            "name": form_name,
            "category": category,
            "consult_type": consult_type,
            "data": data
        }
    except Exception as e:
        print(f"❌ Error reading {json_file_path}: {e}")
        return None

def generate_single_form(json_file_path, output_dir=None):
    """Generate HTML form from a single JSON file"""
    print(f"\n🔧 Processing: {json_file_path}")

    # Read and validate JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return False

    if not validate_json_structure(json_data, json_file_path):
        return False

    # Extract form information
    form_info = extract_form_info(json_file_path)
    if not form_info:
        return False

    print(f"📋 Form: {form_info['name']}")
    print(f"📁 Category: {form_info['category']}")
    print(f"💬 Consult Type: {form_info['consult_type']}")

    try:
        # Load complete form data
        loader = FormDataLoader()
        form_data = loader.generate_complete_form_data(
            form_info['category'],
            form_info['name'],
            form_info['consult_type']
        )

        if not form_data or not form_data.get("sections"):
            print("❌ Error: No form data could be loaded!")
            return False

        print(f"✅ Loaded {len(form_data['sections'])} sections:")
        total_questions = 0
        for section_name, questions in form_data['sections'].items():
            count = len(questions)
            total_questions += count
            print(f"   📋 {section_name}: {count} questions")

        # Generate HTML
        print(f"\n🔧 Generating HTML form...")
        generator = EnhancedFormGenerator()
        html = generator.generate_notion_form(form_data)

        # Determine output path
        if output_dir:
            output_path = Path(output_dir)
        else:
            # Use same directory as input file
            output_path = Path(json_file_path).parent

        output_path.mkdir(parents=True, exist_ok=True)

        # Create filename
        filename = f"{form_info['name']}-screener-live.html"
        full_path = output_path / filename

        # Write HTML file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\n✅ Form generated successfully!")
        print(f"📄 Saved as: {full_path}")
        print(f"📊 Total Questions: {total_questions}")
        print(f"🌐 Open {full_path} in your browser to test")

        return True

    except Exception as e:
        print(f"❌ Error generating form: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_by_category_and_name(category, form_name, consult_type="async"):
    """Generate form using category and form name"""
    print(f"\n🔧 Generating form: {form_name} ({category})")

    try:
        # Load complete form data
        loader = FormDataLoader()
        form_data = loader.generate_complete_form_data(category, form_name, consult_type)

        if not form_data or not form_data.get("sections"):
            print("❌ Error: No form data could be loaded!")
            print("💡 Check that JSON files exist in:")
            print(f"   • ../surveys/{category.lower()}/{form_name}-screener.json")
            print(f"   • ../surveys/all-forms/ (shared sections)")
            return False

        print(f"✅ Loaded {len(form_data['sections'])} sections:")
        total_questions = 0
        for section_name, questions in form_data['sections'].items():
            count = len(questions)
            total_questions += count
            print(f"   📋 {section_name}: {count} questions")

        # Generate HTML
        print(f"\n🔧 Generating HTML form...")
        generator = EnhancedFormGenerator()
        html = generator.generate_notion_form(form_data)

        # Create output path
        output_dir = Path(f"../surveys/{category.lower()}")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{form_name}-screener-live.html"
        full_path = output_dir / filename

        # Write HTML file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\n✅ Form generated successfully!")
        print(f"📄 Saved as: {full_path}")
        print(f"📊 Total Questions: {total_questions}")
        print(f"🌐 Open {full_path} in your browser to test")

        return True

    except Exception as e:
        print(f"❌ Error generating form: {e}")
        import traceback
        traceback.print_exc()
        return False

def interactive_mode():
    """Interactive form generation"""
    print("\n🎯 Interactive Form Generator")
    print("Choose an option:")
    print("1. Generate from existing JSON file")
    print("2. Generate by category and form name")
    print("3. List available forms")
    print("4. Exit")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        print("\n📁 Enter the path to your JSON file:")
        json_path = input("Path: ").strip()
        if os.path.exists(json_path):
            generate_single_form(json_path)
        else:
            print(f"❌ File not found: {json_path}")

    elif choice == "2":
        print("\n📋 Enter form details:")
        category = input("Category (e.g., weightloss, hormone): ").strip()
        form_name = input("Form name (e.g., GLP1, Sermorelin): ").strip()
        consult_type = input("Consult type (async/sync) [async]: ").strip() or "async"

        if category and form_name:
            generate_by_category_and_name(category, form_name, consult_type)
        else:
            print("❌ Category and form name are required")

    elif choice == "3":
        list_available_forms()
        interactive_mode()  # Return to menu

    elif choice == "4":
        print("👋 Goodbye!")
        return

    else:
        print("❌ Invalid choice")
        interactive_mode()

def batch_generate_all():
    """Generate HTML for all available JSON forms"""
    print("\n🚀 Batch generating all forms...")

    surveys_dir = Path("../surveys")
    success_count = 0
    total_count = 0

    # Process each category directory
    for category_dir in surveys_dir.iterdir():
        if category_dir.is_dir() and category_dir.name != "all-forms":
            category = category_dir.name

            # Find JSON files in this category
            for json_file in category_dir.glob("*-screener.json"):
                total_count += 1
                print(f"\n{'='*50}")
                if generate_single_form(str(json_file)):
                    success_count += 1

    print(f"\n🎉 Batch generation complete!")
    print(f"✅ Successfully generated: {success_count}/{total_count} forms")

    if success_count < total_count:
        print(f"❌ Failed: {total_count - success_count} forms")

def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON forms to HTML medical forms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from JSON file
  python3 generate_form.py --form ../surveys/weightloss/GLP1-screener.json

  # Generate by category and name
  python3 generate_form.py --category weightloss --form-name GLP1

  # Interactive mode
  python3 generate_form.py --interactive

  # List all available forms
  python3 generate_form.py --list-forms

  # Generate all forms
  python3 generate_form.py --batch-all
        """
    )

    parser.add_argument('--form', help='Path to JSON form file')
    parser.add_argument('--category', help='Form category (e.g., weightloss, hormone)')
    parser.add_argument('--form-name', help='Form name (e.g., GLP1, Sermorelin)')
    parser.add_argument('--consult-type', default='async', help='Consultation type (async/sync)')
    parser.add_argument('--output-dir', help='Output directory for HTML file')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--list-forms', action='store_true', help='List available forms')
    parser.add_argument('--batch-all', action='store_true', help='Generate all forms')

    args = parser.parse_args()

    print_banner()

    # Handle different modes
    if args.list_forms:
        list_available_forms()

    elif args.interactive:
        interactive_mode()

    elif args.batch_all:
        batch_generate_all()

    elif args.form:
        # Generate from JSON file
        if not os.path.exists(args.form):
            print(f"❌ File not found: {args.form}")
            sys.exit(1)

        success = generate_single_form(args.form, args.output_dir)
        sys.exit(0 if success else 1)

    elif args.category and args.form_name:
        # Generate by category and name
        success = generate_by_category_and_name(args.category, args.form_name, args.consult_type)
        sys.exit(0 if success else 1)

    else:
        # No arguments provided, show help and enter interactive mode
        parser.print_help()
        print("\n" + "="*50)
        print("No arguments provided. Entering interactive mode...")
        interactive_mode()

if __name__ == "__main__":
    main()