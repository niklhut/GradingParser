from colorama import Fore, Style

def get_input_options_description():
    return (
        "Press "
        f"'{Fore.GREEN}Y{Style.RESET_ALL}' or '{Fore.GREEN}1{Style.RESET_ALL}' for 'valid', "
        f"'{Fore.RED}N{Style.RESET_ALL}' or '{Fore.RED}0{Style.RESET_ALL}' for 'invalid', "
        f"'{Fore.CYAN}S{Style.RESET_ALL}' to skip, "
        f"'{Fore.CYAN}B{Style.RESET_ALL}' to go back "
        f"'{Fore.CYAN}Q{Style.RESET_ALL}' to quit | "
        f"Press '{Fore.CYAN}Enter{Style.RESET_ALL}' to confirm."
    )
