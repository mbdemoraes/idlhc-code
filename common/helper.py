def file_name_parser(file_name):
    final_dict = {}
    split_str = file_name.removesuffix(".csv").split("|")
    for str_piece in split_str:
        final_str = str_piece.split("_")
        final_dict[final_str[0]] = int(final_str[1])
    return final_dict