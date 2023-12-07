from colorama import Fore, Style

def get_input_options_description():
    return (
        f"{Fore.GREEN}Y{Style.RESET_ALL} for 'valid', "
        f"{Fore.RED}N{Style.RESET_ALL} for 'not valid', "
        f"{Fore.CYAN}S{Style.RESET_ALL} to skip, "
        f"{Fore.YELLOW}B{Style.RESET_ALL} to go back | "
        f"Press '{Fore.CYAN}Q{Style.RESET_ALL}' to quit"
    )
