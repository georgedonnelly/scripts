import re
import sys


def process_file(file_name):
    with open(file_name, 'r') as f:
        content = f.read()

    imports = []
    image_tag_found = False

    # Find the import line for the Image component
    image_tag_found = 'import { Image } from "astro:assets";' in content

    # Process <img> tags
    img_matches = re.findall(r'<img\s+([^>]+)>', content, re.DOTALL)

    for img_match in img_matches:
        src_match = re.search(r'src="([^"]+)"', img_match)
        alt_match = re.search(r'alt="([^"]*)"', img_match)
        height_match = re.search(r'height="([^"]*)"', img_match)
        width_match = re.search(r'width="([^"]*)"', img_match)

        if src_match:
            src = src_match.group(1)
            variable_name = src.split('/')[-1].split('.')[0]
            import_statement = f'import {variable_name} from "../../assets/{src}";'
            if import_statement not in imports:
                imports.append(import_statement)

            alt_text = alt_match.group(1) if alt_match else ""
            height = height_match.group(1) if height_match else ""
            width = width_match.group(1) if width_match else ""

            new_tag = f'<Image src={{{variable_name}}} alt="{alt_text}" height={{{height}}} width={{{width}}} />'
            content = content.replace(f'<img {img_match}>', new_tag)

    # Process <a> tags
    content = re.sub(r'<a ', '<a target="_blank" ', content)

    # Insert the import statements
    if image_tag_found:
        index = content.index('import { Image } from "astro:assets";') + \
            len('import { Image } from "astro:assets";\n')
        for import_statement in reversed(imports):
            content = content[:index] + \
                import_statement + '\n' + content[index:]

    new_file_name = file_name.split(
        '.')[0] + '_processed.' + file_name.split('.')[-1]
    with open(new_file_name, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    file_name = sys.argv[1] if len(sys.argv) > 1 else "your_file.astro"
    process_file(file_name)
