import argparse
from steg_functions import (
    hide_text_in_image,
    extract_text_from_image,
    hide_image_in_image,
    extract_image_from_image
)

def main():
    parser = argparse.ArgumentParser(
        description="🔐 Multi-layer Steganography CLI Tool (Text ↔ Image & Image ↔ Image)"
    )
    subparsers = parser.add_subparsers(dest='command', help="Choose an action")

    # --- Hide Text ---
    parser_hide_text = subparsers.add_parser('hide_text', help="Hide text inside an image")
    parser_hide_text.add_argument('--input', required=True, help="Cover image file path")
    parser_hide_text.add_argument('--output', required=True, help="Output image file path")
    parser_hide_text.add_argument('--message', required=True, help="Text message to hide")

    # --- Extract Text ---
    parser_extract_text = subparsers.add_parser('extract_text', help="Extract hidden text from image")
    parser_extract_text.add_argument('--input', required=True, help="Image file containing hidden text")

    # --- Hide Image ---
    parser_hide_img = subparsers.add_parser('hide_image', help="Hide image inside another image")
    parser_hide_img.add_argument('--cover', required=True, help="Cover image file path")
    parser_hide_img.add_argument('--secret', required=True, help="Image to hide (secret)")
    parser_hide_img.add_argument('--output', required=True, help="Output image file path")

    # --- Extract Image ---
    parser_extract_img = subparsers.add_parser('extract_image', help="Extract hidden image from stego image")
    parser_extract_img.add_argument('--input', required=True, help="Image file containing hidden image")
    parser_extract_img.add_argument('--output', required=True, help="Path to save the extracted image")

    args = parser.parse_args()

    if args.command == 'hide_text':
        hide_text_in_image(args.input, args.output, args.message)
        print("✅ Text successfully hidden in image!")

    elif args.command == 'extract_text':
        message = extract_text_from_image(args.input)
        print("📤 Extracted Message:\n", message)

    elif args.command == 'hide_image':
        hide_image_in_image(args.cover, args.secret, args.output)
        print("✅ Image successfully hidden in cover image!")

    elif args.command == 'extract_image':
        extract_image_from_image(args.input, args.output)
        print("📤 Hidden image extracted and saved!")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
